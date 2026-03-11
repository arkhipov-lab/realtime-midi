from typing import List, Optional

from detection.candidate_builder import build_chord_candidates

from formatting.chord_notes import format_pressed_notes
from formatting.chord_name import format_candidate_chord_name

from theory.notes import NOTE_NAMES_SHARP, midi_note_to_name
from theory.pitch_classes import format_pitch_classes

from models.chord_candidate import ChordCandidate


def debug_print_candidates(notes: List[int]) -> None:
    candidates = build_chord_candidates(notes)

    print('\nDEBUG: ==================================================')
    print(f'DEBUG: input notes        = {format_pressed_notes(notes)}')
    print(f'DEBUG: input pitch class  = {format_pitch_classes(notes)}')

    if not candidates:
        print('DEBUG: candidates         = not found')
        print('DEBUG: ==================================================\n')
        return

    sorted_candidates = sorted(candidates, key=lambda c: c.score, reverse=True)

    for i, candidate in enumerate(sorted_candidates, start=1):
        formatted_used_notes = format_pressed_notes(candidate.used_notes)
        formatted_full_notes = format_pressed_notes(candidate.full_notes)
        formatted_name = format_candidate_chord_name(candidate)

        used_pcs = format_pitch_classes(candidate.used_notes)
        full_pcs = format_pitch_classes(candidate.full_notes)

        print(f'DEBUG: candidate #{i}')
        print(f'  name            = {candidate.chord_name}')
        print(f'  rendered_name   = {formatted_name}')
        print(f'  score           = {candidate.score}')
        print(f'  root_pc         = {NOTE_NAMES_SHARP[candidate.root_pc]}')
        print(f'  pattern         = {candidate.pattern}')
        print(f'  is_slash        = {candidate.is_slash}')
        print(f'  bass_note       = {midi_note_to_name(candidate.bass_note)}')
        print(f'  ignored_count   = {candidate.ignored_notes_count}')
        print(f'  used_notes      = {formatted_used_notes}')
        print(f'  used_pcs        = {used_pcs}')
        print(f'  full_notes      = {formatted_full_notes}')
        print(f'  full_pcs        = {full_pcs}')
        print('')

    print('DEBUG: ==================================================\n')
    
    
def debug_print_winner(candidate: Optional["ChordCandidate"]) -> None:
    if not candidate:
        print('DEBUG: winner = None')
        return

    print(
        'DEBUG: winner = '
        f'{format_candidate_chord_name(candidate)} | '
        f'score={candidate.score} | '
        f'used=[{format_pressed_notes(candidate.used_notes)}]'
    )    

