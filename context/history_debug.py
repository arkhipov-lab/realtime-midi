from typing import List

from models.chord_event import ChordEvent
from theory.notes import midi_note_to_name, pitch_class_to_name
from formatting.chord_name import format_candidate_chord_name


def format_event_notes(event: ChordEvent) -> str:
    return ' '.join(midi_note_to_name(n) for n in event.analysis.notes)


def format_event_name(event: ChordEvent) -> str:
    if event.analysis.stateless_winner:
        return format_candidate_chord_name(event.analysis.stateless_winner)
    return 'unknown'


def format_pitch_class(pc: int | None) -> str:
    if pc is None:
        return 'None'
    return pitch_class_to_name(pc)


def print_recent_chords(events: List[ChordEvent], limit: int = 5) -> None:
    print('DEBUG: ===== CHORD HISTORY =====')

    for event in events[-limit:]:
        notes = format_event_notes(event)
        name = format_event_name(event)
        duration = int(event.duration_ms)

        bass_pc = format_pitch_class(event.bass_pc)
        highest_pc = format_pitch_class(event.highest_pc)

        print(
            f'  {name:<12} | '
            f'notes=[{notes}] | '
            f'duration={duration}ms | '
            f'bass_pc={bass_pc} | '
            f'highest_pc={highest_pc}'
        )

    print('DEBUG: ========================\n')
    
