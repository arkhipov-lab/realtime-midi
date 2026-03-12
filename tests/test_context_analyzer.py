from context.context_analyzer import ContextAnalyzer
from context.history_buffer import ChordHistoryBuffer
from detection.stateless_analyzer import analyze_notes_stateless
from models.chord_candidate import ChordCandidate
from models.stateless_analysis import StatelessAnalysis
from models.chord_event import ChordEvent


def make_candidate(name: str, root_pc: int, score: int) -> ChordCandidate:
    return ChordCandidate(
        chord_name=name,
        root_pc=root_pc,
        pattern=(0, 4, 7),
        used_notes=[60, 64, 67],
        full_notes=[60, 64, 67],
        bass_note=60,
        is_slash=False,
        ignored_notes_count=0,
        score=score,
    )


def test_context_analyzer_passthrough_without_history():
    analyzer = ContextAnalyzer()
    history = ChordHistoryBuffer(max_size=8)

    c6 = make_candidate('C6', 0, 490)
    am7 = make_candidate('Am7', 9, 500)

    analysis = StatelessAnalysis(
        notes=[36, 40, 43, 45],
        candidates=[am7, c6],
        ranked_candidates=[am7, c6],
        stateless_winner=am7,
        bass_note=36,
        highest_note=45,
    )

    result = analyzer.analyze(
        stateless_analysis=analysis,
        history_buffer=history,
    )

    assert result.context_winner == am7
    assert result.ranked_candidates == [am7, c6]


def test_context_analyzer_can_reorder_by_root_movement():
    analyzer = ContextAnalyzer()
    history = ChordHistoryBuffer(max_size=8)

    previous_winner = make_candidate('G7', 7, 520)
    previous_analysis = StatelessAnalysis(
        notes=[43, 47, 50, 53],
        candidates=[previous_winner],
        ranked_candidates=[previous_winner],
        stateless_winner=previous_winner,
        bass_note=43,
        highest_note=53,
    )

    previous_event = ChordEvent(
        timestamp_start=1.0,
        timestamp_end=1.5,
        duration_ms=500.0,
        analysis=previous_analysis,
        bass_pc=7,
        highest_pc=5,
    )
    history.add(previous_event)

    # Stateless winner = Am7, but C6 should get context bonus from G -> C
    c6 = make_candidate('C6', 0, 490)
    am7 = make_candidate('Am7', 9, 500)

    current_analysis = StatelessAnalysis(
        notes=[36, 40, 43, 45],
        candidates=[am7, c6],
        ranked_candidates=[am7, c6],
        stateless_winner=am7,
        bass_note=36,
        highest_note=45,
    )

    result = analyzer.analyze(
        stateless_analysis=current_analysis,
        history_buffer=history,
    )

    assert result.context_winner == c6
    assert result.ranked_candidates[0] == c6


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
    
