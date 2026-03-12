from dataclasses import dataclass

from .stateless_analysis import StatelessAnalysis


@dataclass
class ChordEvent:
    timestamp_start: float
    timestamp_end: float
    duration_ms: float
    analysis: StatelessAnalysis
    
