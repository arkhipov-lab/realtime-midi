from typing import List, Tuple, Optional

from theory.notes import pitch_class_to_name
from .basic import normalize_to_root
from theory.patterns import INCOMPLETE_EXTENDED_CHORD_PATTERNS, EXTENDED_CHORD_PATTERNS
from theory.intervals import interval_to_missing_label


def detect_extended_chord(notes: List[int]) -> Optional[Tuple[str, int, Tuple[int, ...]]]:
    pitch_classes = sorted(set(note % 12 for note in notes))
    if len(pitch_classes) < 4:
        return None

    for candidate_root in pitch_classes:
        pattern = normalize_to_root(pitch_classes, candidate_root)
        suffix = EXTENDED_CHORD_PATTERNS.get(pattern)
        if suffix is not None:
            root_name = pitch_class_to_name(candidate_root)
            return f'{root_name}{suffix}', candidate_root, pattern

    return None


def detect_incomplete_extended_chord(notes: List[int]) -> Optional[Tuple[str, int, Tuple[int, ...]]]:
    pitch_classes = sorted(set(note % 12 for note in notes))
    if len(pitch_classes) < 4:
        return None

    for candidate_root in pitch_classes:
        pattern = set(normalize_to_root(pitch_classes, candidate_root))

        for spec in INCOMPLETE_EXTENDED_CHORD_PATTERNS:
            required = spec['required']
            optional = spec['optional']
            allowed = required | optional

            if not required.issubset(pattern):
                continue

            if not pattern.issubset(allowed):
                continue

            missing_optional = sorted(optional - pattern)
            suffix = spec['suffix']

            if missing_optional:
                missing_text = ','.join(
                    f'no{interval_to_missing_label(interval, suffix)}'
                    for interval in missing_optional
                )
                suffix = f'{suffix}({missing_text})'

            root_name = pitch_class_to_name(candidate_root)
            full_pattern = tuple(sorted(pattern))
            return f'{root_name}{suffix}', candidate_root, full_pattern

    return None



