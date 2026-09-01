"""Shared test fixtures.

Importing this module puts `src/` on the path, so the suite runs with
`python -m unittest discover -s tests` from the repository root without any
packaging or installation step.
"""

import datetime as dt
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.path.join(ROOT, "src") not in sys.path:
    sys.path.insert(0, os.path.join(ROOT, "src"))

from absence.calendars import CalendarRepository       # noqa: E402
from absence.engine import AbsenceEngine               # noqa: E402
from absence.model import AbsenceEvent, Employee       # noqa: E402
from absence.policy import PolicyRepository            # noqa: E402

POLICY_DIR = os.path.join(ROOT, "policies")
CALENDAR_DIR = os.path.join(POLICY_DIR, "calendars")
LEDGER_START = dt.date(2024, 1, 1)


def build_engine(opening=None, ledger_start=LEDGER_START):
    return AbsenceEngine(
        PolicyRepository(POLICY_DIR),
        CalendarRepository(CALENDAR_DIR),
        ledger_start=ledger_start,
        opening_balances=opening or {},
    )


def employee(employee_id, entity_id, hire_date, **kw):
    kw.setdefault("weekly_hours", 40.0)
    kw.setdefault("working_days_per_week", 5.0)
    return Employee(
        employee_id=employee_id,
        entity_id=entity_id,
        hire_date=dt.date.fromisoformat(hire_date),
        **kw,
    )


def leave(employee_id, bucket_id, start, days, absence_type="annual_leave", status="approved"):
    start_date = dt.date.fromisoformat(start)
    return AbsenceEvent(
        event_id=f"T-{employee_id}-{start}-{bucket_id}",
        employee_id=employee_id,
        absence_type=absence_type,
        start_date=start_date,
        end_date=start_date + dt.timedelta(days=int(days) - 1),
        days=float(days),
        status=status,
        bucket_id=bucket_id,
    )
