from formatting.chord_name import format_candidate_chord_name
from formatting.candidate_formatting import format_candidate_notes
from models.chord_candidate import ChordCandidate


def test_format_candidate_chord_name_root_position():
    candidate = ChordCandidate(
        chord_name='C',
        root_pc=0,
        pattern=(0, 4, 7),
        used_notes=[60, 64, 67],
        full_notes=[60, 64, 67],
        bass_note=60,
        is_slash=False,
        ignored_notes_count=0,
        score=100,
    )
    assert format_candidate_chord_name(candidate) == 'C'


def test_format_candidate_chord_name_slash():
    candidate = ChordCandidate(
        chord_name='C',
        root_pc=0,
        pattern=(0, 4, 7),
        used_notes=[64, 67, 72],
        full_notes=[64, 67, 72],
        bass_note=64,
        is_slash=True,
        ignored_notes_count=0,
        score=100,
    )
    assert format_candidate_chord_name(candidate) == 'C/E'


def test_format_candidate_notes():
    candidate = ChordCandidate(
        chord_name='C7',
        root_pc=0,
        pattern=(0, 4, 7, 10),
        used_notes=[60, 64, 67, 70],
        full_notes=[60, 64, 67, 70],
        bass_note=60,
        is_slash=False,
        ignored_notes_count=0,
        score=100,
    )
    assert format_candidate_notes(candidate) == 'C4 + E4 + G4 + Bb4'
    
