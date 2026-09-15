"""Approval gate: an action at or above the risk threshold waits for a human decision.

Actions below the threshold run immediately and are still written to the audit log, so the log
shows every action, not only the ones a person reviewed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

from .audit_log import AuditLog


class Decision(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    AUTO = "auto"


@dataclass
class ActionRequest:
    action: str
    risk: int
    requested_by: str
    decision: Decision = Decision.PENDING
    decided_by: str | None = None
    decided_at: str | None = None


@dataclass
class ApprovalGate:
    threshold: int
    audit: AuditLog = field(default_factory=AuditLog)

    def submit(self, action: str, risk: int, requested_by: str) -> ActionRequest:
        if not 0 <= risk <= 100:
            raise ValueError("risk must be between 0 and 100")
        request = ActionRequest(action, risk, requested_by)
        if risk < self.threshold:
            request.decision = Decision.AUTO
            self.audit.append("action.auto_approved", requested_by, {"action": action, "risk": risk})
        else:
            self.audit.append("approval.requested", requested_by, {"action": action, "risk": risk})
        return request

    def decide(self, request: ActionRequest, approved: bool, reviewer: str) -> ActionRequest:
        if request.decision is not Decision.PENDING:
            raise ValueError("only a pending request can be decided")
        if reviewer == request.requested_by:
            raise PermissionError("the requester cannot approve their own action")
        request.decision = Decision.APPROVED if approved else Decision.REJECTED
        request.decided_by = reviewer
        request.decided_at = datetime.now(timezone.utc).isoformat()
        self.audit.append(
            f"approval.{request.decision.value}",
            reviewer,
            {"action": request.action, "decided_at": request.decided_at},
        )
        return request
