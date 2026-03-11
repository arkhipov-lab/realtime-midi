from models.chord_candidate import ChordCandidate

from theory.notes import midi_note_to_name

from .chord_notes import format_detected_chord_notes


def format_candidate_notes(candidate: ChordCandidate) -> str:
    if candidate.is_slash:
        upper = format_detected_chord_notes(
            candidate.used_notes,
            candidate.root_pc,
            candidate.pattern,
            candidate.chord_name,
        )
        bass = midi_note_to_name(candidate.bass_note)
        return f'{bass} + {upper}'

    return format_detected_chord_notes(
        candidate.used_notes,
        candidate.root_pc,
        candidate.pattern,
        candidate.chord_name,
    )
    
    