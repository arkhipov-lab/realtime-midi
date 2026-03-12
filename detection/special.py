from typing import List, Tuple, Optional

from .basic import (
    detect_power_chord,
    detect_chord,
    detect_quartal_chord,
    detect_ambiguous_voicing,
    detect_sixth_chord,
)
from .extended import (
    detect_extended_chord,
    detect_incomplete_extended_chord,
)
from .seventh import (
    detect_seventh_chord,
    detect_incomplete_seventh_chord,
)
from .local_ranking import (
    choose_best_three_pc_candidate,
    choose_best_four_pc_candidate,
    choose_best_five_plus_pc_candidate,
)


ChordDetectionResult = Tuple[str, int, Tuple[int, ...]]


def detect_any_chord(notes: List[int]) -> Optional[ChordDetectionResult]:
    unique_pitch_classes = set(note % 12 for note in notes)

    if len(unique_pitch_classes) == 3:
        return detect_chord(notes)

    if len(unique_pitch_classes) == 4:
        return detect_seventh_chord(notes)

    if len(unique_pitch_classes) >= 5:
        return detect_extended_chord(notes)

    return None


def detect_chord_from_notes(notes: List[int]) -> Optional[ChordDetectionResult]:
    unique_pitch_classes = sorted(set(note % 12 for note in notes))

    if len(unique_pitch_classes) == 2:
        return detect_power_chord(notes)

    if len(unique_pitch_classes) == 3:
        candidates = [
            c for c in (
                detect_chord(notes),
                detect_incomplete_seventh_chord(notes),
                detect_quartal_chord(notes),
                detect_ambiguous_voicing(notes),
            )
            if c is not None
        ]
        return choose_best_three_pc_candidate(candidates)

    if len(unique_pitch_classes) == 4:
        candidates = [
            c for c in (
                detect_sixth_chord(notes),
                detect_seventh_chord(notes),
                detect_extended_chord(notes),
                detect_quartal_chord(notes),
                detect_incomplete_extended_chord(notes),
            )
            if c is not None
        ]
        return choose_best_four_pc_candidate(candidates, notes)

    if len(unique_pitch_classes) >= 5:
        candidates = [
            c for c in (
                detect_extended_chord(notes),
                detect_quartal_chord(notes),
                detect_incomplete_extended_chord(notes),
            )
            if c is not None
        ]
        return choose_best_five_plus_pc_candidate(candidates)

    return None

