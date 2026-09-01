"""Output. Plain text for the terminal, CSV for analysis, HTML for circulation."""

from __future__ import annotations

import csv
import html
import os
from typing import Any, Dict, Iterable, List, Optional


def table(rows: List[Dict[str, Any]], columns: Optional[List[str]] = None) -> str:
    if not rows:
        return "(nothing to show)"
    columns = columns or list(rows[0])
    widths = {c: len(c) for c in columns}
    text_rows = []
    for row in rows:
        cells = {c: ("" if row.get(c) is None else str(row.get(c))) for c in columns}
        for c in columns:
            widths[c] = max(widths[c], len(cells[c]))
        text_rows.append(cells)
    widths = {c: min(w, 58) for c, w in widths.items()}
    head = "  ".join(c.ljust(widths[c])[: widths[c]] for c in columns)
    rule = "  ".join("-" * widths[c] for c in columns)
    body = [
        "  ".join(r[c].ljust(widths[c])[: widths[c]] for c in columns) for r in text_rows
    ]
    return "\n".join([head, rule] + body)


def write_csv(path: str, rows: Iterable[Dict[str, Any]], columns: Optional[List[str]] = None) -> str:
    rows = list(rows)
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    columns = columns or (list(rows[0]) if rows else [])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return path


_CSS = """
:root{--fg:#16181d;--muted:#666e7a;--line:#e3e6ea;--bg:#fff;--warn:#8a4b00;--bad:#8a1f1f}
*{box-sizing:border-box}
body{margin:0;font:14px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;color:var(--fg);background:var(--bg)}
.wrap{max-width:1100px;margin:0 auto;padding:40px 24px 80px}
h1{font-size:22px;margin:0 0 4px}
.sub{color:var(--muted);margin:0 0 28px}
.cards{display:flex;flex-wrap:wrap;gap:12px;margin:0 0 28px}
.card{border:1px solid var(--line);border-radius:8px;padding:12px 16px;min-width:150px}
.card .n{font-size:22px;font-weight:600}
.card .l{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.04em}
table{border-collapse:collapse;width:100%;font-size:13px}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:600;color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.04em}
td.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
tr.material td{background:#fff7f7}
tr.unresolved td{background:#fffbf2}
.sev{font-size:11px;padding:2px 7px;border-radius:999px;border:1px solid var(--line);white-space:nowrap}
.sev.material{color:var(--bad);border-color:#e8c4c4}
.sev.unresolved{color:var(--warn);border-color:#e8d8c0}
.note{color:var(--muted);max-width:46ch}
footer{margin-top:32px;color:var(--muted);font-size:12px;border-top:1px solid var(--line);padding-top:16px}
"""


def reconciliation_html(
    findings: List[Any], summary: Dict[str, Any], title: str, as_of: str, path: str
) -> str:
    def esc(v: Any) -> str:
        return html.escape("" if v is None else str(v))

    cards = [
        ("records compared", summary["comparable"]),
        ("match rate", f"{summary['match_rate'] * 100:.0f}%"),
        ("material differences", summary["counts"].get("material", 0)),
        ("cannot be computed", summary["counts"].get("unresolved", 0)),
        ("days in dispute", summary["gross_days_in_dispute"]),
    ]
    card_html = "".join(
        f'<div class="card"><div class="n">{esc(v)}</div><div class="l">{esc(k)}</div></div>'
        for k, v in cards
    )

    ranked = sorted(
        findings,
        key=lambda f: (
            {"material": 0, "unresolved": 1, "missing_in_ledger": 2,
             "missing_in_export": 3, "minor": 4, "match": 5}.get(f.severity, 9),
            -abs(f.delta or 0),
        ),
    )
    body = []
    for f in ranked:
        if f.severity == "match":
            continue
        cls = f.severity if f.severity in ("material", "unresolved") else ""
        body.append(
            f'<tr class="{cls}"><td>{esc(f.employee_id)}</td><td>{esc(f.bucket_id)}</td>'
            f'<td class="num">{esc("" if f.reported is None else round(f.reported, 2))}</td>'
            f'<td class="num">{esc("" if f.computed is None else round(f.computed, 2))}</td>'
            f'<td class="num">{esc("" if f.delta is None else round(f.delta, 2))}</td>'
            f'<td><span class="sev {cls}">{esc(f.severity)}</span></td>'
            f'<td class="note">{esc(f.cause)}</td>'
            f'<td class="note">{esc(", ".join(f.flags))}</td></tr>'
        )

    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Absence reconciliation - {esc(title)}</title><style>{_CSS}</style></head>
<body><div class="wrap">
<h1>Absence reconciliation - {esc(title)}</h1>
<p class="sub">Local record compared against the recomputed balance as at {esc(as_of)}.
Matching rows are omitted. Synthetic data.</p>
<div class="cards">{card_html}</div>
<table><thead><tr>
<th>employee</th><th>pot</th><th>local sheet</th><th>recomputed</th><th>delta</th>
<th>severity</th><th>likely cause</th><th>flags</th>
</tr></thead><tbody>
{''.join(body) or '<tr><td colspan="8">No differences.</td></tr>'}
</tbody></table>
<footer>Delta is the local figure minus the recomputed figure. A negative delta means the
entity is under-granting. Rows marked <em>unresolved</em> are cases where the engine
refuses to produce a number because the underlying record is incomplete - those are not
errors in the calculation, they are gaps in the evidence.</footer>
</div></body></html>"""
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return path
