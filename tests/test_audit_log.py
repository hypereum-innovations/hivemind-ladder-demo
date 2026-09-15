import sys
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from approvals.audit_log import AuditLog  # noqa: E402


class AuditLogTest(unittest.TestCase):
    def test_intact_chain_verifies(self):
        log = AuditLog()
        log.append("approval.requested", "agent:planner", {"action": "send_invoice"})
        log.append("approval.granted", "user:reviewer")
        self.assertIsNone(log.verify())

    def test_edited_entry_breaks_the_chain_at_that_entry(self):
        log = AuditLog()
        log.append("approval.requested", "agent:planner")
        log.append("approval.granted", "user:reviewer")
        log.entries[0] = replace(log.entries[0], actor="user:someone-else")
        self.assertEqual(log.verify(), 1)


if __name__ == "__main__":
    unittest.main()
