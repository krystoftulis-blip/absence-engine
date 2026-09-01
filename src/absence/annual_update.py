"""The annual update, turned into a review instead of a rebuild.

The brief names annual updates - public holidays and seniority-based
entitlements - as a specific source of compliance-heavy manual work. This
module does not perform the update. It produces the list of things that must be
changed, who owns each one, and what evidence is missing, and it refuses to
apply anything automatically.

That restraint is the design. Auto-applying a legal change is how a wrong rule
silently reaches 500 people's balances. Producing a diff that a named human
approves keeps the review where it belongs while removing the part that is
genuinely mechanical: finding out what changed.
"""

from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .calendars import CalendarRepository
from .engine import AbsenceEngine
from .model import Employee
from .policy import PolicyRepository

BLOCKER = "blocker"
ACTION = "action"
INFO = "info"


@dataclass
class Item:
    severity: str
    area: str
    entity_id: str
    subject: str
    detail: str
    owner: str

    def to_row(self) -> Dict[str, Any]:
        return {
            "severity": self.severity,
            "area": self.area,
            "entity_id": self.entity_id,
            "subject": self.subject,
            "detail": self.detail,
            "owner": self.owner,
        }


def _threshold_crossing_date(
    employee: Employee, accrual: Dict[str, Any], threshold: float
) -> Optional[_dt.date]:
    credited = 0.0
    if accrual.get("counts_previous_employers"):
        credited += employee.prior_service_years
    if accrual.get("counts_education"):
        credited += employee.education_credit_years
    remaining_years = threshold - credited
    if remaining_years <= 0:
        return employee.hire_date
    return employee.hire_date + _dt.timedelta(days=remaining_years * 365.25)


def run(
    engine: AbsenceEngine,
    policies: PolicyRepository,
    calendars: CalendarRepository,
    employees: List[Employee],
    year: int,
    today: Optional[_dt.date] = None,
) -> List[Item]:
    today = today or _dt.date.today()
    items: List[Item] = []
    in_engine = [
        row for row in policies.registry_entries if row.get("treatment") == "engine"
    ]

    for row in in_engine:
        entity_id = row["entity_id"]
        try:
            policy = policies.get(entity_id, _dt.date(year, 6, 30))
        except Exception:
            policy = None

        # 1. policy versions that will be out of review ----------------------
        if policy and policy.review_due and policy.review_due < _dt.date(year, 1, 1):
            items.append(Item(
                BLOCKER, "policy", entity_id,
                f"policy review overdue ({policy.review_due.isoformat()})",
                "The rule set has not been re-confirmed by counsel. Balances are still "
                "computed, but they are computed from unverified rules.",
                policy.reviewed_by or "unassigned",
            ))

        # 2. holiday calendars ----------------------------------------------
        needed = set()
        if policy:
            needed.add(policy.holiday_calendar)
        # Entities whose rules are region-specific (India) cannot be resolved
        # without a region, so ask for each region's calendar explicitly.
        for region_key in policies.region_keys(entity_id, _dt.date(year, 6, 30)):
            try:
                variant = policies.get(entity_id, _dt.date(year, 6, 30), region_key)
                needed.add(variant.holiday_calendar)
            except Exception:
                continue
        for key in sorted(k for k in needed if k):
            if not calendars.has(key, year):
                items.append(Item(
                    BLOCKER, "calendar", entity_id,
                    f"no public holiday calendar for {key} {year}",
                    "Working-day counts and holiday entitlement cannot be produced for "
                    f"{year} until this calendar is supplied and signed off locally.",
                    f"Local HR lead ({key})",
                ))
            elif not calendars.is_confirmed(key, year):
                items.append(Item(
                    BLOCKER, "calendar", entity_id,
                    f"calendar {key} {year} is present but not confirmed",
                    "The file carries national holidays only. Regional or state "
                    "holidays are missing and must be added by the local lead.",
                    f"Local HR lead ({key})",
                ))

    # 3. people crossing a seniority threshold during the year ---------------
    by_entity = {row["entity_id"] for row in in_engine}
    for emp in employees:
        if emp.entity_id not in by_entity:
            continue
        try:
            policy = policies.get(emp.entity_id, _dt.date(year, 6, 30), emp.work_region)
        except Exception:
            continue
        for bucket in policy.buckets:
            accrual = bucket.get("accrual", {})
            if accrual.get("method") != "tiered_by_service":
                continue
            if accrual.get("evidence_required") and not emp.service_evidence_on_file:
                items.append(Item(
                    ACTION, "entitlement", emp.entity_id,
                    f"{emp.employee_id}: statutory service undocumented",
                    "Entitlement cannot be determined without evidence of previous "
                    "employment and education. Until it is on file the balance is "
                    "reported as unknown, not as the lower tier.",
                    f"HR administrator ({emp.entity_id})",
                ))
                continue
            tiers = sorted(accrual["tiers"], key=lambda t: float(t["service_years_gte"]))
            for tier in tiers:
                threshold = float(tier["service_years_gte"])
                if threshold <= 0:
                    continue
                crossing = _threshold_crossing_date(emp, accrual, threshold)
                if crossing and _dt.date(year, 1, 1) <= crossing <= _dt.date(year, 12, 31):
                    items.append(Item(
                        ACTION, "entitlement", emp.entity_id,
                        f"{emp.employee_id}: reaches {threshold:g} years on "
                        f"{crossing.isoformat()}",
                        f"Entitlement rises to {tier['amount']} {policy.unit}. "
                        "Confirm the service record before the change takes effect.",
                        f"HR administrator ({emp.entity_id})",
                    ))

    # 4. opening balances still missing --------------------------------------
    missing = []
    for emp in employees:
        if emp.entity_id not in by_entity or not engine.ledger_start:
            continue
        if emp.hire_date >= engine.ledger_start:
            continue
        try:
            bucket_ids = [b["id"] for b in policies.get(
                emp.entity_id, _dt.date(year, 6, 30), emp.work_region).buckets]
        except Exception:
            continue
        if not any((emp.employee_id, b) in engine.opening_balances for b in bucket_ids):
            missing.append(emp)
    for emp in missing:
        items.append(Item(
            BLOCKER, "ledger", emp.entity_id,
            f"{emp.employee_id}: no signed-off opening balance",
            "Employed before the ledger cut-over with no agreed starting balance. "
            "Every balance for this person is unknown until the entity signs one off.",
            f"Country HR lead ({emp.entity_id})",
        ))

    order = {BLOCKER: 0, ACTION: 1, INFO: 2}
    items.sort(key=lambda i: (order[i.severity], i.area, i.entity_id, i.subject))
    return items
