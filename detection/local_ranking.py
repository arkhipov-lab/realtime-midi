from typing import List, Optional, Tuple


ChordDetectionResult = Tuple[str, int, Tuple[int, ...]]


def score_three_pc_candidate(item: ChordDetectionResult) -> int:
    chord_name, _, pattern = item

    if chord_name.endswith('quartal'):
        return 18

    if any(tag in chord_name for tag in ('5add9', 'sus4(no3)', 'sus2sus4', 'cluster5')):
        return 16

    if any(tag in chord_name for tag in ('7(shell)', 'maj7(shell)', 'm7(shell)')):
        return 24

    if any(tag in chord_name for tag in (
        '7(no3)', '7(no5)',
        'maj7(no3)', 'maj7(no5)',
        'm7(no3)', 'm7(no5)',
        'm(maj7)(no3)', 'm(maj7)(no5)',
        'm7b5(no3)', 'm7b5(no5)',
        'dim7(no3)', 'dim7(no5)',
    )):
        return 22

    return len(pattern) + 30


def score_four_pc_candidate(
    item: ChordDetectionResult,
    notes: List[int],
) -> int:
    chord_name, root_pc, _ = item
    bass_pc = min(notes) % 12

    score = 0

    if 'quartal' in chord_name:
        score += 18
    if 'add9' in chord_name:
        score += 42
    if 'maj7#11' in chord_name:
        score += 44
    if any(tag in chord_name for tag in ('7b9', '7#9', '7#11', '7b13', '9(', '11(', '13(')):
        score += 40
    if chord_name.endswith(('6', 'm6')):
        score += 35
    if chord_name.endswith((
        'maj7', 'm7', '7', 'dim7', 'm7b5', 'm(maj7)',
        '7#5', 'maj7#5', '7b5', 'maj7b5', '7sus4', '7sus2'
    )):
        score += 30

    if root_pc == bass_pc:
        score += 20

    return score


def score_five_plus_pc_candidate(item: ChordDetectionResult) -> int:
    chord_name, _, pattern = item

    if 'quartal' in chord_name:
        return 18
    if 'maj7#11' in chord_name:
        return 58
    if '13sus4' in chord_name:
        return 57
    if any(tag in chord_name for tag in ('7b9', '7#9', '7#11', '7b13')):
        return 55
    if '9sus4' in chord_name:
        return 53
    if '6/9' in chord_name:
        return 52
    if any(tag in chord_name for tag in ('maj13', 'm13', '13')):
        return 60
    if any(tag in chord_name for tag in ('maj11', 'm11', '11')):
        return 55
    if any(tag in chord_name for tag in ('maj9', 'm9', '9')):
        return 50

    return len(pattern)


def choose_best_three_pc_candidate(
    candidates: List[ChordDetectionResult],
) -> Optional[ChordDetectionResult]:
    if not candidates:
        return None

    return max(candidates, key=score_three_pc_candidate)


def choose_best_four_pc_candidate(
    candidates: List[ChordDetectionResult],
    notes: List[int],
) -> Optional[ChordDetectionResult]:
    if not candidates:
        return None

    return max(candidates, key=lambda item: score_four_pc_candidate(item, notes))


def choose_best_five_plus_pc_candidate(
    candidates: List[ChordDetectionResult],
) -> Optional[ChordDetectionResult]:
    if not candidates:
        return None

    return max(candidates, key=score_five_plus_pc_candidate)


