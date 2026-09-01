"""Reconciliation: does it actually find the errors it claims to find?"""

import datetime as dt
import os
import tempfile
import unittest

from support import build_engine, employee, leave          # noqa: I001

from absence.reconcile import (                            # noqa: E402
    MATCH, MATERIAL, MINOR, MISSING_IN_EXPORT, MISSING_IN_LEDGER, UNRESOLVED,
    reconcile_entity, summarise,
)

AS_OF = dt.date(2026, 9, 1)

SPEC = {
    "file": "export.csv",
    "entity_id": "PL-SSC",
    "delimiter": ";",
    "employee_column": "Nr pracownika",
    "balances": {"annual_leave": "Dni pozostale"},
    "known_causes": [
        {"delta": -6.0, "bucket": "annual_leave", "cause": "still on the 20-day tier"}
    ],
}


class Reconciliation(unittest.TestCase):
    def setUp(self):
        self.engine = build_engine()
        self.dir = tempfile.mkdtemp()

        # Everyone joined after the cut-over, so balances are fully derivable.
        self.people = [
            employee("A", "PL-SSC", "2025-01-01", service_evidence_on_file=True),
            employee("B", "PL-SSC", "2025-01-01", prior_service_years=4.0,
                     education_credit_years=8.0, service_evidence_on_file=True),
            employee("C", "PL-SSC", "2025-01-01", education_credit_years=8.0,
                     service_evidence_on_file=False),
            employee("D", "PL-SSC", "2025-01-01", service_evidence_on_file=True),
        ]
        self.events = [leave(p.employee_id, "annual_leave", "2025-05-05", 20)
                       for p in self.people]

    def _write(self, rows):
        path = os.path.join(self.dir, "export.csv")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("Nr pracownika;Dni pozostale\n")
            for emp_id, value in rows:
                fh.write(f"{emp_id};{value}\n")
        return path

    def _run(self, rows):
        self._write(rows)
        return reconcile_entity(self.engine, self.people, self.events, SPEC, self.dir, AS_OF)

    def _find(self, findings, emp_id):
        return next(f for f in findings if f.employee_id == emp_id)

    def test_it_finds_the_missed_seniority_tier_and_names_the_cause(self):
        truth = {p.employee_id: self.engine.balance(p, self.events, AS_OF)
                 .bucket("annual_leave").remaining for p in self.people}
        findings = self._run([
            ("A", truth["A"]),                  # correct
            ("B", truth["B"] - 6),              # E1: still on 20 days
            ("C", 20),                          # engine cannot compute this one
            ("D", truth["D"] + 0.25),           # rounding drift
        ])
        self.assertEqual(self._find(findings, "A").severity, MATCH)
        material = self._find(findings, "B")
        self.assertEqual(material.severity, MATERIAL)
        self.assertEqual(material.delta, -6.0)
        self.assertEqual(material.cause, "still on the 20-day tier")
        self.assertEqual(self._find(findings, "C").severity, UNRESOLVED)
        self.assertEqual(self._find(findings, "D").severity, MINOR)

    def test_it_reports_people_the_two_records_do_not_share(self):
        findings = self._run([("A", 6), ("B", 12), ("C", 20), ("ZZ", 5)])
        self.assertEqual(self._find(findings, "D").severity, MISSING_IN_EXPORT)
        self.assertEqual(self._find(findings, "ZZ").severity, MISSING_IN_LEDGER)

    def test_a_wrong_cause_is_not_guessed(self):
        """An unrecognised difference is reported as unexplained, not mislabelled."""
        truth = self.engine.balance(self.people[0], self.events, AS_OF)
        findings = self._run([("A", (truth.bucket("annual_leave").remaining or 0) - 4.0)])
        finding = self._find(findings, "A")
        self.assertEqual(finding.severity, MATERIAL)
        self.assertIn("under-granted", finding.cause)

    def test_summary_counts_only_comparable_records_in_the_match_rate(self):
        truth = {p.employee_id: self.engine.balance(p, self.events, AS_OF)
                 .bucket("annual_leave").remaining for p in self.people}
        findings = self._run([
            ("A", truth["A"]), ("B", truth["B"]), ("C", 20), ("D", truth["D"] - 6),
        ])
        summary = summarise(findings)
        self.assertEqual(summary["comparable"], 3)      # C is not comparable
        self.assertAlmostEqual(summary["match_rate"], 2 / 3)
        self.assertEqual(summary["gross_days_in_dispute"], 6.0)


if __name__ == "__main__":
    unittest.main()
