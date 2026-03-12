from context.event_factory import build_chord_event
from context.key_hypothesis import detect_key_hypothesis
from detection.stateless_analyzer import analyze_notes_stateless


def make_event(notes, start, end):
    analysis = analyze_notes_stateless(notes)
    return build_chord_event(
        timestamp_start=start,
        timestamp_end=end,
        analysis=analysis,
    )


def test_detect_key_hypothesis_c_major_progression():
    events = [
        make_event([48, 52, 55], 1.0, 2.0),       # C
        make_event([53, 57, 60], 2.1, 3.0),       # F
        make_event([55, 59, 62, 65], 3.1, 4.0),   # G7
        make_event([48, 52, 55, 59], 4.1, 5.2),   # Cmaj7
    ]

    hypothesis = detect_key_hypothesis(events)

    assert hypothesis is not None
    assert hypothesis.tonic_pc == 0
    assert hypothesis.mode == 'major'


def test_detect_key_hypothesis_a_minor_progression():
    events = [
        make_event([45, 48, 52], 1.0, 2.0),       # Am
        make_event([50, 53, 57], 2.1, 3.0),       # Dm
        make_event([52, 56, 59, 62], 3.1, 4.0),   # E7
        make_event([45, 48, 52, 55], 4.1, 5.0),   # Am7
    ]

    hypothesis = detect_key_hypothesis(events)

    assert hypothesis is not None
    assert hypothesis.tonic_pc == 9
    assert hypothesis.mode == 'minor'
    
