from tests.helpers import detect_notes


def test_c7_spelling_uses_bb():
    assert detect_notes([60, 64, 67, 70]) == 'C4 + E4 + G4 + Bb4'


def test_cm7_spelling_uses_eb_and_bb():
    assert detect_notes([60, 63, 67, 70]) == 'C4 + Eb4 + G4 + Bb4'


def test_c7b13_spelling_uses_ab():
    notes = detect_notes([60, 64, 67, 70, 68])
    assert notes is not None
    assert 'Ab4' in notes
    assert 'Bb4' in notes


def test_cmaj7_sharp11_spelling_uses_f_sharp():
    notes = detect_notes([60, 64, 67, 71, 66])
    assert notes is not None
    assert 'F#4' in notes
    assert 'B4' in notes
    assert 'G4' in notes
    
    
