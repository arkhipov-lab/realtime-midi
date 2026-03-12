from typing import List

from models.chord_event import ChordEvent
from theory.notes import midi_note_to_name, pitch_class_to_name
from formatting.chord_name import format_candidate_chord_name


def format_event_notes(event: ChordEvent) -> str:
    return ' '.join(midi_note_to_name(n) for n in event.analysis.notes)


def format_event_display_name(event: ChordEvent) -> str:
    if event.analysis.stateless_winner:
        return format_candidate_chord_name(event.analysis.stateless_winner)
    return 'unknown'


def format_event_raw_name(event: ChordEvent) -> str:
    if event.analysis.stateless_winner:
        return event.analysis.stateless_winner.chord_name
    return 'unknown'


def format_pitch_class(pc: int | None) -> str:
    if pc is None:
        return 'None'
    return pitch_class_to_name(pc)


# def format_top_candidates(event: ChordEvent, limit: int = 3) -> str:
#     top = event.analysis.ranked_candidates[:limit]
#     if not top:
#         return '[]'

#     names = [candidate.chord_name for candidate in top]
#     return '[' + ', '.join(names) + ']'


def format_top_candidates(event: ChordEvent, limit: int = 3) -> str:
    top = event.analysis.ranked_candidates[:limit]
    if not top:
        return '[]'

    formatted = [
        f'{candidate.chord_name}({candidate.score})'
        for candidate in top
    ]

    return '[' + ', '.join(formatted) + ']'


def format_winner_score(event: ChordEvent) -> str:
    if event.analysis.stateless_winner:
        return str(event.analysis.stateless_winner.score)
    return 'None'


def print_recent_chords(events: List[ChordEvent], limit: int = 5) -> None:
    print('DEBUG: ===== CHORD HISTORY =====')

    for event in events[-limit:]:
        notes = format_event_notes(event)
        display_name = format_event_display_name(event)
        raw_name = format_event_raw_name(event)
        duration = int(event.duration_ms)

        bass_pc = format_pitch_class(event.bass_pc)
        highest_pc = format_pitch_class(event.highest_pc)

        candidate_count = len(event.analysis.candidates)
        top_candidates = format_top_candidates(event, limit=3)

        winner_score = format_winner_score(event)
        top_candidates = format_top_candidates(event, limit=3)

        print(
            f'  {display_name:<12} | '
            f'raw={raw_name:<16} | '
            f'notes=[{notes}] | '
            f'duration={duration}ms | '
            f'bass_pc={bass_pc} | '
            f'highest_pc={highest_pc} | '
            f'winner_score={winner_score} | '
            f'candidates={candidate_count} | '
            f'top3={top_candidates}'
        )

    print('DEBUG: ========================\n')
    
