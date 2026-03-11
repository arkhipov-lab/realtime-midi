from typing import List, Tuple

from .chord_priority import get_chord_priority_bonus


def score_chord_candidate(
    chord_name: str,
    root_pc: int,
    pattern: Tuple[int, ...],
    used_notes: List[int],
    full_notes: List[int],
    bass_note: int,
    is_slash: bool,
) -> int:
    score = 0

    unique_used_pcs = set(n % 12 for n in used_notes)
    unique_full_pcs = set(n % 12 for n in full_notes)

    score += len(unique_used_pcs) * 100

    ignored_count = len(unique_full_pcs - unique_used_pcs)
    score -= ignored_count * 40

    if not is_slash:
        score += 120
    else:
        score -= 30

    bass_pc = bass_note % 12
    chord_pcs = {(root_pc + interval) % 12 for interval in pattern}

    if bass_pc == root_pc:
        score += 80
    elif bass_pc in chord_pcs:
        score += 20
    else:
        score -= 20

    if len(pattern) >= 5:
        score += 50
    elif len(pattern) == 4:
        score += 25

    if '(no' in chord_name:
        score += 35

    score += get_chord_priority_bonus(chord_name)

    return score

