from scoring.candidate_scoring import score_chord_candidate


def test_full_chord_scores_higher_than_slash_interpretation():
    full_score = score_chord_candidate(
        chord_name='Cmaj9',
        root_pc=0,
        pattern=(0, 2, 4, 7, 11),
        used_notes=[36, 40, 43, 47, 50],
        full_notes=[36, 40, 43, 47, 50],
        bass_note=36,
        is_slash=False,
    )

    slash_score = score_chord_candidate(
        chord_name='Em7',
        root_pc=4,
        pattern=(0, 3, 7, 10),
        used_notes=[40, 43, 47, 50],
        full_notes=[36, 40, 43, 47, 50],
        bass_note=36,
        is_slash=True,
    )

    assert full_score > slash_score


def test_root_in_bass_scores_higher_than_non_chord_bass():
    root_score = score_chord_candidate(
        chord_name='C7',
        root_pc=0,
        pattern=(0, 4, 7, 10),
        used_notes=[36, 40, 43, 46],
        full_notes=[36, 40, 43, 46],
        bass_note=36,
        is_slash=False,
    )

    slash_score = score_chord_candidate(
        chord_name='C7',
        root_pc=0,
        pattern=(0, 4, 7, 10),
        used_notes=[40, 43, 46, 48],
        full_notes=[38, 40, 43, 46, 48],
        bass_note=38,
        is_slash=True,
    )

    assert root_score > slash_score
    
    
