from tests.helpers import detect_name


def test_duplicate_root_and_fifth_do_not_break_major():
    assert detect_name([36, 43, 48, 52, 55]) == 'C'  # C G C E G


def test_extra_fifth_does_not_break_c7():
    assert detect_name([36, 40, 43, 46, 55]) == 'C7'  # C E G Bb G


def test_extra_fifth_does_not_break_cmaj9():
    assert detect_name([36, 40, 43, 47, 50, 55]) == 'Cmaj9'  # C E G B D G


def test_subset_detection_finds_core_chord():
    assert detect_name([36, 40, 43, 46, 50, 55]) == 'C9'  # C E G Bb D G


def test_power_chord_with_octave_duplication():
    assert detect_name([36, 43, 48, 55]) == 'C5'
    
    