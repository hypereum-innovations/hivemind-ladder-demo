import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from approvals.retention import WorkingRecord, sweep  # noqa: E402


class RetentionTest(unittest.TestCase):
    def test_removes_only_records_older_than_the_limit(self):
        now = datetime(2026, 9, 15, tzinfo=timezone.utc)
        records = [
            WorkingRecord("fresh", now - timedelta(days=2)),
            WorkingRecord("old", now - timedelta(days=40)),
        ]
        kept, removed = sweep(records, max_age_days=30, now=now)
        self.assertEqual([r.key for r in kept], ["fresh"])
        self.assertEqual(removed, ["old"])

    def test_rejects_a_zero_day_limit(self):
        with self.assertRaises(ValueError):
            sweep([], max_age_days=0)


if __name__ == "__main__":
    unittest.main()
