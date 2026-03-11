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

    # Покрытие pitch classes
    score += len(unique_used_pcs) * 100

    # Штраф за проигнорированные pitch classes
    ignored_count = len(unique_full_pcs - unique_used_pcs)
    score -= ignored_count * 40

    # Полный аккорд лучше slash-интерпретации
    if not is_slash:
        score += 120
    else:
        score -= 30
        
    bass_pc = bass_note % 12
    chord_pcs = {(root_pc + interval) % 12 for interval in pattern}
        
    if is_slash:
        if bass_pc in chord_pcs:
            # корректное обращение
            score += 25
        else:
            # настоящий slash с внешним басом
            score -= 10

    # Бас
    if bass_pc == root_pc:
        score += 80
    elif bass_pc in chord_pcs:
        # это chord-tone bass / inversion
        score += 35
    else:
        # это non-chord-bass slash
        score -= 25

    # Размер структуры
    if len(pattern) >= 5:
        score += 50
    elif len(pattern) == 4:
        score += 25

    # Неполные extended
    if '(no' in chord_name:
        score += 35

    # Root вообще присутствует
    if root_pc in unique_used_pcs:
        score += 40
    else:
        score -= 20

    # Новый кусок: вес значимых ступеней аккорда
    for interval in pattern:
        pc = (root_pc + interval) % 12
        if pc not in unique_used_pcs:
            continue

        # root
        if interval == 0:
            score += 20

        # thirds: b3 / 3
        elif interval in (3, 4):
            score += 35

        # fifths: b5 / 5 / #5
        elif interval in (6, 7, 8):
            score += 12

        # sevenths: b7 / 7
        elif interval in (10, 11):
            score += 28

        # tensions / extensions
        elif interval in (1, 2, 5, 9):
            score += 10

    # Компактность voicing
    if used_notes:
        spread = max(used_notes) - min(used_notes)
        score -= spread // 12

    # Приоритет типа аккорда
    score += get_chord_priority_bonus(chord_name)

    return score

