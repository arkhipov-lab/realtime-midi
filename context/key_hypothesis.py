from typing import List, Optional

from models.chord_event import ChordEvent
from models.key_hypothesis import KeyHypothesis


MAJOR_SCALE_INTERVALS = {0, 2, 4, 5, 7, 9, 11}
MINOR_SCALE_INTERVALS = {0, 2, 3, 5, 7, 8, 10}


def _score_event_against_key(event: ChordEvent, tonic_pc: int, mode: str) -> int:
    if mode == 'major':
        scale = MAJOR_SCALE_INTERVALS
    else:
        scale = MINOR_SCALE_INTERVALS

    pcs = set(note % 12 for note in event.analysis.notes)
    relative_pcs = {(pc - tonic_pc) % 12 for pc in pcs}

    score = 0

    # Чем больше нот аккорда попадает в тональность, тем лучше
    for rel_pc in relative_pcs:
        if rel_pc in scale:
            score += 10
        else:
            score -= 8

    winner = event.analysis.stateless_winner
    if winner is not None:
        root_rel = (winner.root_pc - tonic_pc) % 12

        # Устойчивые ступени I, IV, V
        if root_rel == 0:
            score += 18
        elif root_rel in (5, 7):
            score += 12
        elif root_rel in (2, 4, 9):
            score += 6

    # Длительные аккорды должны весить больше
    duration_weight = min(int(event.duration_ms // 250), 6)
    score += duration_weight

    return score


def detect_key_hypothesis(events: List[ChordEvent]) -> Optional[KeyHypothesis]:
    if not events:
        return None

    best: Optional[KeyHypothesis] = None

    for tonic_pc in range(12):
        for mode in ('major', 'minor'):
            score = 0

            for event in events:
                score += _score_event_against_key(event, tonic_pc, mode)

            hypothesis = KeyHypothesis(
                tonic_pc=tonic_pc,
                mode=mode,
                score=score,
            )

            if best is None or hypothesis.score > best.score:
                best = hypothesis

    return best

