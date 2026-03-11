from models.chord_candidate import ChordCandidate
from theory.notes import midi_note_to_name
from .chord_notes import format_detected_chord_notes, format_pressed_notes


def format_candidate_notes(candidate: ChordCandidate) -> str:
    if candidate.is_slash:
        upper_notes = sorted(candidate.used_notes)

        removed_bass = False
        filtered_upper_notes = []
        for note in upper_notes:
            if not removed_bass and note == candidate.bass_note:
                removed_bass = True
                continue
            filtered_upper_notes.append(note)

        bass = midi_note_to_name(candidate.bass_note)

        if not filtered_upper_notes:
            return bass

        upper = format_pressed_notes(filtered_upper_notes)
        return f'{bass} + {upper}'

    return format_detected_chord_notes(
        candidate.used_notes,
        candidate.root_pc,
        candidate.pattern,
        candidate.chord_name,
    )
    
    