"""Canonical domain model.

This module is deliberately the *only* place where the shape of an absence
record is defined. Every legal entity feeds the same structures; what differs
between entities lives in `policies/*.yaml`, never here.

That split is the core design decision of this project:
    global engine + global data model, local values.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Dict, List, Optional

# --------------------------------------------------------------------------
# Global absence taxonomy.
#
# Entities are free to *name* things differently in their local systems
# (urlop wypoczynkowy, vakantiedagen, earned leave, PTO). The reconciliation
# layer maps local names onto these. Nothing downstream ever sees a local name.
# --------------------------------------------------------------------------
ABSENCE_TYPES = (
    "annual_leave",
    "sick_leave",
    "public_holiday",
    "parental_leave",
    "unpaid_leave",
    "special_leave",
)

# Status of a balance figure. "unknown" is a first-class outcome, not an error:
# if we cannot compute an entitlement lawfully, we say so rather than guessing.
STATUS_COMPUTED = "computed"
STATUS_UNKNOWN = "unknown"


@dataclass(frozen=True)
class Employee:
    employee_id: str
    entity_id: str
    hire_date: date
    weekly_hours: float
    working_days_per_week: float
    birth_date: Optional[date] = None

    # Sub-national key. Drives policy variants: Indian state, German Bundesland,
    # Spanish región, Swiss canton. One legal entity can span several of these.
    work_region: Optional[str] = None

    # Service that happened before joining Groupon. In several jurisdictions
    # (notably PL) statutory entitlement depends on it, and it cannot be
    # derived from any HR system - it depends on documents the employee submits.
    prior_service_years: float = 0.0
    education_credit_years: float = 0.0
    service_evidence_on_file: bool = False

    # Netherlands: statutory leave only forfeits if the employer demonstrably
    # warned the employee. We track that as data, because the burden of proof
    # sits with the employer.
    expiry_notice_given: bool = False

    termination_date: Optional[date] = None

    def age_at(self, ref: date) -> Optional[int]:
        if self.birth_date is None:
            return None
        years = ref.year - self.birth_date.year
        if (ref.month, ref.day) < (self.birth_date.month, self.birth_date.day):
            years -= 1
        return years

    def is_employed_on(self, ref: date) -> bool:
        if ref < self.hire_date:
            return False
        if self.termination_date is not None and ref > self.termination_date:
            return False
        return True


@dataclass(frozen=True)
class AbsenceEvent:
    event_id: str
    employee_id: str
    absence_type: str
    start_date: date
    end_date: date
    days: float
    status: str = "approved"          # approved | pending | cancelled | rejected
    bucket_id: Optional[str] = None   # which entitlement pot it draws from
    note: str = ""

    @property
    def is_committed(self) -> bool:
        """Approved absence reduces the balance. Pending is shown separately."""
        return self.status == "approved"


@dataclass
class BucketBalance:
    """Balance of one entitlement pot for one employee at one point in time."""

    bucket_id: str
    label: str
    unit: str                          # "days" | "hours"
    status: str = STATUS_COMPUTED
    entitlement: Optional[float] = None
    carried_in: float = 0.0
    taken: float = 0.0
    scheduled: float = 0.0             # approved but in the future
    expired: float = 0.0
    encashed: float = 0.0              # e.g. IN: days above the carry-forward cap
    remaining: Optional[float] = None
    flags: List[str] = field(default_factory=list)
    trace: List[str] = field(default_factory=list)

    def to_row(self) -> Dict[str, Any]:
        return {
            "bucket_id": self.bucket_id,
            "label": self.label,
            "unit": self.unit,
            "status": self.status,
            "entitlement": self.entitlement,
            "carried_in": round(self.carried_in, 3),
            "taken": round(self.taken, 3),
            "scheduled": round(self.scheduled, 3),
            "expired": round(self.expired, 3),
            "encashed": round(self.encashed, 3),
            "remaining": self.remaining,
            "flags": ";".join(self.flags),
        }


@dataclass
class EmployeeBalance:
    employee_id: str
    entity_id: str
    as_of: date
    leave_year_start: date
    leave_year_end: date
    buckets: List[BucketBalance] = field(default_factory=list)

    @property
    def has_unknown(self) -> bool:
        return any(b.status == STATUS_UNKNOWN for b in self.buckets)

    @property
    def all_flags(self) -> List[str]:
        out: List[str] = []
        for b in self.buckets:
            out.extend(b.flags)
        return out

    def bucket(self, bucket_id: str) -> Optional[BucketBalance]:
        for b in self.buckets:
            if b.bucket_id == bucket_id:
                return b
        return None
