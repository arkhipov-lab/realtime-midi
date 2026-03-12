from typing import Callable, List, Optional
import time

import mido

from config import STABILIZE_MS, CHORD_BUFFER_SIZE
from detection.candidate_selector import choose_best_chord_candidate
from formatting.candidate_formatting import format_candidate_notes
from formatting.chord_name import format_candidate_chord_name
from formatting.chord_notes import format_pressed_notes
from theory.intervals import get_interval_name
from theory.notes import midi_note_to_name
from context.history_buffer import ChordHistoryBuffer
from context.context_analyzer import ContextAnalyzer
from midi.live_state import (
    apply_midi_note_event,
    build_signature,
    create_live_runtime_state,
    is_pending_ready,
    update_pending_state,
)
from pipeline.harmonic_processor import process_chord_snapshot


DebugCallback = Callable[[List[int], object], None]


def render_detection(notes: List[int], debug_callback: Optional[DebugCallback] = None) -> str:
    signature = build_signature(notes)
    if signature is None:
        return ''

    if signature[0] == 'interval':
        note1, note2 = notes[0], notes[1]
        interval_name = get_interval_name(note1, note2)
        return f'{midi_note_to_name(note1)} + {midi_note_to_name(note2)} -> {interval_name}'

    best_candidate = choose_best_chord_candidate(notes)

    if debug_callback is not None:
        debug_callback(notes, best_candidate)

    if best_candidate:
        formatted_notes = format_candidate_notes(best_candidate)
        formatted_name = format_candidate_chord_name(best_candidate)
        return f'{formatted_notes} -> {formatted_name}'

    return f'{format_pressed_notes(notes)} -> неизвестный аккорд'


def run_midi_listener(
    port_name: str,
    debug_callback: Optional[DebugCallback] = None,
    sleep_seconds: float = 0.005,
) -> None:
    state = create_live_runtime_state()

    history_buffer = ChordHistoryBuffer(max_size=CHORD_BUFFER_SIZE)
    context_analyzer = ContextAnalyzer()

    with mido.open_input(port_name) as inport:
        while True:
            for msg in inport.iter_pending():
                is_note_on = msg.type == 'note_on' and msg.velocity > 0
                is_note_off = msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)

                if not (is_note_on or is_note_off):
                    continue

                unique_notes = apply_midi_note_event(
                    state,
                    channel=msg.channel,
                    note=msg.note,
                    is_note_on=is_note_on,
                )

                now = time.perf_counter()
                update_pending_state(state, unique_notes, now)

            now = time.perf_counter()

            if is_pending_ready(state, STABILIZE_MS, now):
                pending_signature = state.pending_signature
                pending_notes = state.pending_notes

                if pending_signature is None or pending_notes is None:
                    time.sleep(sleep_seconds)
                    continue

                if pending_signature[0] == 'interval':
                    output = render_detection(pending_notes, debug_callback=debug_callback)
                    if output:
                        print(output)
                else:
                    result = process_chord_snapshot(
                        notes=pending_notes,
                        now=now,
                        state=state,
                        history_buffer=history_buffer,
                        context_analyzer=context_analyzer,
                        debug_callback=debug_callback,
                    )

                    if debug_callback is not None:
                        debug_callback(pending_notes, result.best_candidate)

                    print(result.output_text)

                state.last_output_signature = pending_signature

            time.sleep(sleep_seconds)
            
