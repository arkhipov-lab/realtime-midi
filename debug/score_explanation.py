from typing import List, Tuple

from scoring.chord_priority import get_chord_priority_bonus


def explain_chord_candidate_score(
    chord_name: str,
    root_pc: int,
    pattern: Tuple[int, ...],
    used_notes: List[int],
    full_notes: List[int],
    bass_note: int,
    is_slash: bool,
) -> List[str]:
    explanations: List[str] = []

    unique_used_pcs = set(n % 12 for n in used_notes)
    unique_full_pcs = set(n % 12 for n in full_notes)

    explanations.append(f'+{len(unique_used_pcs) * 100} for covered pitch classes')

    ignored_count = len(unique_full_pcs - unique_used_pcs)
    explanations.append(f'-{ignored_count * 40} for ignored pitch classes')

    if not is_slash:
        explanations.append('+120 for full chord')
    else:
        explanations.append('-30 for slash interpretation')

    bass_pc = bass_note % 12
    chord_pcs = {(root_pc + interval) % 12 for interval in pattern}

    if bass_pc == root_pc:
        explanations.append('+80 because bass is root')
    elif bass_pc in chord_pcs:
        explanations.append('+20 because bass is chord tone')
    else:
        explanations.append('-20 because bass is non-chord tone')

    if len(pattern) >= 5:
        explanations.append('+50 for extended structure')
    elif len(pattern) == 4:
        explanations.append('+25 for 4-note structure')

    if '(no' in chord_name:
        explanations.append('+35 for incomplete extended chord')

    bonus = get_chord_priority_bonus(chord_name)
    if bonus:
        explanations.append(f'+{bonus} chord type priority bonus')

    return explanations

