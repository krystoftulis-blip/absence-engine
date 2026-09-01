"""Generate the synthetic dataset shipped with this repository.

No real employee data is used anywhere in this project. This script is seeded,
so `python scripts/generate_sample_data.py` reproduces byte-identical files and
the numbers quoted in DECISION.md can be checked independently.

It does two things:

1.  writes a canonical ledger (employees + absence events);
2.  writes three "current state" exports in the shape a real fragmented estate
    produces - different delimiters, different languages, different column
    names - and injects a specific, named set of errors into them.

The injected errors are not noise. Each one is a failure mode observed in
practice, and the reconciliation report is judged on whether it finds them:

    E1  seniority tier missed        - PL, degree holders past the 10-year mark
                                       still on 20 days instead of 26
    E2  expired days still shown     - PL, carry-over kept on the sheet after
                                       the 30 September deadline
    E3  unlawful expiry applied      - NL, statutory days written off without
                                       the employer notice that makes the
                                       forfeiture enforceable
    E4  wrong regional rule          - IN, a Maharashtra employee administered
                                       on Karnataka's 18-day entitlement
    E5  rounding drift               - everywhere, sub-half-day differences
"""

from __future__ import annotations

import csv
import datetime as _dt
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

from absence.calendars import CalendarRepository            # noqa: E402
from absence.engine import AbsenceEngine                    # noqa: E402
from absence.model import AbsenceEvent, Employee            # noqa: E402
from absence.policy import PolicyRepository                 # noqa: E402

AS_OF = _dt.date(2026, 9, 1)
LEDGER_START = _dt.date(2024, 1, 1)
SEED = 20260901
DATA = os.path.join(ROOT, "data")
EXPORTS = os.path.join(DATA, "entity_exports")

EMP_FIELDS = [
    "employee_id", "entity_id", "hire_date", "weekly_hours", "working_days_per_week",
    "birth_date", "work_region", "prior_service_years", "education_credit_years",
    "service_evidence_on_file", "expiry_notice_given", "termination_date",
]
ABS_FIELDS = [
    "event_id", "employee_id", "absence_type", "start_date", "end_date",
    "days", "status", "bucket_id", "note",
]


