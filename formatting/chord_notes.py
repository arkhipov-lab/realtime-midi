from typing import List, Tuple

from theory.notes import NOTE_NAMES_SHARP, NOTE_NAMES_FLAT
from theory.spelling import get_extended_note_name_in_context
from theory.notes import midi_note_to_name


def format_pressed_notes(notes: List[int]) -> str:
    return ' + '.join(midi_note_to_name(n) for n in sorted(notes))


def format_seventh_chord_notes(notes: List[int], root_pc: int, pattern: Tuple[int, int, int, int]) -> str:
    octave_map = {note % 12: note for note in sorted(notes)}

    preferred_names = {
        0: NOTE_NAMES_SHARP[root_pc],
        2: NOTE_NAMES_SHARP[(root_pc + 2) % 12],
        3: NOTE_NAMES_FLAT[(root_pc + 3) % 12],
        4: NOTE_NAMES_SHARP[(root_pc + 4) % 12],
        5: NOTE_NAMES_SHARP[(root_pc + 5) % 12],
        6: NOTE_NAMES_FLAT[(root_pc + 6) % 12],
        7: NOTE_NAMES_SHARP[(root_pc + 7) % 12],
        8: NOTE_NAMES_FLAT[(root_pc + 8) % 12],
        9: NOTE_NAMES_SHARP[(root_pc + 9) % 12],
        10: NOTE_NAMES_FLAT[(root_pc + 10) % 12],
        11: NOTE_NAMES_SHARP[(root_pc + 11) % 12],
    }

    result = []
    for interval in pattern:
        pc = (root_pc + interval) % 12
        note = octave_map[pc]
        octave = (note // 12) - 1
        name = preferred_names.get(interval, NOTE_NAMES_SHARP[pc])
        result.append(f'{name}{octave}')

    return ' + '.join(result)


def format_triad_notes(notes: List[int], root_pc: int, pattern: Tuple[int, int, int]) -> str:
    octave_map = {note % 12: note for note in sorted(notes)}

    preferred_names = {
        0: NOTE_NAMES_SHARP[root_pc],             # root
        2: NOTE_NAMES_SHARP[(root_pc + 2) % 12], # major 2nd
        3: NOTE_NAMES_FLAT[(root_pc + 3) % 12],  # minor 3rd
        4: NOTE_NAMES_SHARP[(root_pc + 4) % 12], # major 3rd
        5: NOTE_NAMES_SHARP[(root_pc + 5) % 12], # perfect 4th
        6: NOTE_NAMES_FLAT[(root_pc + 6) % 12],  # diminished 5th
        7: NOTE_NAMES_SHARP[(root_pc + 7) % 12], # perfect 5th
        8: NOTE_NAMES_FLAT[(root_pc + 8) % 12],  # augmented 5th / minor 6th spelling fallback
    }

    result = []
    for interval in pattern:
        pc = (root_pc + interval) % 12
        note = octave_map[pc]
        octave = (note // 12) - 1
        name = preferred_names.get(interval, NOTE_NAMES_SHARP[pc])
        result.append(f'{name}{octave}')

    return ' + '.join(result)


def format_detected_chord_notes(
    notes: List[int],
    root_pc: int,
    pattern: Tuple[int, ...],
    chord_name: str,
) -> str:
    if len(pattern) == 3:
        return format_triad_notes(notes, root_pc, pattern)
    if len(pattern) == 4:
        return format_seventh_chord_notes(notes, root_pc, pattern)
    if len(pattern) >= 5:
        return format_extended_chord_notes(notes, root_pc, pattern, chord_name)

    return format_pressed_notes(notes)


def format_extended_chord_notes(
    notes: List[int],
    root_pc: int,
    pattern: Tuple[int, ...],
    chord_name: str,
) -> str:
    octave_map = {note % 12: note for note in sorted(notes)}

    result = []
    for interval in pattern:
        pc = (root_pc + interval) % 12
        note = octave_map[pc]
        octave = (note // 12) - 1
        name = get_extended_note_name_in_context(root_pc, interval, chord_name)
        result.append(f'{name}{octave}')

    return ' + '.join(result)


def format_detected_chord_notes(
    notes: List[int],
    root_pc: int,
    pattern: Tuple[int, ...],
    chord_name: str,
) -> str:
    if len(pattern) == 2:
        return format_pressed_notes(notes)
    if len(pattern) == 3:
        return format_triad_notes(notes, root_pc, pattern)
    if len(pattern) == 4:
        return format_seventh_chord_notes(notes, root_pc, pattern)
    if len(pattern) >= 5:
        return format_extended_chord_notes(notes, root_pc, pattern, chord_name)

    return format_pressed_notes(notes)
