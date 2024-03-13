import unittest
from datetime import datetime, timedelta
from src.fetch_data import (
    calculate_date_from_delta,
)  # Ensure to import your function correctly


class TestCalculateDateFromDelta(unittest.TestCase):

    def test_with_start_date(self):
        # Test the function with a specific start date
        start_date = datetime(2022, 1, 10)
        expected_date = "2022-01-05"
        result = calculate_date_from_delta(5, start_date)
        self.assertEqual(result, expected_date)

    def test_without_start_date(self):
        # Test the function without specifying a start date (uses today's date)
        n_days = 5
        today = datetime.now()
        expected_date = (today - timedelta(days=n_days)).strftime("%Y-%m-%d")
        result = calculate_date_from_delta(n_days)
        self.assertEqual(result, expected_date)

    def test_negative_days(self):
        # Test the function with a negative value for n_days (future date)
        start_date = datetime(2022, 1, 10)
        expected_date = "2022-01-15"
        result = calculate_date_from_delta(-5, start_date)
        self.assertEqual(result, expected_date)


if __name__ == "__main__":
    unittest.main()
