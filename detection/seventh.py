from typing import List, Tuple, Optional

from theory.patterns import SEVENTH_CHORD_PATTERNS, INCOMPLETE_SEVENTH_CHORD_PATTERNS
from theory.notes import pitch_class_to_name
from .basic import normalize_to_root


def detect_seventh_chord(notes: List[int]) -> Optional[Tuple[str, int, Tuple[int, int, int, int]]]:
    pitch_classes = sorted(set(note % 12 for note in notes))
    if len(pitch_classes) != 4:
        return None

    for candidate_root in pitch_classes:
        pattern = normalize_to_root(pitch_classes, candidate_root)
        suffix = SEVENTH_CHORD_PATTERNS.get(pattern)
        if suffix is not None:
            root_name = pitch_class_to_name(candidate_root)
            chord_name = f'{root_name}{suffix}'
            return chord_name, candidate_root, pattern

    return None


def detect_incomplete_seventh_chord(notes: List[int]) -> Optional[Tuple[str, int, Tuple[int, ...]]]:
    pitch_classes = sorted(set(note % 12 for note in notes))
    if len(pitch_classes) != 3:
        return None

    for candidate_root in pitch_classes:
        pattern = set(normalize_to_root(pitch_classes, candidate_root))

        for spec in INCOMPLETE_SEVENTH_CHORD_PATTERNS:
            required = spec['required']
            if pattern == required:
                root_name = pitch_class_to_name(candidate_root)
                return f'{root_name}{spec["suffix"]}', candidate_root, tuple(sorted(pattern))

    return None
