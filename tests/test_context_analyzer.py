from context.context_analyzer import ContextAnalyzer
from context.history_buffer import ChordHistoryBuffer
from detection.stateless_analyzer import analyze_notes_stateless


def test_context_analyzer_passthrough_returns_stateless_winner():
    analyzer = ContextAnalyzer()
    history = ChordHistoryBuffer(max_size=8)

    stateless_analysis = analyze_notes_stateless([36, 40, 43, 47, 50])  # Cmaj9

    result = analyzer.analyze(
        stateless_analysis=stateless_analysis,
        history_buffer=history,
    )

    assert result.context_winner is not None
    assert stateless_analysis.stateless_winner is not None
    assert result.context_winner == stateless_analysis.stateless_winner


def test_context_analyzer_passthrough_keeps_ranked_candidates():
    analyzer = ContextAnalyzer()
    history = ChordHistoryBuffer(max_size=8)

    stateless_analysis = analyze_notes_stateless([36, 40, 43, 45])  # C6 / Am7

    result = analyzer.analyze(
        stateless_analysis=stateless_analysis,
        history_buffer=history,
    )

    assert result.ranked_candidates == stateless_analysis.ranked_candidates
    assert len(result.ranked_candidates) > 0


def test_context_analyzer_initial_fields_are_empty():
    analyzer = ContextAnalyzer()
    history = ChordHistoryBuffer(max_size=8)

    stateless_analysis = analyze_notes_stateless([36, 40, 43])  # C

    result = analyzer.analyze(
        stateless_analysis=stateless_analysis,
        history_buffer=history,
    )

    assert result.key_hypothesis is None
    assert result.functional_label is None
    assert result.cadence_label is None
    assert result.explanation is not None
    
