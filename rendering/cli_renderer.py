from typing import List, Optional

from detection.candidate_selector import choose_best_chord_candidate
from formatting.candidate_formatting import format_candidate_notes
from formatting.chord_name import format_candidate_chord_name
from formatting.chord_notes import format_pressed_notes
from midi.live_state import build_signature
from models.chord_candidate import ChordCandidate
from models.render_result import RenderResult
from theory.intervals import get_interval_name
from theory.notes import midi_note_to_name


def render_interval(notes: List[int]) -> RenderResult:
    note1, note2 = notes[0], notes[1]
    interval_name = get_interval_name(note1, note2)
    return RenderResult(
        text=f'{midi_note_to_name(note1)} + {midi_note_to_name(note2)} -> {interval_name}'
    )


def render_candidate_result(best_candidate: ChordCandidate) -> RenderResult:
    formatted_notes = format_candidate_notes(best_candidate)
    formatted_name = format_candidate_chord_name(best_candidate)
    return RenderResult(
        text=f'{formatted_notes} -> {formatted_name}'
    )


def render_unknown(notes: List[int]) -> RenderResult:
    return RenderResult(
        text=f'{format_pressed_notes(notes)} -> неизвестный аккорд'
    )


def render_stateless_snapshot(
    notes: List[int],
    debug_callback=None,
) -> RenderResult:
    signature = build_signature(notes)
    if signature is None:
        return RenderResult(text='')

    if signature[0] == 'interval':
        return render_interval(notes)

    best_candidate = choose_best_chord_candidate(notes)

    if debug_callback is not None:
        debug_callback(notes, best_candidate)

    if best_candidate is not None:
        return render_candidate_result(best_candidate)

    return render_unknown(notes)


def render_best_candidate_or_unknown(
    notes: List[int],
    best_candidate: Optional[ChordCandidate],
) -> RenderResult:
    if best_candidate is None:
        return render_unknown(notes)

    return render_candidate_result(best_candidate)