def build_people(rng: random.Random):
    people = []

    # -- hand-built cases the tests assert on -----------------------------
    people += [
        # E1: master's degree (8 years credit) plus 4 years elsewhere -> already
        # past 10 years of statutory service on day one. Entitlement is 26.
        dict(employee_id="PL-0001", entity_id="PL-SSC", hire_date="2022-03-01",
             birth_date="1990-05-12", prior_service_years=4, education_credit_years=8,
             service_evidence_on_file="yes"),
        # Same profile, no documents on file -> entitlement is UNKNOWN, not 20.
        dict(employee_id="PL-0002", entity_id="PL-SSC", hire_date="2021-09-15",
             birth_date="1988-01-30", prior_service_years=6, education_credit_years=8,
             service_evidence_on_file="no"),
        # Crosses the 10-year threshold during 2026 -> flagged before it happens.
        dict(employee_id="PL-0003", entity_id="PL-SSC", hire_date="2019-11-01",
             birth_date="1995-07-07", prior_service_years=0, education_credit_years=6,
             service_evidence_on_file="yes"),
        # Over 50: employer funds only 14 sick days, not 33.
        dict(employee_id="PL-0004", entity_id="PL-SSC", hire_date="2015-02-02",
             birth_date="1972-04-18", prior_service_years=12, education_credit_years=8,
             service_evidence_on_file="yes"),
        # E3: Dutch employee who was never warned -> statutory days survive.
        dict(employee_id="NL-0001", entity_id="NL-BV", hire_date="2020-01-06",
             birth_date="1991-09-09", expiry_notice_given="no"),
        # Warned in writing -> the same days do lapse.
        dict(employee_id="NL-0002", entity_id="NL-BV", hire_date="2019-04-01",
             birth_date="1985-12-01", expiry_notice_given="yes"),
        # E4: Maharashtra, 21 days - not Karnataka's 18.
        dict(employee_id="IN-0001", entity_id="IN-SSC", hire_date="2021-06-01",
             birth_date="1993-02-14", work_region="MH"),
        dict(employee_id="IN-0002", entity_id="IN-SSC", hire_date="2023-08-16",
             birth_date="1997-11-23", work_region="KA"),
        # California: accrued vacation cannot be forfeited.
        dict(employee_id="US-0001", entity_id="US-CORP", hire_date="2018-07-09",
             birth_date="1986-03-03", work_region="CA"),
        dict(employee_id="US-0002", entity_id="US-CORP", hire_date="2022-01-10",
             birth_date="1994-08-21", work_region="IL"),
        # Ireland: leave year runs April to March.
        dict(employee_id="IE-0001", entity_id="IE-INTL", hire_date="2021-05-04",
             birth_date="1990-10-10", weekly_hours=40),
        # Part-time, to exercise the pro-rata path.
        dict(employee_id="IE-0002", entity_id="IE-INTL", hire_date="2023-09-11",
             birth_date="1996-06-30", weekly_hours=24, working_days_per_week=3),
        dict(employee_id="DE-0001", entity_id="DE-GMBH", hire_date="2017-03-20",
             birth_date="1983-01-15", work_region="BE", expiry_notice_given="yes"),
        dict(employee_id="DE-0002", entity_id="DE-GMBH", hire_date="2024-10-01",
             birth_date="1999-05-05", work_region="BY", expiry_notice_given="no"),
    ]

    # -- bulk population --------------------------------------------------
    plan = [("PL-SSC", "PL", 16, None), ("IN-SSC", "IN", 10, ["KA", "MH", "DL", "TN"]),
            ("US-CORP", "US", 8, ["IL", "CA"]), ("NL-BV", "NL", 4, None),
            ("DE-GMBH", "DE", 3, ["BE", "BY"]), ("IE-INTL", "IE", 3, None)]
    for entity, prefix, count, regions in plan:
        start = sum(1 for p in people if p["entity_id"] == entity) + 1
        for i in range(start, start + count):
            hire = _dt.date(rng.randint(2015, 2025), rng.randint(1, 12), rng.randint(1, 28))
            born = _dt.date(rng.randint(1968, 2001), rng.randint(1, 12), rng.randint(1, 28))
            part_time = rng.random() < 0.15
            people.append(dict(
                employee_id=f"{prefix}-{i:04d}",
                entity_id=entity,
                hire_date=hire.isoformat(),
                birth_date=born.isoformat(),
                weekly_hours=24 if part_time else 40,
                working_days_per_week=3 if part_time else 5,
                work_region=rng.choice(regions) if regions else "",
                prior_service_years=rng.choice([0, 0, 2, 3, 5, 9]) if entity == "PL-SSC" else 0,
                education_credit_years=rng.choice([0, 6, 8]) if entity == "PL-SSC" else 0,
                service_evidence_on_file=rng.choice(["yes"] * 6 + ["no"])
                if entity == "PL-SSC" else "yes",
                expiry_notice_given=rng.choice(["yes", "yes", "yes", "yes", "no"]),
            ))

    for p in people:
        p.setdefault("weekly_hours", 40)
        p.setdefault("working_days_per_week", 5)
        p.setdefault("work_region", "")
        p.setdefault("prior_service_years", 0)
        p.setdefault("education_credit_years", 0)
        p.setdefault("service_evidence_on_file", "yes")
        p.setdefault("expiry_notice_given", "no")
        p.setdefault("termination_date", "")
    return people


