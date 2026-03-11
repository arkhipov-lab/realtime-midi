from tests.helpers import detect_name


def test_cmaj9_not_em7_slash_c():
    assert detect_name([36, 40, 43, 47, 50]) == 'Cmaj9'  # C E G B D


def test_first_inversion_major():
    assert detect_name([64, 67, 72]) == 'C/E'  # E G C


def test_power_chord_with_doubled_root():
    assert detect_name([36, 43, 48]) == 'C5'  # C G C


def test_incomplete_dominant_seventh():
    assert detect_name([55, 62, 65]) == 'G7'  # G D F


def test_non_chord_bass_case_current_behavior():
    assert detect_name([38, 48, 52, 55]) == 'Cadd9/D'  # D C E G
    
    
