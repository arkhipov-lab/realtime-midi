from detection.candidate_selector import choose_best_chord_candidate


def test_choose_root_position_major():
    candidate = choose_best_chord_candidate([60, 64, 67])  # C E G
    assert candidate is not None
    assert candidate.chord_name == 'C'
    assert candidate.root_pc == 0
    assert candidate.is_slash is False


def test_choose_first_inversion():
    candidate = choose_best_chord_candidate([64, 67, 72])  # E G C
    assert candidate is not None
    assert candidate.chord_name == 'C'
    assert candidate.is_slash is True


def test_choose_cmaj9_over_em7_slash_c():
    candidate = choose_best_chord_candidate([36, 40, 43, 47, 50])  # C E G B D
    assert candidate is not None
    assert candidate.chord_name == 'Cmaj9'


def test_choose_power_chord_with_doubled_root():
    candidate = choose_best_chord_candidate([36, 43, 48])  # C G C
    assert candidate is not None
    assert candidate.chord_name == 'C5'


def test_choose_non_chord_bass_slash_when_needed():
    candidate = choose_best_chord_candidate([38, 48, 52, 55])  # D + C E G
    assert candidate is not None
    assert candidate.is_slash is True
    
