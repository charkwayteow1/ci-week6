import unittest

from duckfine import DuckFine


class TestDuckFine(unittest.TestCase):
    def setUp(self):
        self.duck_fine = DuckFine("member-123")

    def test_stores_member_id(self):
        self.assertEqual(self.duck_fine.member_id, "member-123")

    def test_starts_with_no_amount_owed(self):
        self.assertEqual(self.duck_fine.total_owed, 0.0)

    def test_no_fee_when_returned_on_time(self):
        self.assertEqual(self.duck_fine.charge(0), 0.0)

    def test_no_fee_on_last_grace_day(self):
        self.assertEqual(self.duck_fine.charge(2), 0.0)

    def test_charges_for_days_after_grace_period(self):
        self.assertEqual(self.duck_fine.charge(4), 1.0)

    def test_deluxe_doubles_the_fee(self):
        self.assertEqual(self.duck_fine.charge(4, deluxe=True), 2.0)

    def test_caps_a_single_fee(self):
        self.assertEqual(self.duck_fine.charge(20), 5.0)

    def test_caps_a_deluxe_fee(self):
        self.assertEqual(self.duck_fine.charge(10, deluxe=True), 5.0)

    def test_rejects_negative_days_late(self):
        with self.assertRaisesRegex(ValueError, "days_late must not be negative"):
            self.duck_fine.charge(-1)

    def test_adds_fees_to_total_owed(self):
        self.duck_fine.charge(3)
        self.duck_fine.charge(4)

        self.assertEqual(self.duck_fine.total_owed, 1.5)


if __name__ == "__main__":
    unittest.main()
