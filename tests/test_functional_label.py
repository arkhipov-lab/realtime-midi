from context.functional_label import detect_functional_label
from models.chord_candidate import ChordCandidate
from models.key_hypothesis import KeyHypothesis


def make_candidate(root_pc: int) -> ChordCandidate:
    return ChordCandidate(
        chord_name='X',
        root_pc=root_pc,
        pattern=(0, 4, 7),
        used_notes=[60, 64, 67],
        full_notes=[60, 64, 67],
        bass_note=60,
        is_slash=False,
        ignored_notes_count=0,
        score=100,
    )


def test_detect_functional_label_in_c_major():
    key = KeyHypothesis(tonic_pc=0, mode='major', score=80)

    assert detect_functional_label(make_candidate(0), key) == 'I'
    assert detect_functional_label(make_candidate(2), key) == 'ii'
    assert detect_functional_label(make_candidate(5), key) == 'IV'
    assert detect_functional_label(make_candidate(7), key) == 'V'
    assert detect_functional_label(make_candidate(9), key) == 'vi'


def test_detect_functional_label_in_a_minor():
    key = KeyHypothesis(tonic_pc=9, mode='minor', score=75)

    assert detect_functional_label(make_candidate(9), key) == 'i'
    assert detect_functional_label(make_candidate(0), key) == 'III'
    assert detect_functional_label(make_candidate(2), key) == 'iv'
    assert detect_functional_label(make_candidate(4), key) == 'v'
    assert detect_functional_label(make_candidate(7), key) == 'VII'
    
