from context.event_factory import build_chord_event
from context.history_debug import print_recent_chords
from detection.stateless_analyzer import analyze_notes_stateless


def test_print_recent_chords_outputs_name_notes_and_duration(capsys):
    analysis = analyze_notes_stateless([36, 40, 43])  # C
    event = build_chord_event(
        timestamp_start=1.0,
        timestamp_end=1.4,
        analysis=analysis,
    )

    print_recent_chords([event], limit=5)

    captured = capsys.readouterr().out

    assert 'C' in captured
    assert 'duration=' in captured
    assert 'C2' in captured
    
    