# How much of each pot people actually use in a year, as a (min, max) day range.
# Real utilisation is high - most people take most of their leave - and the
# residual balance is small. Modelling low utilisation would make the
# reconciliation look dramatic for the wrong reason.
UTILISATION = {
    "PL-SSC":  {"annual_leave": (16, 24)},
    "IN-SSC":  {"earned_leave": (10, 17), "casual_leave": (4, 11), "sick_leave": (2, 9)},
    "US-CORP": {"pto": (8, 14)},
    "NL-BV":   {"statutory": (14, 20), "supplementary": (2, 5)},
    "DE-GMBH": {"statutory": (14, 20), "contractual": (3, 8)},
    "IE-INTL": {"annual_leave": (12, 19)},
}
CHUNKS = [1, 1, 1, 2, 2, 3, 5, 5, 10]
TYPE_OF = {"casual_leave": "special_leave", "sick_leave": "sick_leave"}


def build_absences(people, rng: random.Random):
    events = []
    counter = 1
    for p in people:
        hire = _dt.date.fromisoformat(p["hire_date"])
        buckets = UTILISATION[p["entity_id"]]
        for year in range(max(2024, hire.year), 2027):
            for bucket, (lo, hi) in buckets.items():
                target = rng.uniform(lo, hi)
                if year == 2026:
                    target *= 0.62                       # year is two thirds gone
                if hire.year == year:
                    target *= max(0.1, (12 - hire.month) / 12.0)
                used = 0.0
                guard = 0
                while used < target and guard < 12:
                    guard += 1
                    length = min(rng.choice(CHUNKS), max(1, int(round(target - used))))
                    month = rng.randint(1, 8 if year == 2026 else 12)
                    start = _dt.date(year, month, rng.randint(1, 20))
                    if start < hire:
                        continue
                    events.append(dict(
                        event_id=f"EV-{counter:05d}",
                        employee_id=p["employee_id"],
                        absence_type=TYPE_OF.get(bucket, "annual_leave"),
                        start_date=start.isoformat(),
                        end_date=(start + _dt.timedelta(days=length - 1)).isoformat(),
                        days=float(length),
                        status="approved",
                        bucket_id=bucket,
                        note="",
                    ))
                    counter += 1
                    used += length
        # a future booking, so "scheduled" is exercised separately from "taken"
        if rng.random() < 0.4:
            start = _dt.date(2026, rng.randint(10, 12), rng.randint(1, 20))
            events.append(dict(
                event_id=f"EV-{counter:05d}", employee_id=p["employee_id"],
                absence_type="annual_leave", start_date=start.isoformat(),
                end_date=(start + _dt.timedelta(days=3)).isoformat(), days=4.0,
                status="approved",
                bucket_id=list(buckets)[0], note="booked ahead",
            ))
            counter += 1
    # a couple of sickness spells, for the sick-pay split
    for emp in ("PL-0004", "PL-0001"):
        events.append(dict(
            event_id=f"EV-{counter:05d}", employee_id=emp, absence_type="sick_leave",
            start_date="2026-02-02", end_date="2026-03-20", days=35.0,
            status="approved", bucket_id="", note="long sickness spell",
        ))
        counter += 1
    return events


def write_csv(path, fields, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in fields})


