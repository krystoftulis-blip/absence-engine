"""Ireland's April leave year, California's ban on forfeiture, policy versioning."""

import datetime as dt
import unittest

from support import POLICY_DIR, build_engine, employee, leave   # noqa: I001

from absence.policy import PolicyRepository, apply_override      # noqa: E402


class IrishLeaveYear(unittest.TestCase):
    def setUp(self):
        self.engine = build_engine()

    def test_leave_year_runs_april_to_march(self):
        emp = employee("T1", "IE-INTL", "2024-04-01")
        balance = self.engine.balance(emp, [], dt.date(2026, 2, 10))
        self.assertEqual(balance.leave_year_start, dt.date(2025, 4, 1))
        self.assertEqual(balance.leave_year_end, dt.date(2026, 3, 31))

    def test_a_january_absence_belongs_to_the_leave_year_that_opened_in_april(self):
        emp = employee("T2", "IE-INTL", "2024-04-01")
        events = [leave("T2", "annual_leave", "2026-01-12", 5)]
        balance = self.engine.balance(emp, events, dt.date(2026, 2, 10))
        self.assertEqual(balance.bucket("annual_leave").taken, 5.0)

    def test_accrual_is_eight_percent_of_hours_capped_at_four_weeks(self):
        emp = employee("T3", "IE-INTL", "2024-04-01")
        bucket = self.engine.balance(emp, [], dt.date(2026, 2, 10)).bucket("annual_leave")
        self.assertEqual(bucket.entitlement, 20.0)
        self.assertIn("ACCRUAL_USES_CONTRACTED_HOURS", bucket.flags)


class CaliforniaOverride(unittest.TestCase):
    def setUp(self):
        self.engine = build_engine()

    def _bucket(self, region):
        emp = employee("T4", "US-CORP", "2024-01-01", work_region=region)
        return self.engine.balance(emp, [], dt.date(2026, 9, 1)).bucket("pto")

    def test_illinois_applies_the_cap_and_the_march_deadline(self):
        bucket = self._bucket("IL")
        self.assertGreater(bucket.expired, 0.0)

    def test_california_accrued_vacation_cannot_be_forfeited(self):
        """Accrued vacation is earned wages in California.

        The same national policy therefore has to produce a different lawful
        result by region - which is why expiry is a policy value and not a
        global switch.
        """
        bucket = self._bucket("CA")
        self.assertEqual(bucket.expired, 0.0)
        self.assertGreater(bucket.carried_in, 0.0)


class PolicyVersioning(unittest.TestCase):
    def setUp(self):
        self.repo = PolicyRepository(POLICY_DIR)

    def test_a_policy_before_its_effective_date_is_refused(self):
        with self.assertRaises(Exception):
            self.repo.get("IE-INTL", dt.date(2020, 1, 1))

    def test_dotted_overrides_address_buckets_by_id(self):
        doc = {"buckets": [{"id": "a", "accrual": {"amount": 1}},
                           {"id": "b", "accrual": {"amount": 2}}]}
        apply_override(doc, "buckets.b.accrual.amount", 99)
        self.assertEqual(doc["buckets"][0]["accrual"]["amount"], 1)
        self.assertEqual(doc["buckets"][1]["accrual"]["amount"], 99)

    def test_regions_do_not_leak_between_lookups(self):
        """A region override must not mutate the cached base policy."""
        base = self.repo.get("IN-SSC", dt.date(2026, 6, 1), "MH")
        again = self.repo.get("IN-SSC", dt.date(2026, 6, 1), "KA")
        amount = {b["id"]: b["accrual"].get("amount") for b in again.buckets}
        self.assertEqual(amount["earned_leave"], 18)
        self.assertEqual(
            {b["id"]: b["accrual"].get("amount") for b in base.buckets}["earned_leave"], 21
        )

    def test_every_engine_entity_in_the_registry_has_a_policy_file(self):
        for row in self.repo.registry_entries:
            if row.get("treatment") != "engine":
                continue
            self.assertIn(row["entity_id"], self.repo.entity_ids(),
                          f"{row['entity_id']} is classified as 'engine' but has no policy")


class OpeningBalance(unittest.TestCase):
    def test_service_before_the_cut_over_without_an_opening_balance_is_unknown(self):
        engine = build_engine()
        emp = employee("T5", "PL-SSC", "2019-01-01", service_evidence_on_file=True)
        bucket = engine.balance(emp, [], dt.date(2026, 9, 1)).bucket("annual_leave")
        self.assertEqual(bucket.status, "unknown")
        self.assertIn("OPENING_BALANCE_MISSING", bucket.flags)

    def test_a_signed_off_opening_balance_is_carried_in_not_recomputed(self):
        engine = build_engine(opening={("T6", "annual_leave"): 7.0})
        emp = employee("T6", "PL-SSC", "2019-01-01", service_evidence_on_file=True)
        bucket = engine.balance(emp, [], dt.date(2024, 3, 1)).bucket("annual_leave")
        self.assertEqual(bucket.status, "computed")
        self.assertEqual(bucket.carried_in, 7.0)


if __name__ == "__main__":
    unittest.main()
