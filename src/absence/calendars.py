"""Public holiday calendars, as data.

Holidays are the single most reliable source of annual manual work in a
multi-entity HR function: every calendar has to be rebuilt every year, and in
several countries it is not even a national list (Indian states, German
Bundeslaender, Spanish regions, Swiss cantons each publish their own).

Keeping them as one file per calendar and year means the yearly update is a
reviewable pull request, not a spreadsheet edited in place with no history.
"""

from __future__ import annotations

import datetime as _dt
import os
from typing import Dict, List, Optional, Set

import yaml

CALENDAR_DIR_DEFAULT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "policies",
    "calendars",
)


class CalendarRepository:
    def __init__(self, calendar_dir: str = CALENDAR_DIR_DEFAULT):
        self.calendar_dir = calendar_dir
        self._by_key_year: Dict[str, Dict[_dt.date, str]] = {}
        self._confirmed: Dict[str, bool] = {}
        self._load()

    def _load(self) -> None:
        if not os.path.isdir(self.calendar_dir):
            return
        for name in sorted(os.listdir(self.calendar_dir)):
            if not name.endswith((".yaml", ".yml")):
                continue
            with open(os.path.join(self.calendar_dir, name), "r", encoding="utf-8") as fh:
                doc = yaml.safe_load(fh) or {}
            key = doc.get("calendar")
            year = doc.get("year")
            if not key or not year:
                continue
            entries: Dict[_dt.date, str] = {}
            for item in doc.get("holidays", []) or []:
                raw = item["date"]
                day = raw if isinstance(raw, _dt.date) else _dt.date.fromisoformat(str(raw))
                entries[day] = item.get("name", "")
            self._by_key_year[f"{key}:{year}"] = entries
            self._confirmed[f"{key}:{year}"] = bool(doc.get("confirmed", False))

    def available(self) -> List[str]:
        return sorted(self._by_key_year)

    def has(self, key: str, year: int) -> bool:
        return f"{key}:{year}" in self._by_key_year

    def is_confirmed(self, key: str, year: int) -> bool:
        """A calendar can exist and still not be usable.

        Indian state festival lists are published locally each year; a file that
        only carries the three national holidays is present but incomplete, and
        pretending otherwise would silently under-count holidays for that state.
        """
        return self._confirmed.get(f"{key}:{year}", False)

    def holidays(self, key: Optional[str], year: int) -> Dict[_dt.date, str]:
        if key is None:
            return {}
        return self._by_key_year.get(f"{key}:{year}", {})

    def holiday_dates(self, key: Optional[str], start: _dt.date, end: _dt.date) -> Set[_dt.date]:
        out: Set[_dt.date] = set()
        for year in range(start.year, end.year + 1):
            for day in self.holidays(key, year):
                if start <= day <= end:
                    out.add(day)
        return out

    def years_covered(self, key: str) -> List[int]:
        prefix = f"{key}:"
        return sorted(
            int(k.split(":", 1)[1]) for k in self._by_key_year if k.startswith(prefix)
        )


def working_days_between(
    start: _dt.date,
    end: _dt.date,
    working_days_per_week: float,
    holidays: Set[_dt.date],
) -> float:
    """Working days in a closed interval.

    ASSUMPTION (documented in DECISION.md): the working pattern is Monday to
    Friday, and a part-time employee's pattern is modelled as a fraction of a
    five-day week rather than as named working days. Real payroll data carries
    actual work schedules; this is the first thing to replace with real data
    before any production use, because it changes deductions for part-timers.
    """
    if end < start:
        return 0.0
    count = 0
    cursor = start
    while cursor <= end:
        if cursor.weekday() < 5 and cursor not in holidays:
            count += 1
        cursor += _dt.timedelta(days=1)
    factor = working_days_per_week / 5.0 if working_days_per_week else 1.0
    return round(count * factor, 3)
