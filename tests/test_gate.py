import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from approvals.gate import ApprovalGate, Decision  # noqa: E402


class ApprovalGateTest(unittest.TestCase):
    def test_low_risk_runs_without_a_human_but_is_logged(self):
        gate = ApprovalGate(threshold=50)
        request = gate.submit("read_report", risk=10, requested_by="agent:analyst")
        self.assertIs(request.decision, Decision.AUTO)
        self.assertEqual(gate.audit.entries[-1].action, "action.auto_approved")

    def test_high_risk_waits_for_a_reviewer(self):
        gate = ApprovalGate(threshold=50)
        request = gate.submit("send_payment", risk=80, requested_by="agent:treasury")
        self.assertIs(request.decision, Decision.PENDING)
        gate.decide(request, approved=True, reviewer="user:controller")
        self.assertIs(request.decision, Decision.APPROVED)
        self.assertEqual(request.decided_by, "user:controller")
        self.assertIsNotNone(request.decided_at)
        self.assertEqual(gate.audit.entries[-1].actor, "user:controller")

    def test_requester_cannot_approve_itself(self):
        gate = ApprovalGate(threshold=50)
        request = gate.submit("send_payment", risk=80, requested_by="user:controller")
        with self.assertRaises(PermissionError):
            gate.decide(request, approved=True, reviewer="user:controller")


if __name__ == "__main__":
    unittest.main()
