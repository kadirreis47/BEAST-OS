from __future__ import annotations

from collections.abc import Iterable

from .models import TimeBlock


def find_conflicts(
    candidate: TimeBlock,
    existing: Iterable[TimeBlock],
    *,
    ignore_block_id=None,
) -> list[TimeBlock]:
    return [
        block
        for block in existing
        if block.id != ignore_block_id and candidate.overlaps(block)
    ]


def has_conflict(
    candidate: TimeBlock,
    existing: Iterable[TimeBlock],
    *,
    ignore_block_id=None,
) -> bool:
    return bool(
        find_conflicts(
            candidate,
            existing,
            ignore_block_id=ignore_block_id,
        )
    )
