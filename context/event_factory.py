from models.chord_event import ChordEvent
from models.stateless_analysis import StatelessAnalysis


def build_chord_event(
    timestamp_start: float,
    timestamp_end: float,
    analysis: StatelessAnalysis,
) -> ChordEvent:
    duration_ms = (timestamp_end - timestamp_start) * 1000

    return ChordEvent(
        timestamp_start=timestamp_start,
        timestamp_end=timestamp_end,
        duration_ms=duration_ms,
        analysis=analysis,
    )
    
