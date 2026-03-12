from context.event_factory import build_chord_event
from detection.stateless_analyzer import analyze_notes_stateless


def test_build_chord_event():
    analysis = analyze_notes_stateless([36, 40, 43, 47, 50])  # C E G B D

    event = build_chord_event(
        timestamp_start=1.0,
        timestamp_end=1.25,
        analysis=analysis,
    )

    assert event.timestamp_start == 1.0
    assert event.timestamp_end == 1.25
    assert event.duration_ms == 250.0
    assert event.analysis.stateless_winner is not None
    assert event.analysis.stateless_winner.chord_name == 'Cmaj9'
    
    
def test_chord_event_contains_bass_pc_and_highest_pc():
    analysis = analyze_notes_stateless([36, 40, 43, 47, 50])  # C E G B D

    event = build_chord_event(
        timestamp_start=1.0,
        timestamp_end=1.5,
        analysis=analysis,
    )

    assert event.bass_pc == 0      # C
    assert event.highest_pc == 2   # D
    
