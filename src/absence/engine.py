"""The balance engine.

One engine for every legal entity. Everything that differs between entities is
read from the policy, never branched on by country name in this file. If you
ever find yourself writing `if jurisdiction == "PL"` here, the policy schema is
missing a dimension - that is the invariant this design depends on.

Two behaviours are deliberate and worth reading before changing:

*   **Entitlement can be `unknown`.** Where the law makes entitlement depend on
    evidence the employer does not hold (Poland counts previous employers and
    education towards the 10-year threshold), the engine refuses to guess. A
    silent default of 20 days is how an employer ends up owing six days per
    person per year, discovered at termination.
*   **Leave is tracked as dated lots, not as one number.** Expiry rules differ
    per origin year (NL statutory expires after 6 months, NL supplementary
    after 5 years, PL on 30 September, DE on 31 March), and you cannot apply
    them to a single running total.
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .calendars import CalendarRepository
from .model import (
    STATUS_COMPUTED,
    STATUS_UNKNOWN,
    AbsenceEvent,
    BucketBalance,
    Employee,
    EmployeeBalance,
)
from .policy import Policy, PolicyRepository

MAX_LEAVE_YEARS = 15  # guard against absurd hire dates in imported data


# --------------------------------------------------------------------------
# small date helpers (kept local so the project has no date-library dependency)
# --------------------------------------------------------------------------
def _safe_date(year: int, month: int, day: int) -> _dt.date:
    """Clamp 29 February onto 28 February in non-leap years."""
    while True:
        try:
            return _dt.date(year, month, day)
        except ValueError:
            day -= 1


def _add_months(day: _dt.date, months: int) -> _dt.date:
    total = day.month - 1 + months
    return _safe_date(day.year + total // 12, total % 12 + 1, day.day)


def _overlap_months(
    a_start: _dt.date, a_end: _dt.date, ly_start: _dt.date, ly_end: _dt.date
) -> float:
    """How much of a leave year an interval covers, expressed in twelfths.

    Measured against the length of that leave year rather than a nominal
    30-day month, so a full year is exactly 12.0 and the proration test does
    not fire on rounding noise.
    """
    start = max(a_start, ly_start)
    end = min(a_end, ly_end)
    if end < start:
        return 0.0
    covered = (end - start).days + 1
    total = (ly_end - ly_start).days + 1
    return 12.0 * covered / total


def _service_months(hire: _dt.date, ref: _dt.date) -> float:
    if ref < hire:
        return 0.0
    return (ref.year - hire.year) * 12 + (ref.month - hire.month) + (ref.day - hire.day) / 30.0


def _round(value: float, mode: str) -> float:
    if mode == "up_full_day":
        return float(int(value)) + (1.0 if value > int(value) else 0.0)
    if mode == "up_half_day":
        return round(value * 2 + 0.4999) / 2
    if mode == "nearest_half_day":
        return round(value * 2) / 2
    return round(value, 3)


@dataclass
class Lot:
    """A dated pot of entitlement. Expiry attaches to the lot, not the balance."""

    origin_year_end: _dt.date
    granted: float
    remaining: float
    expires_on: Optional[_dt.date]
    notice_required: bool = False

    @property
    def sort_key(self) -> Tuple[_dt.date, _dt.date]:
        return (self.expires_on or _dt.date.max, self.origin_year_end)


class AbsenceEngine:
    def __init__(
        self,
        policies: PolicyRepository,
        calendars: Optional[CalendarRepository] = None,
        ledger_start: Optional[_dt.date] = None,
        opening_balances: Optional[Dict[Tuple[str, str], float]] = None,
    ):
        self.policies = policies
        self.calendars = calendars or CalendarRepository()
        # The cut-over date. Nobody has clean absence history back to an
        # employee's hire date, so the engine does not pretend to: it starts
        # from a signed-off opening balance and only recomputes forward.
        # This is why the tool can be deployed alongside the current process
        # instead of after a migration.
        self.ledger_start = ledger_start
        self.opening_balances: Dict[Tuple[str, str], float] = opening_balances or {}

    # ---------------------------------------------------------------- leave year
    def leave_year_bounds(
        self, policy: Policy, ref: _dt.date, employee: Employee
    ) -> Tuple[_dt.date, _dt.date]:
        cfg = policy.leave_year
        kind = cfg.get("type", "calendar")
        if kind == "calendar":
            return _dt.date(ref.year, 1, 1), _dt.date(ref.year, 12, 31)
        if kind == "fixed_window":
            month, day = int(cfg["start_month"]), int(cfg["start_day"])
            start = _safe_date(ref.year, month, day)
            if ref < start:
                start = _safe_date(ref.year - 1, month, day)
            end = _safe_date(start.year + 1, month, day) - _dt.timedelta(days=1)
            return start, end
        if kind == "anniversary":
            month, day = employee.hire_date.month, employee.hire_date.day
            start = _safe_date(ref.year, month, day)
            if ref < start:
                start = _safe_date(ref.year - 1, month, day)
            end = _safe_date(start.year + 1, month, day) - _dt.timedelta(days=1)
            return start, end
        raise ValueError(f"unknown leave_year type '{kind}'")

    def _leave_years_until(
        self, policy: Policy, employee: Employee, as_of: _dt.date
    ) -> List[Tuple[_dt.date, _dt.date]]:
        current = self.leave_year_bounds(policy, as_of, employee)
        opened = employee.hire_date
        if self.ledger_start is not None and self.ledger_start > opened:
            opened = self.ledger_start
        first = self.leave_year_bounds(policy, opened, employee)
        years: List[Tuple[_dt.date, _dt.date]] = []
        cursor = first
        while cursor[0] <= current[0] and len(years) < MAX_LEAVE_YEARS:
            years.append(cursor)
            cursor = self.leave_year_bounds(
                policy, cursor[1] + _dt.timedelta(days=1), employee
            )
        if not years:
            years = [current]
        if years[-1][0] != current[0]:
            years.append(current)
        return years

    # ---------------------------------------------------------------- service
    @staticmethod
    def service_years_at(employee: Employee, ref: _dt.date, accrual: Dict[str, Any]) -> Optional[float]:
        """Statutory service, which is not the same thing as tenure.

        Returns None when the policy says entitlement depends on evidence the
        employer must hold and that evidence is not on file.
        """
        if accrual.get("evidence_required") and not employee.service_evidence_on_file:
            return None
        years = max(0.0, (ref - employee.hire_date).days / 365.25)
        if accrual.get("counts_previous_employers"):
            years += employee.prior_service_years
        if accrual.get("counts_education"):
            years += employee.education_credit_years
        return years

    # ---------------------------------------------------------------- entitlement
    def _entitlement(
        self,
        bucket: Dict[str, Any],
        employee: Employee,
        ly_start: _dt.date,
        ly_end: _dt.date,
        policy: Policy,
        as_of: _dt.date,
    ) -> Tuple[Optional[float], List[str], List[str]]:
        accrual = bucket.get("accrual", {})
        method = accrual.get("method", "fixed")
        flags: List[str] = []
        trace: List[str] = []
        base: Optional[float] = None

        if method == "fixed":
            base = float(accrual["amount"])
            trace.append(f"fixed entitlement {base} {policy.unit}")

        elif method == "tiered_by_service":
            eval_at = min(ly_end, as_of) if as_of >= ly_start else ly_end
            service = self.service_years_at(employee, eval_at, accrual)
            if service is None:
                flags.append("SERVICE_EVIDENCE_MISSING")
                trace.append(
                    "entitlement depends on total statutory service (previous employers "
                    "and education). No evidence on file -> refusing to assume a tier."
                )
                return None, flags, trace
            tiers = sorted(accrual["tiers"], key=lambda t: -float(t["service_years_gte"]))
            for tier in tiers:
                if service >= float(tier["service_years_gte"]):
                    base = float(tier["amount"])
                    trace.append(
                        f"statutory service {service:.2f}y at {eval_at.isoformat()} "
                        f">= {tier['service_years_gte']}y -> {base} {policy.unit}"
                    )
                    break
            # Flag an upgrade that lands inside this leave year but after as_of,
            # so HR sees it coming instead of discovering it in a payroll dispute.
            service_at_end = self.service_years_at(employee, ly_end, accrual)
            if service_at_end is not None and base is not None:
                for tier in tiers:
                    if service_at_end >= float(tier["service_years_gte"]) and float(tier["amount"]) > base:
                        flags.append("TIER_UPGRADE_DURING_LEAVE_YEAR")
                        trace.append(
                            f"crosses {tier['service_years_gte']}y threshold before "
                            f"{ly_end.isoformat()} -> entitlement rises to {tier['amount']}"
                        )
                        break

        elif method == "weekly_hours_multiple":
            multiple = float(accrual["multiple"])
            basis = employee.weekly_hours if policy.unit == "hours" else employee.working_days_per_week
            base = multiple * basis
            trace.append(f"{multiple} x weekly basis {basis} -> {base} {policy.unit}")

        elif method == "monthly_accrual":
            base = float(accrual["annual_amount"])
            trace.append(f"accrues {base / 12:.4f} {policy.unit} per completed month")

        elif method == "hours_worked_percentage":
            pct = float(accrual["percentage"])
            weeks = ((ly_end - ly_start).days + 1) / 7.0
            hours = employee.weekly_hours * weeks
            base = pct * hours
            if policy.unit == "days" and employee.weekly_hours:
                base = base / (employee.weekly_hours / employee.working_days_per_week)
            cap = accrual.get("cap")
            if cap is not None:
                capped = min(base, float(cap))
                trace.append(f"{pct:.0%} of {hours:.0f} contracted hours, capped at {cap}")
                base = capped
            else:
                trace.append(f"{pct:.0%} of {hours:.0f} contracted hours")
            flags.append("ACCRUAL_USES_CONTRACTED_HOURS")

        elif method == "days_worked_threshold":
            base = float(accrual["amount"])
            trace.append(
                f"{base} {policy.unit} once the {accrual.get('threshold_days', 240)}-day "
                "qualifying period is met"
            )
        else:
            raise ValueError(f"unknown accrual method '{method}'")

        # Qualifying period ------------------------------------------------
        min_months = accrual.get("eligibility_service_months")
        if min_months:
            served = _service_months(employee.hire_date, ly_end)
            if served < float(min_months):
                trace.append(
                    f"qualifying period not met ({served:.1f} of {min_months} months) -> 0"
                )
                flags.append("QUALIFYING_PERIOD_NOT_MET")
                return 0.0, flags, trace

        # Proration for part-years (joiners and leavers) --------------------
        if bucket.get("proration", "monthly") != "none" and base is not None:
            employed_from = max(ly_start, employee.hire_date)
            employed_to = min(ly_end, employee.termination_date or ly_end)
            months = _overlap_months(employed_from, employed_to, ly_start, ly_end)
            if months < 11.99:
                prorated = base * min(months, 12.0) / 12.0
                trace.append(
                    f"prorated for {months:.1f}/12 months employed -> {prorated:.3f}"
                )
                base = prorated
                flags.append("PRORATED")

        if base is not None:
            base = _round(base, policy.rounding)
        return base, flags, trace

    # ---------------------------------------------------------------- expiry
    @staticmethod
    def _expiry_for(expiry: Dict[str, Any], origin_year_end: _dt.date) -> Optional[_dt.date]:
        kind = (expiry or {}).get("type", "none")
        if kind == "none":
            return None
        if kind == "end_of_leave_year":
            return origin_year_end
        if kind == "deadline_in_next_year":
            return _safe_date(origin_year_end.year + 1, int(expiry["month"]), int(expiry["day"]))
        if kind == "months_after_leave_year_end":
            return _add_months(origin_year_end, int(expiry["months"]))
        if kind == "years_after_leave_year_end":
            return _safe_date(
                origin_year_end.year + int(expiry["years"]),
                origin_year_end.month,
                origin_year_end.day,
            )
        raise ValueError(f"unknown expiry type '{kind}'")

    # ---------------------------------------------------------------- main
    def balance(
        self,
        employee: Employee,
        events: Iterable[AbsenceEvent],
        as_of: _dt.date,
    ) -> EmployeeBalance:
        policy = self.policies.get(employee.entity_id, as_of, employee.work_region)
        years = self._leave_years_until(policy, employee, as_of)
        ly_start, ly_end = years[-1]

        own_events = [e for e in events if e.employee_id == employee.employee_id]
        result = EmployeeBalance(
            employee_id=employee.employee_id,
            entity_id=employee.entity_id,
            as_of=as_of,
            leave_year_start=ly_start,
            leave_year_end=ly_end,
        )

        for bucket in policy.buckets:
            result.buckets.append(
                self._bucket_balance(bucket, employee, own_events, years, policy, as_of)
            )
        return result

    def _events_for(
        self,
        bucket: Dict[str, Any],
        events: List[AbsenceEvent],
        start: _dt.date,
        end: _dt.date,
        status: str,
    ) -> float:
        bucket_id = bucket["id"]
        bucket_type = bucket.get("absence_type", "annual_leave")
        total = 0.0
        for ev in events:
            if ev.status != status:
                continue
            if not (start <= ev.start_date <= end):
                continue
            if ev.bucket_id:
                if ev.bucket_id != bucket_id:
                    continue
            elif ev.absence_type != bucket_type:
                continue
            total += ev.days
        return total

    def _bucket_balance(
        self,
        bucket: Dict[str, Any],
        employee: Employee,
        events: List[AbsenceEvent],
        years: List[Tuple[_dt.date, _dt.date]],
        policy: Policy,
        as_of: _dt.date,
    ) -> BucketBalance:
        out = BucketBalance(
            bucket_id=bucket["id"],
            label=bucket.get("label", bucket["id"]),
            unit=bucket.get("unit", policy.unit),
        )
        out.trace.append(
            f"policy {policy.source_file} v{policy.effective_from.isoformat()} "
            f"({policy.describe()}); legal basis: {policy.legal_basis or 'n/a'}"
        )

        carryover = bucket.get("carryover", {})
        expiry_cfg = bucket.get("expiry", {"type": "none"})
        lots: List[Lot] = []
        expired_total = 0.0
        encashed_total = 0.0
        overdrawn = 0.0

        # Seed the opening balance for anyone who was already employed when the
        # ledger started. Refusing to invent this number is the same discipline
        # as refusing to invent a Polish seniority tier.
        if employee.hire_date < years[0][0]:
            key = (employee.employee_id, bucket["id"])
            if key not in self.opening_balances:
                out.status = STATUS_UNKNOWN
                out.remaining = None
                out.flags.append("OPENING_BALANCE_MISSING")
                out.trace.append(
                    f"employed since {employee.hire_date.isoformat()}, before the ledger "
                    f"opened on {years[0][0].isoformat()}, and no signed-off opening "
                    "balance exists -> reported as UNKNOWN rather than as zero"
                )
                return out
            opening = float(self.opening_balances[key])
            prior_end = years[0][0] - _dt.timedelta(days=1)
            if opening > 0:
                lots.append(
                    Lot(
                        origin_year_end=prior_end,
                        granted=opening,
                        remaining=opening,
                        expires_on=self._expiry_for(expiry_cfg, prior_end),
                        notice_required=bool(expiry_cfg.get("requires_employer_notice")),
                    )
                )
            out.trace.append(
                f"opening balance {opening} {out.unit} carried in at "
                f"{years[0][0].isoformat()} (signed off, not recomputed)"
            )

        for index, (ly_start, ly_end) in enumerate(years):
            is_current = index == len(years) - 1
            if is_current:
                # `expired` and `encashed` report what is being lost in the
                # leave year now open. Losses from closed years are history and
                # would otherwise pile up into a meaningless lifetime total.
                if expired_total or encashed_total:
                    out.trace.append(
                        f"in closed leave years since the cut-over: {expired_total:.2f} "
                        f"{out.unit} lapsed, {encashed_total:.2f} became payable"
                    )
                expired_total = 0.0
                encashed_total = 0.0

            # 1. expire anything that lapsed before this leave year opened
            cut = as_of if is_current else ly_start
            for lot in lots:
                if lot.remaining <= 0 or lot.expires_on is None:
                    continue
                if lot.expires_on < cut:
                    if lot.notice_required and not employee.expiry_notice_given:
                        if "EXPIRY_NOT_ENFORCEABLE" not in out.flags:
                            out.flags.append("EXPIRY_NOT_ENFORCEABLE")
                            out.trace.append(
                                f"{lot.remaining:.2f} {out.unit} from {lot.origin_year_end.year} "
                                f"passed {lot.expires_on.isoformat()} but no evidence the employee "
                                "was warned - statutory forfeiture is not enforceable, days kept"
                            )
                        continue
                    expired_total += lot.remaining
                    out.trace.append(
                        f"{lot.remaining:.2f} {out.unit} from {lot.origin_year_end.year} "
                        f"expired on {lot.expires_on.isoformat()}"
                    )
                    lot.remaining = 0.0

            # 2. apply the carry-forward cap at the year boundary
            if index > 0:
                allowed = carryover.get("allowed", True)
                cap = carryover.get("max_days")
                live = sum(l.remaining for l in lots)
                if not allowed and live > 0:
                    expired_total += live
                    out.trace.append(
                        f"carry-forward not permitted -> {live:.2f} {out.unit} lapsed at "
                        f"{ly_start.isoformat()}"
                    )
                    for lot in lots:
                        lot.remaining = 0.0
                elif cap is not None and live > float(cap):
                    excess = live - float(cap)
                    if carryover.get("encash_above_cap"):
                        encashed_total += excess
                        out.trace.append(
                            f"balance {live:.2f} exceeds carry cap {cap} -> {excess:.2f} "
                            f"{out.unit} must be paid out (statutory encashment)"
                        )
                    else:
                        expired_total += excess
                        out.trace.append(
                            f"balance {live:.2f} exceeds carry cap {cap} -> {excess:.2f} "
                            f"{out.unit} forfeited"
                        )
                    for lot in sorted(lots, key=lambda l: l.sort_key):
                        if excess <= 0:
                            break
                        take = min(lot.remaining, excess)
                        lot.remaining -= take
                        excess -= take

            # 3. grant this year's entitlement
            entitlement, flags, trace = self._entitlement(
                bucket, employee, ly_start, ly_end, policy, as_of
            )
            # Only the current leave year's flags describe the balance being
            # reported. A proration that applied in the year someone joined is
            # history, not a caveat on today's number.
            if is_current:
                for f in flags:
                    if f not in out.flags:
                        out.flags.append(f)
                out.trace.extend(trace)
                out.entitlement = entitlement
            if entitlement is None:
                if not is_current:
                    # The reason has to travel with the result even when the
                    # blocking year is a historical one.
                    for f in flags:
                        if f not in out.flags:
                            out.flags.append(f)
                    out.trace.extend(trace)
                out.status = STATUS_UNKNOWN
                out.remaining = None
                out.trace.append(
                    "balance cannot be computed lawfully -> reported as UNKNOWN, "
                    "not as a default"
                )
                return out

            granted = entitlement
            if is_current and bucket.get("accrual", {}).get("method") == "monthly_accrual":
                served = _overlap_months(
                    max(ly_start, employee.hire_date), min(as_of, ly_end), ly_start, ly_end
                )
                granted = _round(entitlement * min(served, 12.0) / 12.0, policy.rounding)
                out.trace.append(
                    f"accrued {granted} of {entitlement} {out.unit} "
                    f"by {as_of.isoformat()} ({served:.1f} months)"
                )

            lots.append(
                Lot(
                    origin_year_end=ly_end,
                    granted=granted,
                    remaining=granted,
                    expires_on=self._expiry_for(expiry_cfg, ly_end),
                    notice_required=bool(expiry_cfg.get("requires_employer_notice")),
                )
            )

            # 4. consume this year's absences, oldest-expiring first
            window_end = as_of if is_current else ly_end
            taken = self._events_for(bucket, events, ly_start, window_end, "approved")
            scheduled = 0.0
            if is_current:
                scheduled = self._events_for(
                    bucket, events, as_of + _dt.timedelta(days=1), ly_end, "approved"
                )
                out.taken = taken
                out.scheduled = scheduled
            demand = taken + scheduled
            for lot in sorted(lots, key=lambda l: l.sort_key):
                if demand <= 0:
                    break
                take = min(lot.remaining, demand)
                lot.remaining -= take
                demand -= take
            if demand > 0:
                if is_current:
                    if "NEGATIVE_BALANCE" not in out.flags:
                        out.flags.append("NEGATIVE_BALANCE")
                    overdrawn += demand
                    out.trace.append(
                        f"{demand:.2f} {out.unit} approved beyond what is available in "
                        f"{ly_start.year} - over-approval, or leave booked against "
                        "entitlement not yet accrued"
                    )
                else:
                    if "HISTORIC_OVERDRAW" not in out.flags:
                        out.flags.append("HISTORIC_OVERDRAW")
                    out.trace.append(
                        f"{demand:.2f} {out.unit} were taken beyond entitlement in "
                        f"{ly_start.year} - a data quality issue in a closed year, "
                        "not carried into today's balance"
                    )

        out.carried_in = round(
            sum(l.remaining for l in lots if l.origin_year_end < years[-1][1]), 3
        )
        out.expired = round(expired_total, 3)
        out.encashed = round(encashed_total, 3)
        live = sum(l.remaining for l in lots)
        out.remaining = round(live - overdrawn, 3)
        out.status = STATUS_COMPUTED

        # Surface the next thing that will lapse - the single most useful number
        # for the person who has to nudge employees to take their leave.
        upcoming = [
            l for l in lots if l.remaining > 0 and l.expires_on and l.expires_on >= as_of
        ]
        if upcoming:
            soonest = min(upcoming, key=lambda l: l.expires_on)
            out.trace.append(
                f"next expiry: {soonest.remaining:.2f} {out.unit} lapse on "
                f"{soonest.expires_on.isoformat()}"
            )
        return out

    # ---------------------------------------------------------------- sick pay
    def sick_pay(
        self, employee: Employee, events: Iterable[AbsenceEvent], year: int
    ) -> Optional[Dict[str, Any]]:
        """Split sickness absence into employer-funded and state-funded days.

        Included because sick leave, not annual leave, is where the entity-level
        differences bite hardest on cost, and because it is the clearest example
        of a rule that must never be globalised: Poland funds the first 33 days
        from the employer, 14 if the employee is 50 or older.
        """
        as_of = _dt.date(year, 12, 31)
        policy = self.policies.get(employee.entity_id, as_of, employee.work_region)
        cfg = policy.sick_pay
        if not cfg:
            return None

        bands = cfg.get("employer_paid", [])
        age = employee.age_at(_dt.date(year, 1, 1))
        chosen = None
        for band in bands:
            cond = band.get("condition", "always")
            if cond == "always":
                chosen = band
                break
            if cond.startswith("age_gte_") and age is not None and age >= int(cond.split("_")[-1]):
                chosen = band
                break
            if cond.startswith("age_lt_") and age is not None and age < int(cond.split("_")[-1]):
                chosen = band
                break
        if chosen is None:
            return None

        total = sum(
            e.days
            for e in events
            if e.employee_id == employee.employee_id
            and e.absence_type == "sick_leave"
            and e.status == "approved"
            and e.start_date.year == year
        )
        employer_days = min(total, float(chosen["days"]))
        return {
            "employee_id": employee.employee_id,
            "entity_id": employee.entity_id,
            "year": year,
            "sick_days_total": round(total, 2),
            "employer_paid_days": round(employer_days, 2),
            "employer_rate": chosen.get("rate"),
            "transferred_days": round(total - employer_days, 2),
            "transferred_to": cfg.get("then", "state authority"),
            "band": chosen.get("condition", "always"),
        }
