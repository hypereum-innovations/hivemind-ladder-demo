"""Retention sweep: remove old working records, never audit entries.

Working records (drafts, cached tool results) expire after `max_age_days`. Audit entries are
excluded by construction: the sweep only accepts working records, and the audit log is not one.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True)
class WorkingRecord:
    key: str
    created_at: datetime


def sweep(records: list[WorkingRecord], max_age_days: int, now: datetime | None = None) -> tuple[list[WorkingRecord], list[str]]:
    """Return the records to keep and the keys that were removed."""
    if max_age_days < 1:
        raise ValueError("max_age_days must be at least 1")
    now = now or datetime.now(timezone.utc)
    cutoff = now - timedelta(days=max_age_days)
    kept = [r for r in records if r.created_at >= cutoff]
    removed = [r.key for r in records if r.created_at < cutoff]
    return kept, removed
