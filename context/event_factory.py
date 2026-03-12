from models.chord_event import ChordEvent
from models.stateless_analysis import StatelessAnalysis


def build_chord_event(
    timestamp_start: float,
    timestamp_end: float,
    analysis: StatelessAnalysis,
) -> ChordEvent:
    duration_ms = (timestamp_end - timestamp_start) * 1000

    bass_pc = None if analysis.bass_note is None else analysis.bass_note % 12
    highest_pc = None if analysis.highest_note is None else analysis.highest_note % 12

    return ChordEvent(
        timestamp_start=timestamp_start,
        timestamp_end=timestamp_end,
        duration_ms=duration_ms,
        analysis=analysis,
        bass_pc=bass_pc,
        highest_pc=highest_pc,
    )
    
