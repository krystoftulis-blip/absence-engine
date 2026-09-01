"""Netherlands: two pots, two clocks, and forfeiture the employer has to earn."""

import datetime as dt
import unittest

from support import build_engine, employee, leave


class DutchAccrual(unittest.TestCase):
    def setUp(self):
        self.engine = build_engine()

    def test_statutory_entitlement_is_four_times_the_working_week(self):
        full = employee("T1", "NL-BV", "2024-01-01", expiry_notice_given=True)
        part = employee("T2", "NL-BV", "2024-01-01", weekly_hours=24.0,
                        working_days_per_week=3.0, expiry_notice_given=True)
        as_of = dt.date(2026, 9, 1)
        self.assertEqual(
            self.engine.balance(full, [], as_of).bucket("statutory").entitlement, 20.0
        )
        # A three-day week earns twelve statutory days, not twenty pro-rated by
        # hours - the formula is the entitlement, not an approximation of it.
        self.assertEqual(
            self.engine.balance(part, [], as_of).bucket("statutory").entitlement, 12.0
        )


class DutchExpiry(unittest.TestCase):
    def setUp(self):
        self.engine = build_engine()

    def _balance(self, notice_given, as_of):
        emp = employee("T3", "NL-BV", "2024-01-01", expiry_notice_given=notice_given)
        events = [
            leave("T3", "statutory", "2024-03-04", 5),
            leave("T3", "statutory", "2025-03-03", 20),
            leave("T3", "supplementary", "2025-06-02", 5),
        ]
        return self.engine.balance(emp, events, as_of)

    def test_statutory_days_lapse_six_months_after_the_year_they_accrued(self):
        # 15 days left from 2024 lapse on 1 July 2025, so by 2026 they are gone.
        bucket = self._balance(True, dt.date(2026, 9, 1)).bucket("statutory")
        self.assertEqual(bucket.carried_in, 0.0)

    def test_without_notice_the_forfeiture_is_not_enforceable(self):
        """Dutch statutory days only lapse if the employer warned the employee.

        The employer carries the burden of proof, so 'no record of a warning'
        has to mean 'the days survive', not 'the days lapsed'. Writing them off
        silently creates a liability that surfaces at termination.
        """
        bucket = self._balance(False, dt.date(2026, 9, 1)).bucket("statutory")
        self.assertIn("EXPIRY_NOT_ENFORCEABLE", bucket.flags)
        self.assertEqual(bucket.carried_in, 15.0)
        self.assertEqual(bucket.expired, 0.0)

    def test_supplementary_days_run_on_a_five_year_clock(self):
        bucket = self._balance(True, dt.date(2026, 9, 1)).bucket("supplementary")
        self.assertEqual(bucket.expired, 0.0)
        self.assertEqual(bucket.remaining, 10.0)     # 5 + 5 + 5 accrued, 5 taken

    def test_the_two_pots_are_reported_separately(self):
        balance = self._balance(True, dt.date(2026, 9, 1))
        self.assertEqual({b.bucket_id for b in balance.buckets},
                         {"statutory", "supplementary"})


if __name__ == "__main__":
    unittest.main()
