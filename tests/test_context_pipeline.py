from context.context_analyzer import ContextAnalyzer
from context.event_factory import build_chord_event
from context.history_buffer import ChordHistoryBuffer
from detection.stateless_analyzer import analyze_notes_stateless


def test_context_pipeline_with_history_buffer():
    analyzer = ContextAnalyzer()
    history = ChordHistoryBuffer(max_size=8)

    analysis1 = analyze_notes_stateless([36, 40, 43])  # C
    event1 = build_chord_event(
        timestamp_start=1.0,
        timestamp_end=1.5,
        analysis=analysis1,
    )
    history.add(event1)

    analysis2 = analyze_notes_stateless([38, 42, 45, 48])  # Dm-ish / Dm7 without C depending on engine
    result = analyzer.analyze(
        stateless_analysis=analysis2,
        history_buffer=history,
    )

    assert result.context_winner == analysis2.stateless_winner
    assert history.size() == 1
    
