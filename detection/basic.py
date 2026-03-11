from typing import Dict, Tuple, Optional, List
from theory.patterns import CHORD_PATTERNS
from theory.notes import pitch_class_to_name
from theory.patterns import SIXTH_CHORD_PATTERNS


def normalize_to_root(pitch_classes: List[int], root: int) -> Tuple[int, ...]:
    return tuple(sorted((pc - root) % 12 for pc in pitch_classes))


def detect_chord(notes: List[int]) -> Optional[Tuple[str, int, Tuple[int, int, int]]]:
    """
    Возвращает:
    (имя_аккорда, root_pc, pattern)
    например:
    ('Cm', 0, (0, 3, 7))
    """
    pitch_classes = sorted(set(note % 12 for note in notes))
    if len(pitch_classes) != 3:
        return None

    for candidate_root in pitch_classes:
        pattern = normalize_to_root(pitch_classes, candidate_root)
        suffix = CHORD_PATTERNS.get(pattern)
        if suffix is not None:
            root_name = pitch_class_to_name(candidate_root)
            return f'{root_name}{suffix}', candidate_root, pattern

    return None


def build_interval_signature(pressed_notes: Dict[Tuple[int, int], int]) -> Optional[Tuple[int, int]]:
    unique_notes = sorted(set(pressed_notes.values()))
    if len(unique_notes) != 2:
        return None
    return unique_notes[0], unique_notes[1]


def build_chord_signature(pressed_notes: Dict[Tuple[int, int], int]) -> Optional[Tuple[int, int, int]]:
    unique_notes = sorted(set(pressed_notes.values()))
    if len(unique_notes) != 3:
        return None
    return unique_notes[0], unique_notes[1], unique_notes[2]


def detect_sixth_chord(notes: List[int]) -> Optional[Tuple[str, int, Tuple[int, int, int, int]]]:
    pitch_classes = sorted(set(note % 12 for note in notes))
    if len(pitch_classes) != 4:
        return None

    for candidate_root in pitch_classes:
        pattern = normalize_to_root(pitch_classes, candidate_root)
        suffix = SIXTH_CHORD_PATTERNS.get(pattern)
        if suffix is not None:
            root_name = pitch_class_to_name(candidate_root)
            return f'{root_name}{suffix}', candidate_root, pattern

    return None


def detect_power_chord(notes: List[int]) -> Optional[Tuple[str, int, Tuple[int, ...]]]:
    pitch_classes = sorted(set(note % 12 for note in notes))
    if len(pitch_classes) != 2:
        return None

    for candidate_root in pitch_classes:
        pattern = normalize_to_root(pitch_classes, candidate_root)
        if pattern == (0, 7):
            root_name = pitch_class_to_name(candidate_root)
            return f'{root_name}5', candidate_root, pattern

    return None


def detect_quartal_chord(notes: List[int]) -> Optional[Tuple[str, int, Tuple[int, ...]]]:
    pitch_classes = sorted(set(note % 12 for note in notes))
    if len(pitch_classes) < 3:
        return None

    for candidate_root in pitch_classes:
        pattern = normalize_to_root(pitch_classes, candidate_root)

        # Последовательность кварт: +5, +10, +3, ...
        is_quartal = True
        for i in range(1, len(pattern)):
            prev = pattern[i - 1]
            cur = pattern[i]
            if (cur - prev) % 12 != 5:
                is_quartal = False
                break

        if is_quartal:
            root_name = pitch_class_to_name(candidate_root)
            return f'{root_name}quartal', candidate_root, pattern

    return None


def detect_ambiguous_voicing(notes: List[int]) -> Optional[Tuple[str, int, Tuple[int, ...]]]:
    pitch_classes = sorted(set(note % 12 for note in notes))
    if len(pitch_classes) < 3:
        return None

    for candidate_root in pitch_classes:
        pattern = normalize_to_root(pitch_classes, candidate_root)

        if pattern == (0, 2, 7):
            root_name = pitch_class_to_name(candidate_root)
            return f'{root_name}5add9', candidate_root, pattern

        if pattern == (0, 5, 7):
            root_name = pitch_class_to_name(candidate_root)
            return f'{root_name}sus4(no3)', candidate_root, pattern

        if pattern == (0, 2, 5):
            root_name = pitch_class_to_name(candidate_root)
            return f'{root_name}sus2sus4', candidate_root, pattern

        if pattern == (0, 1, 7):
            root_name = pitch_class_to_name(candidate_root)
            return f'{root_name}cluster5', candidate_root, pattern

    return None


def is_bass_in_chord(root_pc: int, bass_note: int, pattern: Tuple[int, ...]) -> bool:
    bass_pc = bass_note % 12
    chord_pcs = {(root_pc + interval) % 12 for interval in pattern}
    return bass_pc in chord_pcs
