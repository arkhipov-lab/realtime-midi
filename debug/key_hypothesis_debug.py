from typing import List

from context.key_hypothesis import score_key_hypothesis, _score_event_against_key
from models.chord_event import ChordEvent
from theory.notes import pitch_class_to_name
from formatting.chord_name import format_candidate_chord_name


def _event_name(event: ChordEvent) -> str:
    winner = event.analysis.stateless_winner
    if winner is None:
        return 'unknown'
    return format_candidate_chord_name(winner)


def print_key_hypothesis_debug(events: List[ChordEvent], top_n: int = 3) -> None:
    if not events:
        print('DEBUG: ===== KEY HYPOTHESIS =====')
        print('DEBUG: no events')
        print('DEBUG: ==========================\n')
        return

    scored = []

    for tonic_pc in range(12):
        for mode in ('major', 'minor'):
            total = score_key_hypothesis(events, tonic_pc, mode)
            scored.append((total, tonic_pc, mode))

    scored.sort(reverse=True)

    print('DEBUG: ===== KEY HYPOTHESIS =====')

    for total, tonic_pc, mode in scored[:top_n]:
        tonic_name = pitch_class_to_name(tonic_pc)
        print(f'DEBUG: {tonic_name} {mode} ({total})')

        for idx, event in enumerate(events, start=1):
            event_score = _score_event_against_key(event, tonic_pc, mode)
            print(f'  event {idx}: {_event_name(event):<12} {event_score:+d}')

    print('DEBUG: ==========================\n')
    
