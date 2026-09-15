"""Append-only audit log whose entries are linked by a SHA-256 hash chain.

Every entry stores the hash of the previous entry, so editing or removing an earlier entry breaks
every hash after it. `verify()` walks the chain and reports the first entry that does not match.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone

GENESIS_HASH = "0" * 64


def _entry_hash(prev_hash: str, seq: int, action: str, actor: str, at: str, details: dict) -> str:
    payload = json.dumps(
        {"prev": prev_hash, "seq": seq, "action": action, "actor": actor, "at": at, "details": details},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class AuditEntry:
    seq: int
    action: str
    actor: str
    at: str
    details: dict
    prev_hash: str
    hash: str


@dataclass
class AuditLog:
    entries: list[AuditEntry] = field(default_factory=list)

    def append(self, action: str, actor: str, details: dict | None = None) -> AuditEntry:
        broken = self.verify()
        if broken is not None:
            raise ValueError(f"audit chain is broken at entry {broken}; refusing to append")
        details = dict(details or {})
        seq = len(self.entries) + 1
        prev_hash = self.entries[-1].hash if self.entries else GENESIS_HASH
        at = datetime.now(timezone.utc).isoformat()
        entry = AuditEntry(seq, action, actor, at, details, prev_hash, _entry_hash(prev_hash, seq, action, actor, at, details))
        self.entries.append(entry)
        return entry

    def verify(self) -> int | None:
        """Return the sequence number of the first broken entry, or None when the chain is intact."""
        prev_hash = GENESIS_HASH
        for entry in self.entries:
            expected = _entry_hash(prev_hash, entry.seq, entry.action, entry.actor, entry.at, entry.details)
            if entry.prev_hash != prev_hash or entry.hash != expected:
                return entry.seq
            prev_hash = entry.hash
        return None
