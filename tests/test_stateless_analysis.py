from detection.stateless_analyzer import analyze_notes_stateless


def test_stateless_analysis_returns_ranked_candidates():
    analysis = analyze_notes_stateless([36, 40, 43, 47, 50])  # C E G B D

    assert analysis.notes == [36, 40, 43, 47, 50]
    assert analysis.stateless_winner is not None
    assert analysis.stateless_winner.chord_name == 'Cmaj9'
    assert len(analysis.candidates) >= 1
    assert len(analysis.ranked_candidates) >= 1
    assert analysis.bass_note == 36
    assert analysis.highest_note == 50
    
