"""A single self-contained page for the people who actually use this in phase 0.

Deliberately NOT an application. There is no login, no approval flow and no
employee self-service, because in phase 0 the user is an HR analyst reading a
reconciliation, not an employee booking leave (see DECISION.md section 6 and
CHANGE_PLAN.md section 4). What that person needs is to see the numbers, see
why each number is what it is, and see where the local record disagrees.

It is one HTML file with the data baked in, rather than a web application,
because of who has to open it: a country HR lead on a call, a works council
member, a lawyer reviewing a rule. A file opens from a link on any machine
with no install and no server running on somebody's laptop.

If the page is opened inside a Claude artifact viewer it also lights up an
"ask" panel that puts the calculation trace into plain language. That panel is
optional by construction - the page renders and works identically without it -
and it never computes anything: it reads the trace the engine already produced.
Keeping AI out of the calculation path and on top of the explanation is the
same line DECISION.md section 8 draws.
"""

from __future__ import annotations

import datetime as _dt
import json
import os
from typing import Any, Dict, List

from . import annual_update as annual
from .calendars import CalendarRepository
from .engine import AbsenceEngine
from .model import AbsenceEvent, Employee
from .policy import PolicyRepository
from .reconcile import load_export_specs, reconcile_entity, summarise

TEMPLATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard_template.html")


def build_payload(
    policies: PolicyRepository,
    calendars: CalendarRepository,
    engine: AbsenceEngine,
    employees: List[Employee],
    events: List[AbsenceEvent],
    export_dir: str,
    as_of: _dt.date,
    annual_year: int,
) -> Dict[str, Any]:
    # -- entity registry ----------------------------------------------------
    entities: List[Dict[str, Any]] = []
    totals: Dict[str, List[int]] = {}
    for row in policies.registry_entries:
        treatment = row.get("treatment", "unclassified")
        head = int(row.get("headcount", 0) or 0)
        totals.setdefault(treatment, [0, 0])
        totals[treatment][0] += 1
        totals[treatment][1] += head
        entities.append({
            "id": row.get("entity_id"),
            "name": row.get("legal_entity"),
            "jurisdiction": row.get("jurisdiction"),
            "treatment": treatment,
            "headcount": head,
            "owner": row.get("owner_role", "") or "unassigned",
            "rationale": row.get("rationale", "") or row.get("owner_role", ""),
        })
    everyone = sum(v[1] for v in totals.values()) or 1
    treatments = [
        {"treatment": t, "entities": v[0], "headcount": v[1],
         "share": round(v[1] / everyone * 100, 1)}
        for t, v in sorted(totals.items(), key=lambda kv: -kv[1][1])
    ]

    # -- people and balances ------------------------------------------------
    people: List[Dict[str, Any]] = []
    unknown_count = 0
    for emp in sorted(employees, key=lambda e: e.employee_id):
        try:
            balance = engine.balance(emp, events, as_of)
        except Exception as exc:                                    # pragma: no cover
            people.append({
                "id": emp.employee_id, "entity": emp.entity_id,
                "region": emp.work_region or "", "hired": emp.hire_date.isoformat(),
                "error": str(exc), "buckets": [],
            })
            continue
        buckets = []
        for b in balance.buckets:
            if b.status == "unknown":
                unknown_count += 1
            buckets.append({
                "id": b.bucket_id, "label": b.label, "unit": b.unit, "status": b.status,
                "entitlement": b.entitlement, "carried_in": b.carried_in,
                "taken": b.taken, "scheduled": b.scheduled, "expired": b.expired,
                "encashed": b.encashed, "remaining": b.remaining,
                "flags": list(b.flags), "trace": list(b.trace),
            })
        record = {
            "id": emp.employee_id,
            "entity": emp.entity_id,
            "region": emp.work_region or "",
            "hired": emp.hire_date.isoformat(),
            "leave_year": [balance.leave_year_start.isoformat(),
                           balance.leave_year_end.isoformat()],
            "buckets": buckets,
        }
        sick = engine.sick_pay(emp, events, as_of.year)
        if sick and sick["sick_days_total"]:
            record["sick"] = sick
        people.append(record)

    # -- reconciliation -----------------------------------------------------
    specs = load_export_specs(os.path.join(export_dir, "_mappings.yaml"))
    findings: List[Dict[str, Any]] = []
    recon: List[Dict[str, Any]] = []
    for name, spec in specs.items():
        found = reconcile_entity(engine, employees, events, spec, export_dir, as_of)
        summary = summarise(found)
        recon.append({
            "name": name,
            "entity": spec["entity_id"],
            "file": spec["file"],
            "comparable": summary["comparable"],
            "match_rate": round(summary["match_rate"] * 100),
            "counts": summary["counts"],
            "gross": summary["gross_days_in_dispute"],
            "net": summary["net_days_on_local_sheets"],
            "note": (spec.get("note") or "").strip(),
        })
        for f in found:
            findings.append({
                "entity": f.entity_id, "employee": f.employee_id, "bucket": f.bucket_id,
                "reported": f.reported, "computed": f.computed, "delta": f.delta,
                "severity": f.severity, "cause": f.cause, "flags": list(f.flags),
            })

    # -- annual update ------------------------------------------------------
    items = annual.run(engine, policies, calendars, employees, annual_year)

    return {
        "generated": _dt.date.today().isoformat(),
        "as_of": as_of.isoformat(),
        "ledger_start": engine.ledger_start.isoformat() if engine.ledger_start else None,
        "annual_year": annual_year,
        "summary": {
            "entities": len(entities),
            "engine_entities": totals.get("engine", [0, 0])[0],
            "engine_share": round(totals.get("engine", [0, 0])[1] / everyone * 100),
            "employees": len(people),
            "unknown": unknown_count,
            "findings": len(findings),
            "material": sum(1 for f in findings if f["severity"] == "material"),
        },
        "treatments": treatments,
        "entities": entities,
        "people": people,
        "recon": recon,
        "findings": findings,
        "annual": [i.to_row() for i in items],
    }


SKELETON_OPEN = (
    "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
    "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
)
SKELETON_MID = "</head>\n<body>\n"
SKELETON_CLOSE = "</body>\n</html>\n"


def render(payload: Dict[str, Any], path: str, standalone: bool = True) -> str:
    """Write the page.

    `standalone` wraps the fragment in a document skeleton, which is what a file
    opened straight from disk needs. Hosts that supply their own skeleton (the
    Claude artifact viewer among them) take the fragment instead.
    """
    with open(TEMPLATE, "r", encoding="utf-8") as fh:
        html = fh.read()
    blob = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    # `</script>` inside a JSON string would end the host script tag early.
    blob = blob.replace("</", "<\\/")
    html = html.replace("__PAYLOAD__", blob)
    if standalone:
        head, _, rest = html.partition("</style>")
        html = SKELETON_OPEN + head + "</style>" + SKELETON_MID + rest + SKELETON_CLOSE
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return path
