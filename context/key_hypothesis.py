from typing import List, Optional

from models.chord_event import ChordEvent
from models.key_hypothesis import KeyHypothesis


MAJOR_SCALE_INTERVALS = {0, 2, 4, 5, 7, 9, 11}
MINOR_SCALE_INTERVALS = {0, 2, 3, 5, 7, 8, 10}


def _score_root_function_in_key(root_rel: int, mode: str) -> int:
    if mode == 'major':
        if root_rel == 0:   # I
            return 22
        if root_rel == 7:   # V
            return 18
        if root_rel == 5:   # IV
            return 12
        if root_rel in (2, 9):  # ii, vi
            return 8
        if root_rel in (4, 11):  # iii, vii
            return 4
        return 0

    # minor
    if root_rel == 0:   # i
        return 24
    if root_rel == 7:   # V / v
        return 20
    if root_rel == 5:   # iv
        return 12
    if root_rel in (3, 8, 10):  # III, VI, VII
        return 8
    if root_rel == 2:   # ii°
        return 4
    return 0


def _score_event_against_key(event: ChordEvent, tonic_pc: int, mode: str) -> int:
    if mode == 'major':
        scale = MAJOR_SCALE_INTERVALS
    else:
        scale = MINOR_SCALE_INTERVALS

    pcs = set(note % 12 for note in event.analysis.notes)
    relative_pcs = {(pc - tonic_pc) % 12 for pc in pcs}

    score = 0

    for rel_pc in relative_pcs:
        if rel_pc in scale:
            score += 10
        else:
            score -= 8

    winner = event.analysis.stateless_winner
    if winner is not None:
        root_rel = (winner.root_pc - tonic_pc) % 12
        score += _score_root_function_in_key(root_rel, mode)

    duration_weight = min(int(event.duration_ms // 250), 6)
    score += duration_weight

    return score


def score_key_hypothesis(events: List[ChordEvent], tonic_pc: int, mode: str) -> int:
    return sum(_score_event_against_key(event, tonic_pc, mode) for event in events)


def _score_event_transitions(events: List[ChordEvent], tonic_pc: int, mode: str) -> int:
    score = 0

    for prev, cur in zip(events, events[1:]):
        prev_winner = prev.analysis.stateless_winner
        cur_winner = cur.analysis.stateless_winner

        if prev_winner is None or cur_winner is None:
            continue

        prev_rel = (prev_winner.root_pc - tonic_pc) % 12
        cur_rel = (cur_winner.root_pc - tonic_pc) % 12

        # V -> I / i
        if prev_rel == 7 and cur_rel == 0:
            score += 28

        # IV -> V
        if prev_rel == 5 and cur_rel == 7:
            score += 10

        # ii -> V (major-ish)
        if prev_rel == 2 and cur_rel == 7:
            score += 10

    return score


def detect_key_hypothesis(events: List[ChordEvent]) -> Optional[KeyHypothesis]:
    if not events:
        return None

    best: Optional[KeyHypothesis] = None

    for tonic_pc in range(12):
        for mode in ('major', 'minor'):
            score = score_key_hypothesis(events, tonic_pc, mode)
            score += _score_event_transitions(events, tonic_pc, mode)

            hypothesis = KeyHypothesis(
                tonic_pc=tonic_pc,
                mode=mode,
                score=score,
            )

            if best is None or hypothesis.score > best.score:
                best = hypothesis

    return best

