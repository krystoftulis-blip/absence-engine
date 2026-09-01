"""Reconciliation: the part that can be deployed on a Monday.

The engine on its own is a proposal. Reconciliation is what makes it useful
before anything is migrated: it takes each entity's current file - in whatever
shape that entity keeps it - recomputes the same population from the canonical
ledger and the entity's own policy, and reports where the two disagree.

That ordering matters. A migration that starts by moving balances into a new
system moves the errors with them, and the new system gets blamed for numbers
it inherited. Running the recomputation *alongside* the current process for a
few cycles surfaces the errors while the old process is still the record, which
is the only point at which they are cheap to fix.
"""

from __future__ import annotations

import csv
import datetime as _dt
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import yaml

from .config import MATERIALITY_DAYS
from .engine import AbsenceEngine
from .model import AbsenceEvent, Employee

MATCH = "match"
MINOR = "minor"
MATERIAL = "material"
UNRESOLVED = "unresolved"
MISSING_IN_EXPORT = "missing_in_export"
MISSING_IN_LEDGER = "missing_in_ledger"

SEVERITY_ORDER = [MATERIAL, UNRESOLVED, MISSING_IN_LEDGER, MISSING_IN_EXPORT, MINOR, MATCH]


@dataclass
class Finding:
    entity_id: str
    employee_id: str
    bucket_id: str
    reported: Optional[float]
    computed: Optional[float]
    delta: Optional[float]
    severity: str
    cause: str
    flags: List[str] = field(default_factory=list)

    def to_row(self) -> Dict[str, Any]:
        return {
            "entity_id": self.entity_id,
            "employee_id": self.employee_id,
            "bucket_id": self.bucket_id,
            "reported": "" if self.reported is None else round(self.reported, 2),
            "computed": "" if self.computed is None else round(self.computed, 2),
            "delta": "" if self.delta is None else round(self.delta, 2),
            "severity": self.severity,
            "likely_cause": self.cause,
            "flags": ";".join(self.flags),
        }


def load_export_specs(path: str) -> Dict[str, Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as fh:
        doc = yaml.safe_load(fh) or {}
    return doc.get("exports", {})


def read_export(spec: Dict[str, Any], base_dir: str) -> Dict[str, Dict[str, str]]:
    path = os.path.join(base_dir, spec["file"])
    delimiter = spec.get("delimiter", ",")
    key = spec["employee_column"]
    rows: Dict[str, Dict[str, str]] = {}
    with open(path, newline="", encoding=spec.get("encoding", "utf-8")) as fh:
        for row in csv.DictReader(fh, delimiter=delimiter):
            rows[(row[key] or "").strip()] = row
    return rows


def _number(raw: Optional[str]) -> Optional[float]:
    if raw is None:
        return None
    raw = raw.strip().replace(",", ".")
    if not raw:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


def classify(
    delta: float,
    computed_bucket,
    employee: Employee,
    spec: Dict[str, Any],
    bucket_id: str = "",
) -> str:
    """Name the most likely cause instead of only reporting a number.

    An HR administrator cannot act on "delta -6.0". They can act on "this
    person is probably still on the 20-day tier". The rules below are explicit
    and few on purpose: a wrong guess is worse than none, so anything that does
    not match a known pattern is reported as unexplained and goes to a human.
    """
    tolerance = 0.35
    expired = getattr(computed_bucket, "expired", 0.0) or 0.0

    for pattern in spec.get("known_causes", []):
        # A named cause only applies to the pot and the region it was written
        # for. Attaching "wrong Indian state" to a Karnataka employee's sick
        # leave would be a confident wrong answer, which is worse than none.
        if pattern.get("bucket") and pattern["bucket"] != bucket_id:
            continue
        if pattern.get("when_region") and pattern["when_region"] != (employee.work_region or ""):
            continue
        if abs(delta - float(pattern["delta"])) <= tolerance:
            return pattern["cause"]

    if expired and abs(delta - expired) <= tolerance:
        return (
            f"local sheet still shows {expired:g} day(s) that have already lapsed "
            "under the entity's expiry rule"
        )
    if "EXPIRY_NOT_ENFORCEABLE" in getattr(computed_bucket, "flags", []) and delta < 0:
        return (
            "days written off locally, but the statutory forfeiture is not "
            "enforceable without evidence the employee was warned"
        )
    if delta < 0:
        return "local sheet is lower than the recomputed entitlement - under-granted"
    return "local sheet is higher than the recomputed entitlement - over-granted"


def reconcile_entity(
    engine: AbsenceEngine,
    employees: List[Employee],
    events: List[AbsenceEvent],
    spec: Dict[str, Any],
    export_dir: str,
    as_of: _dt.date,
) -> List[Finding]:
    entity_id = spec["entity_id"]
    rows = read_export(spec, export_dir)
    population = [e for e in employees if e.entity_id == entity_id]
    findings: List[Finding] = []
    seen = set()

    for emp in population:
        row = rows.get(emp.employee_id)
        if row is None:
            findings.append(
                Finding(entity_id, emp.employee_id, "-", None, None, None,
                        MISSING_IN_EXPORT,
                        "on the payroll ledger but absent from the entity's own file")
            )
            continue
        seen.add(emp.employee_id)
        balance = engine.balance(emp, events, as_of)
        for bucket_id, column in spec["balances"].items():
            bucket = balance.bucket(bucket_id)
            reported = _number(row.get(column))
            if bucket is None:
                continue
            computed = bucket.remaining
            if computed is None:
                findings.append(
                    Finding(entity_id, emp.employee_id, bucket_id, reported, None, None,
                            UNRESOLVED,
                            "the entity reports a number the engine cannot lawfully "
                            "reproduce - the underlying record is incomplete",
                            list(bucket.flags))
                )
                continue
            if reported is None:
                findings.append(
                    Finding(entity_id, emp.employee_id, bucket_id, None, computed, None,
                            MISSING_IN_EXPORT, "no value in the entity's file for this pot",
                            list(bucket.flags))
                )
                continue
            delta = reported - computed
            if abs(delta) < 1e-9:
                severity, cause = MATCH, ""
            elif abs(delta) <= MATERIALITY_DAYS:
                severity, cause = MINOR, "rounding or half-day convention"
            else:
                severity = MATERIAL
                cause = classify(delta, bucket, emp, spec, bucket_id)
            findings.append(
                Finding(entity_id, emp.employee_id, bucket_id, reported, computed,
                        delta, severity, cause, list(bucket.flags))
            )

    for emp_id in rows:
        if emp_id and emp_id not in seen and not any(
            e.employee_id == emp_id for e in population
        ):
            findings.append(
                Finding(entity_id, emp_id, "-", None, None, None, MISSING_IN_LEDGER,
                        "appears in the entity's file but not on the payroll ledger")
            )
    return findings


def summarise(findings: List[Finding]) -> Dict[str, Any]:
    counts = {key: 0 for key in SEVERITY_ORDER}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    material = [f for f in findings if f.severity == MATERIAL]
    comparable = [f for f in findings if f.severity in (MATCH, MINOR, MATERIAL)]
    gross = sum(abs(f.delta or 0.0) for f in material)
    net = sum((f.delta or 0.0) for f in material)
    return {
        "records": len(findings),
        "comparable": len(comparable),
        "counts": counts,
        "match_rate": (counts[MATCH] + counts[MINOR]) / len(comparable) if comparable else 0.0,
        "gross_days_in_dispute": round(gross, 2),
        "net_days_on_local_sheets": round(net, 2),
    }
