from collections import deque
from typing import Deque, List, Optional

from models.chord_event import ChordEvent


class ChordHistoryBuffer:
    def __init__(self, max_size: int) -> None:
        if max_size <= 0:
            raise ValueError('max_size must be greater than 0')

        self.max_size = max_size
        self._events: Deque[ChordEvent] = deque(maxlen=max_size)

    def _can_merge(self, previous: ChordEvent, current: ChordEvent) -> bool:
        previous_winner = previous.analysis.stateless_winner
        current_winner = current.analysis.stateless_winner

        if previous_winner is None or current_winner is None:
            return False

        return (
            previous.analysis.notes == current.analysis.notes
            and previous_winner.chord_name == current_winner.chord_name
            and previous_winner.root_pc == current_winner.root_pc
            and previous_winner.pattern == current_winner.pattern
            and previous_winner.is_slash == current_winner.is_slash
            and previous.bass_pc == current.bass_pc
            and previous.highest_pc == current.highest_pc
        )

    def add(self, event: ChordEvent) -> None:
        if self._events and self._can_merge(self._events[-1], event):
            previous = self._events[-1]
            previous.timestamp_end = event.timestamp_end
            previous.duration_ms = (previous.timestamp_end - previous.timestamp_start) * 1000
            return

        self._events.append(event)

    def clear(self) -> None:
        self._events.clear()

    def is_empty(self) -> bool:
        return len(self._events) == 0

    def size(self) -> int:
        return len(self._events)

    def get_latest(self) -> Optional[ChordEvent]:
        if not self._events:
            return None
        return self._events[-1]

    def get_all(self) -> List[ChordEvent]:
        return list(self._events)

    def get_last_n(self, n: int) -> List[ChordEvent]:
        if n <= 0:
            return []
        return list(self._events)[-n:]
    
