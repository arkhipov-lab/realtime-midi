from typing import Callable, List, Optional
import time

import mido

from config import STABILIZE_MS, CHORD_BUFFER_SIZE
from context.history_buffer import ChordHistoryBuffer
from context.context_analyzer import ContextAnalyzer
from midi.live_state import (
    apply_midi_note_event,
    create_live_runtime_state,
    is_pending_ready,
    update_pending_state,
)
from pipeline.harmonic_processor import process_chord_snapshot
from rendering.cli_renderer import render_stateless_snapshot


DebugCallback = Callable[[List[int], object], None]


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
                    render_result = render_stateless_snapshot(
                        pending_notes,
                        debug_callback=debug_callback,
                    )
                    if render_result.text:
                        print(render_result.text)
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
            
