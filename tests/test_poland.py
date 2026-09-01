"""Poland: seniority tiers, the refusal to guess, and age-banded sick pay."""

import datetime as dt
import unittest

from support import build_engine, employee, leave


class PolandEntitlement(unittest.TestCase):
    def setUp(self):
        self.engine = build_engine()
        self.as_of = dt.date(2026, 9, 1)

    def test_under_ten_years_gets_twenty_days(self):
        emp = employee("T1", "PL-SSC", "2024-01-01", service_evidence_on_file=True)
        bucket = self.engine.balance(emp, [], self.as_of).bucket("annual_leave")
        self.assertEqual(bucket.entitlement, 20.0)

    def test_education_counts_towards_the_ten_year_threshold(self):
        """A master's degree plus four years elsewhere clears 10 years on day one.

        This is the single most expensive mistake in Polish absence
        administration: the employee looks junior in the HR system and is owed
        six more days a year than the system would suggest.
        """
        emp = employee(
            "T2", "PL-SSC", "2024-01-01",
            prior_service_years=4.0, education_credit_years=8.0,
            service_evidence_on_file=True,
        )
        bucket = self.engine.balance(emp, [], self.as_of).bucket("annual_leave")
        self.assertEqual(bucket.entitlement, 26.0)

    def test_without_evidence_the_balance_is_unknown_not_twenty(self):
        emp = employee(
            "T3", "PL-SSC", "2024-01-01",
            prior_service_years=4.0, education_credit_years=8.0,
            service_evidence_on_file=False,
        )
        bucket = self.engine.balance(emp, [], self.as_of).bucket("annual_leave")
        self.assertEqual(bucket.status, "unknown")
        self.assertIsNone(bucket.remaining)
        self.assertIn("SERVICE_EVIDENCE_MISSING", bucket.flags)

    def test_upcoming_tier_change_is_flagged_before_it_happens(self):
        # 8 years of credited education, hired September 2024: statutory service
        # is 9.75 years on 1 June 2026 but passes 10 before the leave year ends.
        emp = employee(
            "T4", "PL-SSC", "2024-09-01",
            education_credit_years=8.0, service_evidence_on_file=True,
        )
        bucket = self.engine.balance(emp, [], dt.date(2026, 6, 1)).bucket("annual_leave")
        self.assertEqual(bucket.entitlement, 20.0)
        self.assertIn("TIER_UPGRADE_DURING_LEAVE_YEAR", bucket.flags)

    def test_partial_first_year_is_prorated_and_rounded_up(self):
        # Polish law rounds a partial day of entitlement up to a full day.
        emp = employee("T5", "PL-SSC", "2026-07-01", service_evidence_on_file=True)
        bucket = self.engine.balance(emp, [], self.as_of).bucket("annual_leave")
        self.assertEqual(bucket.entitlement, 11.0)   # 20 * ~184/365 = 10.08 -> 11
        self.assertIn("PRORATED", bucket.flags)


class PolandExpiry(unittest.TestCase):
    def setUp(self):
        self.engine = build_engine()

    def _bucket(self, as_of):
        emp = employee("T6", "PL-SSC", "2025-01-01", service_evidence_on_file=True)
        events = [leave("T6", "annual_leave", "2025-03-03", 10)]
        return self.engine.balance(emp, events, as_of).bucket("annual_leave")

    def test_carryover_survives_until_30_september(self):
        bucket = self._bucket(dt.date(2026, 9, 29))
        self.assertEqual(bucket.carried_in, 10.0)
        self.assertEqual(bucket.expired, 0.0)

    def test_carryover_lapses_after_30_september(self):
        bucket = self._bucket(dt.date(2026, 10, 1))
        self.assertEqual(bucket.carried_in, 0.0)
        self.assertEqual(bucket.expired, 10.0)
        self.assertEqual(bucket.remaining, 20.0)


class PolandSickPay(unittest.TestCase):
    def setUp(self):
        self.engine = build_engine()

    def _split(self, birth_date):
        emp = employee("T7", "PL-SSC", "2020-01-01", birth_date=dt.date.fromisoformat(birth_date),
                       service_evidence_on_file=True)
        events = [leave("T7", "", "2026-02-02", 40, absence_type="sick_leave")]
        return self.engine.sick_pay(emp, events, 2026)

    def test_under_fifty_employer_funds_33_days(self):
        result = self._split("1990-01-01")
        self.assertEqual(result["employer_paid_days"], 33.0)
        self.assertEqual(result["transferred_days"], 7.0)

    def test_fifty_or_over_employer_funds_only_14_days(self):
        result = self._split("1970-01-01")
        self.assertEqual(result["employer_paid_days"], 14.0)
        self.assertEqual(result["transferred_days"], 26.0)


if __name__ == "__main__":
    unittest.main()
