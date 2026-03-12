from typing import List, Optional, Tuple

from detection.basic import is_bass_in_chord
from detection.special import detect_any_chord
from formatting.chord_notes import format_detected_chord_notes
from theory.notes import midi_note_to_name, pitch_class_to_pretty_name


def format_non_chord_bass_slash_chord(notes: List[int]) -> Optional[Tuple[str, str]]:
    if len(notes) < 4:
        return None

    sorted_notes = sorted(set(notes))
    bass_note = sorted_notes[0]
    upper_notes = sorted_notes[1:]

    detected = detect_any_chord(upper_notes)
    if not detected:
        return None

    chord_name, root_pc, pattern = detected

    if is_bass_in_chord(root_pc, bass_note, pattern):
        return None

    upper_formatted = format_detected_chord_notes(upper_notes, root_pc, pattern)
    bass_formatted = midi_note_to_name(bass_note)
    bass_pc_name = pitch_class_to_pretty_name(bass_note % 12)

    formatted_notes = f'{bass_formatted} + {upper_formatted}'
    slash_name = f'{chord_name}/{bass_pc_name}'

    return formatted_notes, slash_name

