from context.event_factory import build_chord_event
from context.history_buffer import ChordHistoryBuffer
from detection.stateless_analyzer import analyze_notes_stateless


def make_event(notes, start, end):
    analysis = analyze_notes_stateless(notes)
    return build_chord_event(
        timestamp_start=start,
        timestamp_end=end,
        analysis=analysis,
    )


def test_history_buffer_add_and_latest():
    buffer = ChordHistoryBuffer(max_size=3)

    event1 = make_event([36, 40, 43], 1.0, 1.2)
    event2 = make_event([38, 41, 45], 1.3, 1.5)

    buffer.add(event1)
    buffer.add(event2)

    assert buffer.size() == 2
    assert buffer.get_latest() == event2


def test_history_buffer_respects_max_size():
    buffer = ChordHistoryBuffer(max_size=2)

    event1 = make_event([36, 40, 43], 1.0, 1.2)
    event2 = make_event([38, 41, 45], 1.3, 1.5)
    event3 = make_event([43, 47, 50], 1.6, 1.8)

    buffer.add(event1)
    buffer.add(event2)
    buffer.add(event3)

    events = buffer.get_all()

    assert buffer.size() == 2
    assert events[0] == event2
    assert events[1] == event3


def test_history_buffer_get_last_n():
    buffer = ChordHistoryBuffer(max_size=5)

    event1 = make_event([36, 40, 43], 1.0, 1.2)
    event2 = make_event([38, 41, 45], 1.3, 1.5)
    event3 = make_event([43, 47, 50], 1.6, 1.8)

    buffer.add(event1)
    buffer.add(event2)
    buffer.add(event3)

    last_two = buffer.get_last_n(2)

    assert last_two == [event2, event3]


def test_history_buffer_clear():
    buffer = ChordHistoryBuffer(max_size=3)

    event = make_event([36, 40, 43], 1.0, 1.2)
    buffer.add(event)

    buffer.clear()

    assert buffer.is_empty() is True
    assert buffer.get_latest() is None
    
    
