from collections import deque
from typing import Deque, List, Optional

from models.chord_event import ChordEvent


class ChordHistoryBuffer:
    def __init__(self, max_size: int) -> None:
        if max_size <= 0:
            raise ValueError('max_size must be greater than 0')

        self.max_size = max_size
        self._events: Deque[ChordEvent] = deque(maxlen=max_size)

    def add(self, event: ChordEvent) -> None:
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
    
    
    