"""The record of what was published, as distinct from what was true.

Two different questions get confused with each other:

*   *What was this person's balance in March?* The engine already answers that
    without storing anything. It is deterministic, policy files are versioned by
    effective date, and `--as-of` recomputes any past date under the rules that
    were in force then. History is reconstructed, not remembered.
*   *What did we tell this person in March?* Nothing in a recomputation can
    answer that, and in a dispute it is the question that decides. If HR quoted
    a figure and the rules were corrected afterwards, the employee's claim rests
    on the figure they were given, not on today's recomputation of it.

This module records the second one. A snapshot writes every balance as it stood
when it was published, together with the policy version that produced each one
and a digest of the file, so a later reader can show the record has not moved.

HONEST LIMIT: a CSV in an output directory is a record, not an immutable one -
anyone who can reach the file can rewrite it and recompute the digest. In
production this belongs in append-only storage (object storage with a retention
lock, or an audit table nobody holds UPDATE on) with the digest published
somewhere the same person cannot reach. What is here is the shape of the
record and the discipline of writing one, not the storage guarantee.
"""

from __future__ import annotations

import csv
import datetime as _dt
import hashlib
import json
import os
from typing import Any, Dict, Iterable, List

from .engine import AbsenceEngine
from .model import AbsenceEvent, Employee
from .policy import PolicyRepository

FIELDS = [
    "as_of", "employee_id", "entity_id", "region", "bucket_id", "unit", "status",
    "entitlement", "carried_in", "taken", "scheduled", "expired", "encashed",
    "remaining", "flags", "policy_file", "policy_effective_from",
]


def _digest(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def take(
    policies: PolicyRepository,
    engine: AbsenceEngine,
    employees: List[Employee],
    events: Iterable[AbsenceEvent],
    as_of: _dt.date,
    out_dir: str,
    label: str = "",
) -> Dict[str, Any]:
    events = list(events)
    stamp = _dt.datetime.now().strftime("%Y%m%dT%H%M%S")
    name = f"{as_of.isoformat()}__{stamp}" + (f"__{label}" if label else "")
    snap_dir = os.path.join(out_dir, "snapshots")
    os.makedirs(snap_dir, exist_ok=True)
    csv_path = os.path.join(snap_dir, name + ".csv")

    rows: List[Dict[str, Any]] = []
    policy_versions: Dict[str, str] = {}
    unknown = 0
    for emp in sorted(employees, key=lambda e: e.employee_id):
        try:
            policy = policies.get(emp.entity_id, as_of, emp.work_region)
            balance = engine.balance(emp, events, as_of)
        except Exception:
            # A person whose balance cannot be produced at all is still part of
            # the population: leaving them out would make the record look
            # complete when it is not.
            rows.append({
                "as_of": as_of.isoformat(), "employee_id": emp.employee_id,
                "entity_id": emp.entity_id, "region": emp.work_region or "",
                "bucket_id": "", "unit": "", "status": "not_computable",
                "flags": "NO_APPLICABLE_POLICY", "policy_file": "",
                "policy_effective_from": "",
            })
            continue
        policy_versions[policy.entity_id] = policy.effective_from.isoformat()
        for b in balance.buckets:
            if b.status == "unknown":
                unknown += 1
            rows.append({
                "as_of": as_of.isoformat(),
                "employee_id": emp.employee_id,
                "entity_id": emp.entity_id,
                "region": emp.work_region or "",
                "bucket_id": b.bucket_id,
                "unit": b.unit,
                "status": b.status,
                "entitlement": b.entitlement,
                "carried_in": b.carried_in,
                "taken": b.taken,
                "scheduled": b.scheduled,
                "expired": b.expired,
                "encashed": b.encashed,
                "remaining": b.remaining,
                "flags": ";".join(b.flags),
                "policy_file": policy.source_file,
                "policy_effective_from": policy.effective_from.isoformat(),
            })

    with open(csv_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row.get(k, "") for k in FIELDS})

    manifest = {
        "snapshot": name,
        "label": label,
        "as_of": as_of.isoformat(),
        "taken_at": _dt.datetime.now().isoformat(timespec="seconds"),
        "ledger_start": engine.ledger_start.isoformat() if engine.ledger_start else None,
        "rows": len(rows),
        "people": len({r["employee_id"] for r in rows}),
        "unknown_balances": unknown,
        "policy_versions": policy_versions,
        "file": os.path.basename(csv_path),
        "sha256": _digest(csv_path),
    }
    with open(os.path.join(snap_dir, name + ".json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    # An append-only index, so the set of snapshots is itself a record.
    index = os.path.join(snap_dir, "register.csv")
    new = not os.path.exists(index)
    with open(index, "a", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        if new:
            writer.writerow(["taken_at", "as_of", "label", "people", "rows",
                             "unknown_balances", "file", "sha256"])
        writer.writerow([manifest["taken_at"], manifest["as_of"], label,
                         manifest["people"], manifest["rows"],
                         manifest["unknown_balances"], manifest["file"],
                         manifest["sha256"]])
    manifest["path"] = csv_path
    return manifest


def verify(snap_dir: str) -> List[Dict[str, Any]]:
    """Re-digest every recorded snapshot and report whether it still matches."""
    out: List[Dict[str, Any]] = []
    if not os.path.isdir(snap_dir):
        return out
    for name in sorted(os.listdir(snap_dir)):
        if not name.endswith(".json"):
            continue
        with open(os.path.join(snap_dir, name), "r", encoding="utf-8") as fh:
            manifest = json.load(fh)
        target = os.path.join(snap_dir, manifest.get("file", ""))
        if not os.path.exists(target):
            out.append({"snapshot": manifest.get("snapshot"), "state": "MISSING"})
            continue
        actual = _digest(target)
        out.append({
            "snapshot": manifest.get("snapshot"),
            "as_of": manifest.get("as_of"),
            "rows": manifest.get("rows"),
            "state": "intact" if actual == manifest.get("sha256") else "ALTERED",
        })
    return out