def main() -> None:
    os.makedirs(EXPORTS, exist_ok=True)
    rng = random.Random(SEED)
    people = build_people(rng)
    events = build_absences(people, rng)
    write_csv(os.path.join(DATA, "employees.csv"), EMP_FIELDS, people)
    write_csv(os.path.join(DATA, "absences.csv"), ABS_FIELDS, events)

    # Opening balances at the cut-over. Everyone employed before LEDGER_START
    # needs one; three people deliberately do not have one, so the UNKNOWN path
    # is visible in the reconciliation report rather than only in a unit test.
    buckets_of = {k: list(v) for k, v in UTILISATION.items()}
    missing = {"PL-0009", "IN-0005", "US-0004"}
    opening = []
    for p in people:
        if _dt.date.fromisoformat(p["hire_date"]) >= LEDGER_START:
            continue
        if p["employee_id"] in missing:
            continue
        for bucket in buckets_of[p["entity_id"]]:
            opening.append(dict(
                employee_id=p["employee_id"], bucket_id=bucket,
                opening_days=rng.choice([0, 0, 1, 2, 3, 4, 5, 6, 8]),
                as_of=LEDGER_START.isoformat(),
                signed_off_by=f"Country HR Lead ({p['entity_id']})",
            ))
    write_csv(os.path.join(DATA, "opening_balances.csv"),
              ["employee_id", "bucket_id", "opening_days", "as_of", "signed_off_by"], opening)

    # ---- now compute the truth and corrupt it into "current state" exports
    from absence.data import load_absences, load_employees

    from absence.data import load_opening_balances
    engine = AbsenceEngine(
        PolicyRepository(os.path.join(ROOT, "policies")),
        CalendarRepository(os.path.join(ROOT, "policies", "calendars")),
        ledger_start=LEDGER_START,
        opening_balances=load_opening_balances(os.path.join(DATA, "opening_balances.csv")),
    )
    emps = {e.employee_id: e for e in load_employees(os.path.join(DATA, "employees.csv"))}
    evs = load_absences(os.path.join(DATA, "absences.csv"))

    truth = {}
    for emp in emps.values():
        try:
            truth[emp.employee_id] = engine.balance(emp, evs, AS_OF)
        except Exception as exc:                                  # pragma: no cover
            print(f"  ! {emp.employee_id}: {exc}")

    def reported(emp_id, bucket_id, error_rng):
        bal = truth.get(emp_id)
        if bal is None:
            return ""
        b = bal.bucket(bucket_id)
        if b is None or b.remaining is None:
            # The local sheet always has *a* number, even where the engine
            # correctly refuses to produce one. That gap is the finding.
            return round(20 - error_rng.choice([0, 0, 6]), 1)
        value = b.remaining
        roll = error_rng.random()
        if roll < 0.10:
            value -= 6.0            # E1 seniority tier missed (sheet still on 20 days)
        elif roll < 0.20:
            value += b.expired      # E2 expired days still on the sheet
        elif roll < 0.28:
            value -= 3.0            # E4 wrong regional entitlement
        elif roll < 0.55:
            value += error_rng.choice([-0.5, 0.25, 0.5])   # E5 rounding drift
        return max(0.0, round(value, 2))

    err = random.Random(SEED + 1)

    pl_rows = [
        {"Nr pracownika": e, "Dni pozostale": reported(e, "annual_leave", err),
         "Dni zalegle": err.choice([0, 0, 2, 4])}
        for e in sorted(emps) if emps[e].entity_id == "PL-SSC"
    ]
    with open(os.path.join(EXPORTS, "pl_urlop_2026.csv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["Nr pracownika", "Dni pozostale", "Dni zalegle"],
                           delimiter=";")
        w.writeheader()
        w.writerows(pl_rows)

    in_rows = [
        {"Emp Code": e, "State": emps[e].work_region or "",
         "EL Balance": reported(e, "earned_leave", err),
         "CL Balance": reported(e, "casual_leave", err),
         "SL Balance": reported(e, "sick_leave", err)}
        for e in sorted(emps) if emps[e].entity_id == "IN-SSC"
    ]
    write_csv(os.path.join(EXPORTS, "in_leave_tracker_2026.csv"),
              ["Emp Code", "State", "EL Balance", "CL Balance", "SL Balance"], in_rows)

    nl_rows = [
        {"medewerker": e, "wettelijk_saldo": reported(e, "statutory", err),
         "bovenwettelijk_saldo": reported(e, "supplementary", err)}
        for e in sorted(emps) if emps[e].entity_id == "NL-BV"
    ]
    write_csv(os.path.join(EXPORTS, "nl_verlof_2026.csv"),
              ["medewerker", "wettelijk_saldo", "bovenwettelijk_saldo"], nl_rows)

    print(f"employees: {len(people)}   absence events: {len(events)}")
    print(f"exports:   PL {len(pl_rows)}   IN {len(in_rows)}   NL {len(nl_rows)}")


if __name__ == "__main__":
    main()
