"""Deployment-level settings that are not legal rules.

Kept apart from `policies/` on purpose: everything in there needs a lawyer's
signature, everything in here does not.
"""

from __future__ import annotations

import datetime as _dt
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

POLICY_DIR = os.path.join(ROOT, "policies")
CALENDAR_DIR = os.path.join(POLICY_DIR, "calendars")
DATA_DIR = os.path.join(ROOT, "data")
EXPORT_DIR = os.path.join(DATA_DIR, "entity_exports")
OUTPUT_DIR = os.path.join(ROOT, "out")

EMPLOYEES_CSV = os.path.join(DATA_DIR, "employees.csv")
ABSENCES_CSV = os.path.join(DATA_DIR, "absences.csv")
OPENING_CSV = os.path.join(DATA_DIR, "opening_balances.csv")

# Cut-over date. Absence history before this date is not recomputed; the
# opening balance is taken as signed off by the entity. Moving this date
# backwards is only meaningful if the underlying event history actually exists.
LEDGER_START = _dt.date(2024, 1, 1)

# Materiality threshold for the reconciliation report, in days. Differences at
# or below this are reported but not escalated - they are almost always
# rounding conventions, not errors.
MATERIALITY_DAYS = 0.5
