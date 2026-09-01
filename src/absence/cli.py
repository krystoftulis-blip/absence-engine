"""Command line interface.

    python -m absence registry
    python -m absence balance   --entity PL-SSC [--as-of 2026-09-01]
    python -m absence explain   --employee PL-0001
    python -m absence reconcile [--export pl_urlop] [--html]
    python -m absence annual-update --year 2027
    python -m absence sick-pay  --entity PL-SSC --year 2026
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import sys
from typing import List

from . import annual_update as annual
from . import config as C
from . import report
from .calendars import CalendarRepository
from .data import load_absences, load_employees, load_opening_balances
from .engine import AbsenceEngine
from .policy import PolicyRepository
from .reconcile import (
    SEVERITY_ORDER,
    load_export_specs,
    reconcile_entity,
    summarise,
)


def _build():
    policies = PolicyRepository(C.POLICY_DIR)
    calendars = CalendarRepository(C.CALENDAR_DIR)
    engine = AbsenceEngine(
        policies,
        calendars,
        ledger_start=C.LEDGER_START,
        opening_balances=load_opening_balances(C.OPENING_CSV),
    )
    employees = load_employees(C.EMPLOYEES_CSV)
    events = load_absences(C.ABSENCES_CSV)
    return policies, calendars, engine, employees, events


def _as_of(args) -> _dt.date:
    return _dt.date.fromisoformat(args.as_of) if args.as_of else _dt.date(2026, 9, 1)


# ---------------------------------------------------------------- commands
def cmd_registry(args) -> int:
    policies, *_ = _build()
    rows = []
    totals = {}
    for row in policies.registry_entries:
        treatment = row.get("treatment", "unclassified")
        head = row.get("headcount", 0) or 0
        totals[treatment] = totals.get(treatment, [0, 0])
        totals[treatment][0] += 1
        totals[treatment][1] += head
        rows.append({
            "entity_id": row.get("entity_id"),
            "legal_entity": row.get("legal_entity"),
            "jurisdiction": row.get("jurisdiction"),
            "treatment": treatment,
            "headcount": head,
        })
    print(report.table(rows))
    print()
    everyone = sum(v[1] for v in totals.values()) or 1
    summary = [
        {"treatment": t, "entities": v[0], "headcount": v[1],
         "share_of_people": f"{v[1] / everyone * 100:.1f}%"}
        for t, v in sorted(totals.items(), key=lambda kv: -kv[1][1])
    ]
    print(report.table(summary))
    engine_share = totals.get("engine", [0, 0])[1] / everyone * 100
    print(
        f"\n{totals.get('engine', [0])[0]} of {len(rows)} legal entities are configured "
        f"in the engine, covering {engine_share:.0f}% of employees."
    )
    return 0


def cmd_balance(args) -> int:
    _, _, engine, employees, events = _build()
    as_of = _as_of(args)
    people = [e for e in employees if not args.entity or e.entity_id == args.entity]
    rows = []
    for emp in sorted(people, key=lambda e: e.employee_id):
        balance = engine.balance(emp, events, as_of)
        for bucket in balance.buckets:
            row = {"employee_id": emp.employee_id, "entity_id": emp.entity_id}
            row.update(bucket.to_row())
            row.pop("label", None)
            rows.append(row)
    print(f"Balances as at {as_of.isoformat()}  (ledger opened {C.LEDGER_START.isoformat()})\n")
    print(report.table(rows))
    unknown = sum(1 for r in rows if r["status"] == "unknown")
    print(f"\n{len(rows)} balances, {unknown} reported as unknown rather than guessed.")
    if args.csv:
        path = report.write_csv(os.path.join(C.OUTPUT_DIR, "balances.csv"), rows)
        print(f"written: {path}")
    return 0


def cmd_explain(args) -> int:
    _, _, engine, employees, events = _build()
    as_of = _as_of(args)
    matches = [e for e in employees if e.employee_id == args.employee]
    if not matches:
        print(f"no such employee: {args.employee}", file=sys.stderr)
        return 1
    emp = matches[0]
    balance = engine.balance(emp, events, as_of)
    print(f"{emp.employee_id}  {emp.entity_id}"
          f"{' / ' + emp.work_region if emp.work_region else ''}")
    print(f"hired {emp.hire_date.isoformat()}   leave year "
          f"{balance.leave_year_start.isoformat()} to {balance.leave_year_end.isoformat()}")
    for bucket in balance.buckets:
        print(f"\n  {bucket.label}  [{bucket.bucket_id}]")
        value = "unknown" if bucket.remaining is None else f"{bucket.remaining:g} {bucket.unit}"
        print(f"  remaining: {value}"
              f"   (entitlement {bucket.entitlement}, carried in {bucket.carried_in},"
              f" taken {bucket.taken}, booked ahead {bucket.scheduled},"
              f" lapsed this year {bucket.expired})")
        if bucket.flags:
            print(f"  flags: {', '.join(bucket.flags)}")
        for line in bucket.trace:
            print(f"    - {line}")
    sick = engine.sick_pay(emp, events, as_of.year)
    if sick and sick["sick_days_total"]:
        print(f"\n  sick pay {sick['year']}: {sick['sick_days_total']:g} days total, "
              f"{sick['employer_paid_days']:g} funded by the employer at "
              f"{sick['employer_rate']:.0%} (band: {sick['band']}), "
              f"{sick['transferred_days']:g} transferred to {sick['transferred_to']}")
    return 0


def cmd_reconcile(args) -> int:
    _, _, engine, employees, events = _build()
    as_of = _as_of(args)
    specs = load_export_specs(os.path.join(C.EXPORT_DIR, "_mappings.yaml"))
    chosen = {args.export: specs[args.export]} if args.export else specs
    all_findings: List = []
    for name, spec in chosen.items():
        findings = reconcile_entity(engine, employees, events, spec, C.EXPORT_DIR, as_of)
        summary = summarise(findings)
        all_findings.extend(findings)
        print(f"\n=== {name}  ({spec['entity_id']}, file {spec['file']}) ===")
        counts = ", ".join(
            f"{k}={summary['counts'][k]}" for k in SEVERITY_ORDER if summary["counts"][k]
        )
        print(f"{summary['comparable']} comparable records | "
              f"match rate {summary['match_rate'] * 100:.0f}% | {counts}")
        print(f"gross days in dispute: {summary['gross_days_in_dispute']} | "
              f"net days sitting on local sheets: {summary['net_days_on_local_sheets']:+g}")
        worst = [f for f in findings if f.severity in ("material", "unresolved")]
        worst.sort(key=lambda f: -abs(f.delta or 0))
        if worst:
            print()
            print(report.table([f.to_row() for f in worst[: args.limit]]))
        if args.html:
            path = report.reconciliation_html(
                findings, summary, spec["entity_id"], as_of.isoformat(),
                os.path.join(C.OUTPUT_DIR, f"reconciliation-{spec['entity_id']}.html"),
            )
            print(f"\nwritten: {path}")
    if args.csv and all_findings:
        path = report.write_csv(
            os.path.join(C.OUTPUT_DIR, "reconciliation.csv"),
            [f.to_row() for f in all_findings],
        )
        print(f"written: {path}")
    return 0


def cmd_annual_update(args) -> int:
    policies, calendars, engine, employees, events = _build()
    items = annual.run(engine, policies, calendars, employees, args.year)
    blockers = [i for i in items if i.severity == annual.BLOCKER]
    actions = [i for i in items if i.severity == annual.ACTION]
    print(f"Annual update review for {args.year}\n")
    print(f"{len(blockers)} blocker(s), {len(actions)} action(s). "
          "Nothing has been changed - this is the list to approve.\n")
    print(report.table([i.to_row() for i in items[: args.limit]],
                       ["severity", "area", "entity_id", "subject", "owner"]))
    if blockers:
        print("\nBlockers in full:")
        for item in blockers[:12]:
            print(f"  [{item.entity_id}] {item.subject}\n      {item.detail}"
                  f"\n      owner: {item.owner}")
    if args.csv:
        path = report.write_csv(
            os.path.join(C.OUTPUT_DIR, f"annual-update-{args.year}.csv"),
            [i.to_row() for i in items],
        )
        print(f"\nwritten: {path}")
    return 0


def cmd_sick_pay(args) -> int:
    _, _, engine, employees, events = _build()
    rows = []
    for emp in employees:
        if args.entity and emp.entity_id != args.entity:
            continue
        result = engine.sick_pay(emp, events, args.year)
        if result and result["sick_days_total"]:
            rows.append(result)
    if not rows:
        print("no sickness absence recorded for that entity and year")
        return 0
    print(report.table(rows))
    total = sum(r["employer_paid_days"] for r in rows)
    print(f"\nemployer-funded sick days in {args.year}: {total:g}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="absence", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    # Shared options live on every subcommand, so `absence reconcile --csv`
    # works as well as `absence --csv reconcile`.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--as-of", help="date to compute at (default 2026-09-01)")
    common.add_argument("--csv", action="store_true", help="also write CSV output to out/")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("registry", parents=[common],
                   help="show the entity segmentation and its coverage")

    p = sub.add_parser("balance", parents=[common], help="balances for an entity")
    p.add_argument("--entity")

    p = sub.add_parser("explain", parents=[common],
                       help="show how one person's balance was derived")
    p.add_argument("--employee", required=True)

    p = sub.add_parser("reconcile", parents=[common],
                       help="compare local files against recomputed balances")
    p.add_argument("--export", help="reconcile only this export (see data/entity_exports)")
    p.add_argument("--html", action="store_true", help="write an HTML report to out/")
    p.add_argument("--limit", type=int, default=15)

    p = sub.add_parser("annual-update", parents=[common],
                       help="what has to change for a given year")
    p.add_argument("--year", type=int, required=True)
    p.add_argument("--limit", type=int, default=30)

    p = sub.add_parser("sick-pay", parents=[common],
                       help="employer-funded versus state-funded sick days")
    p.add_argument("--entity")
    p.add_argument("--year", type=int, default=2026)

    args = parser.parse_args(argv)
    handlers = {
        "registry": cmd_registry,
        "balance": cmd_balance,
        "explain": cmd_explain,
        "reconcile": cmd_reconcile,
        "annual-update": cmd_annual_update,
        "sick-pay": cmd_sick_pay,
    }
    return handlers[args.command](args)
