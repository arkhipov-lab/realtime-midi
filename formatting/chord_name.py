from typing import List, Tuple

from models.chord_candidate import ChordCandidate
from theory.notes import NOTE_NAMES_SHARP
from theory.spelling import get_note_name_in_chord_context
from .chord_display import simplify_chord_name


def format_chord_with_slash(chord_name: str, root_pc: int, notes: List[int], pattern: Tuple[int, ...]) -> str:
    bass_note = min(notes)
    bass_pc = bass_note % 12

    if bass_pc == root_pc:
        return chord_name

    chord_pcs = {(root_pc + interval) % 12: interval for interval in pattern}
    bass_interval = chord_pcs.get(bass_pc)

    if bass_interval is None:
        bass_name = NOTE_NAMES_SHARP[bass_pc]
        return f'{chord_name}/{bass_name}'

    bass_name = get_note_name_in_chord_context(root_pc, bass_interval)
    return f'{chord_name}/{bass_name}'


def format_candidate_chord_name(candidate: ChordCandidate) -> str:
    simplified_name = simplify_chord_name(candidate.chord_name)

    if not candidate.is_slash:
        return format_chord_with_slash(
            chord_name=simplified_name,
            root_pc=candidate.root_pc,
            notes=candidate.used_notes,
            pattern=candidate.pattern,
        )

    bass_pc = candidate.bass_note % 12

    chord_pcs = {(candidate.root_pc + interval) % 12: interval for interval in candidate.pattern}
    bass_interval = chord_pcs.get(bass_pc)

    if bass_interval is not None:
        bass_name = get_note_name_in_chord_context(candidate.root_pc, bass_interval)
    else:
        bass_name = NOTE_NAMES_SHARP[bass_pc]

    return f'{simplified_name}/{bass_name}'
