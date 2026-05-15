"""Friction signal detection background job.

Enqueued by the scheduler every 15 minutes.
Implemented in Phase 1.
"""
from __future__ import annotations


def detect_friction(org_id: str) -> None:
    """Analyze recent events for friction signals."""
    raise NotImplementedError
