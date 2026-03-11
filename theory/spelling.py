from theory.notes import NOTE_NAMES_SHARP, NOTE_NAMES_FLAT


def get_note_name_in_chord_context(root_pc: int, interval: int) -> str:
    preferred_names = {
        0: NOTE_NAMES_SHARP[root_pc],
        1: NOTE_NAMES_FLAT[(root_pc + 1) % 12],
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
    return preferred_names.get(interval, NOTE_NAMES_SHARP[(root_pc + interval) % 12])


def get_extended_note_name_in_context(root_pc: int, interval: int, chord_name: str) -> str:
    if '7b9' in chord_name and interval == 1:
        return NOTE_NAMES_FLAT[(root_pc + 1) % 12]

    if '7#9' in chord_name and interval == 3:
        return NOTE_NAMES_SHARP[(root_pc + 3) % 12]

    if ('7#11' in chord_name or 'maj7#11' in chord_name) and interval == 6:
        return NOTE_NAMES_SHARP[(root_pc + 6) % 12]

    if '7b13' in chord_name and interval == 8:
        return NOTE_NAMES_FLAT[(root_pc + 8) % 12]

    if ('9sus4' in chord_name or '13sus4' in chord_name) and interval == 5:
        return NOTE_NAMES_SHARP[(root_pc + 5) % 12]

    if interval == 9 and '6/9' in chord_name:
        return NOTE_NAMES_SHARP[(root_pc + 9) % 12]

    if interval == 2 and ('add9' in chord_name or '6/9' in chord_name or '9' in chord_name):
        return NOTE_NAMES_SHARP[(root_pc + 2) % 12]

    return get_note_name_in_chord_context(root_pc, interval)

