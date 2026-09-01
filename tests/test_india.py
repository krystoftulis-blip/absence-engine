"""India: one legal entity, four statutory regimes, three separate pots."""

import datetime as dt
import unittest

from support import build_engine, employee, leave     # noqa: I001  (puts src/ on the path)

from absence.policy import PolicyError                # noqa: E402


class RegionalEntitlement(unittest.TestCase):
    def setUp(self):
        self.engine = build_engine()
        self.as_of = dt.date(2026, 9, 1)

    def _earned(self, region):
        emp = employee("T1", "IN-SSC", "2024-01-01", work_region=region)
        return self.engine.balance(emp, [], self.as_of).bucket("earned_leave").entitlement

    def test_each_state_has_its_own_entitlement(self):
        self.assertEqual(self._earned("KA"), 18.0)
        self.assertEqual(self._earned("MH"), 21.0)
        self.assertEqual(self._earned("DL"), 15.0)
        self.assertEqual(self._earned("TN"), 12.0)

    def test_computing_without_a_state_is_refused(self):
        """Silently defaulting to one state's rules is the failure this prevents."""
        emp = employee("T2", "IN-SSC", "2024-01-01")
        with self.assertRaises(PolicyError) as ctx:
            self.engine.balance(emp, [], self.as_of)
        self.assertIn("work_region", str(ctx.exception))

    def test_an_unknown_state_is_refused_rather_than_approximated(self):
        emp = employee("T3", "IN-SSC", "2024-01-01", work_region="GJ")
        with self.assertRaises(PolicyError):
            self.engine.balance(emp, [], self.as_of)


class SeparatePots(unittest.TestCase):
    def setUp(self):
        self.engine = build_engine()
        self.as_of = dt.date(2026, 9, 1)

    def test_casual_leave_does_not_carry_over(self):
        emp = employee("T4", "IN-SSC", "2025-01-01", work_region="KA")
        bucket = self.engine.balance(emp, [], self.as_of).bucket("casual_leave")
        self.assertEqual(bucket.carried_in, 0.0)
        self.assertEqual(bucket.expired, 12.0)      # the whole 2025 quota lapsed
        self.assertEqual(bucket.remaining, 12.0)

    def test_earned_leave_above_the_cap_becomes_payable_not_forfeited(self):
        """Statutory encashment. Treating the excess as forfeited would be unlawful."""
        emp = employee("T5", "IN-SSC", "2024-01-01", work_region="MH")
        bucket = self.engine.balance(emp, [], self.as_of).bucket("earned_leave")
        # 21 + 21 = 42 accrued by the start of 2026, capped at 30.
        self.assertEqual(bucket.encashed, 12.0)
        self.assertEqual(bucket.expired, 0.0)
        self.assertEqual(bucket.remaining, 51.0)    # 30 carried + 21 for 2026

    def test_sick_leave_is_not_annual_leave(self):
        emp = employee("T6", "IN-SSC", "2025-01-01", work_region="TN")
        events = [leave("T6", "sick_leave", "2026-02-02", 4, absence_type="sick_leave")]
        balance = self.engine.balance(emp, events, self.as_of)
        self.assertEqual(balance.bucket("sick_leave").taken, 4.0)
        self.assertEqual(balance.bucket("earned_leave").taken, 0.0)


if __name__ == "__main__":
    unittest.main()
