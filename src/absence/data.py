"""Loading the canonical ledger.

In production these two readers are replaced by a connection to whatever the
system of record turns out to be. Everything downstream depends only on the
dataclasses in `model.py`, so swapping the source is a one-file change.
"""

from __future__ import annotations

import csv
import datetime as _dt
import os
from typing import Dict, Iterable, List, Optional, Tuple

from .model import AbsenceEvent, Employee


def _date(value: str) -> Optional[_dt.date]:
    value = (value or "").strip()
    if not value:
        return None
    return _dt.date.fromisoformat(value)


def _bool(value: str) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y", "tak", "ja"}


def _float(value: str, default: float = 0.0) -> float:
    value = (value or "").strip().replace(",", ".")
    return float(value) if value else default


def load_employees(path: str) -> List[Employee]:
    out: List[Employee] = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            out.append(
                Employee(
                    employee_id=row["employee_id"].strip(),
                    entity_id=row["entity_id"].strip(),
                    hire_date=_date(row["hire_date"]),
                    weekly_hours=_float(row.get("weekly_hours"), 40.0),
                    working_days_per_week=_float(row.get("working_days_per_week"), 5.0),
                    birth_date=_date(row.get("birth_date", "")),
                    work_region=(row.get("work_region") or "").strip() or None,
                    prior_service_years=_float(row.get("prior_service_years")),
                    education_credit_years=_float(row.get("education_credit_years")),
                    service_evidence_on_file=_bool(row.get("service_evidence_on_file", "")),
                    expiry_notice_given=_bool(row.get("expiry_notice_given", "")),
                    termination_date=_date(row.get("termination_date", "")),
                )
            )
    return out


def load_absences(path: str) -> List[AbsenceEvent]:
    out: List[AbsenceEvent] = []
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            out.append(
                AbsenceEvent(
                    event_id=row["event_id"].strip(),
                    employee_id=row["employee_id"].strip(),
                    absence_type=row["absence_type"].strip(),
                    start_date=_date(row["start_date"]),
                    end_date=_date(row["end_date"]),
                    days=_float(row["days"]),
                    status=(row.get("status") or "approved").strip(),
                    bucket_id=(row.get("bucket_id") or "").strip() or None,
                    note=(row.get("note") or "").strip(),
                )
            )
    return out


def load_opening_balances(path: str) -> Dict[Tuple[str, str], float]:
    """Signed-off balances at the ledger cut-over.

    A missing row is not the same as a zero balance, and the engine treats it
    that way: it reports UNKNOWN rather than assuming the employee starts from
    nothing.
    """
    out: Dict[Tuple[str, str], float] = {}
    if not os.path.exists(path):
        return out
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            out[(row["employee_id"].strip(), row["bucket_id"].strip())] = _float(
                row["opening_days"]
            )
    return out


def index_by_employee(events: Iterable[AbsenceEvent]) -> Dict[str, List[AbsenceEvent]]:
    out: Dict[str, List[AbsenceEvent]] = {}
    for ev in events:
        out.setdefault(ev.employee_id, []).append(ev)
    return out
