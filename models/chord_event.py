from dataclasses import dataclass
from typing import Optional

from .stateless_analysis import StatelessAnalysis


@dataclass
class ChordEvent:
    timestamp_start: float
    timestamp_end: float
    duration_ms: float
    analysis: StatelessAnalysis
    bass_pc: Optional[int]
    highest_pc: Optional[int]
    
