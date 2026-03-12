from dataclasses import dataclass
from typing import List


@dataclass
class NoteSegment:
    notes: List[int]
    timestamp: float
    
