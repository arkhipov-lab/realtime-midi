from typing import Callable, Dict, List, Optional, Tuple
import time

import mido

from config import STABILIZE_MS, CHORD_BUFFER_SIZE, ANALYSIS_MODE
from detection.candidate_selector import choose_best_chord_candidate
from formatting.candidate_formatting import format_candidate_notes
from formatting.chord_name import format_candidate_chord_name
from formatting.chord_notes import format_pressed_notes
from theory.intervals import get_interval_name
from theory.notes import midi_note_to_name

from context.event_factory import build_chord_event
from context.history_buffer import ChordHistoryBuffer
from detection.stateless_analyzer import analyze_notes_stateless
from context.history_debug import print_recent_chords

from context.context_analyzer import ContextAnalyzer


Signature = Tuple[str, Tuple[int, ...]]
DebugCallback = Callable[[List[int], object], None]


def build_signature(notes: List[int]) -> Optional[Signature]:
    unique_pitch_classes_count = len(set(note % 12 for note in notes))
    pressed_notes_count = len(notes)

    if unique_pitch_classes_count < 2:
        return None

    if unique_pitch_classes_count == 2 and pressed_notes_count == 2:
        return ('interval', tuple(notes))

    return ('chord_detect', tuple(notes))


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
    pressed_notes: Dict[Tuple[int, int], int] = {}

    last_output_signature: Optional[Signature] = None
    pending_signature: Optional[Signature] = None
    pending_notes: Optional[List[int]] = None
    pending_since: Optional[float] = None
    active_chord_signature: Optional[Signature] = None
    active_chord_started_at: Optional[float] = None
    active_chord_analysis = None

    history_buffer = ChordHistoryBuffer(max_size=CHORD_BUFFER_SIZE)
    context_analyzer = ContextAnalyzer()

    with mido.open_input(port_name) as inport:
        while True:
            for msg in inport.iter_pending():
                is_note_on = msg.type == 'note_on' and msg.velocity > 0
                is_note_off = msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0)

                if not (is_note_on or is_note_off):
                    continue

                key = (msg.channel, msg.note)

                if is_note_on:
                    pressed_notes[key] = msg.note
                else:
                    pressed_notes.pop(key, None)

                unique_notes = sorted(set(pressed_notes.values()))
                current_signature = build_signature(unique_notes)
                now = time.perf_counter()

                if current_signature is None:
                    last_output_signature = None
                    pending_signature = None
                    pending_notes = None
                    pending_since = None
                    continue

                if current_signature != pending_signature:
                    pending_signature = current_signature
                    pending_notes = unique_notes.copy()
                    pending_since = now

            now = time.perf_counter()

            if pending_signature is not None and pending_notes is not None and pending_since is not None:
                elapsed_ms = (now - pending_since) * 1000

                if elapsed_ms >= STABILIZE_MS and pending_signature != last_output_signature:
                    if pending_signature[0] == 'interval':
                        output = render_detection(pending_notes, debug_callback=debug_callback)
                        if output:
                            print(output)

                    else:
                        analysis = analyze_notes_stateless(pending_notes)
                        if ANALYSIS_MODE == 'context':
                            context_result = context_analyzer.analyze(
                                stateless_analysis=analysis,
                                history_buffer=history_buffer,
                            )
                            best_candidate = context_result.context_winner
                        else:
                            best_candidate = analysis.stateless_winner

                        # Если уже был активный аккорд — закрываем его
                        if active_chord_signature is not None and active_chord_analysis is not None and active_chord_started_at is not None:

                            event = build_chord_event(
                                timestamp_start=active_chord_started_at,
                                timestamp_end=now,
                                analysis=active_chord_analysis,
                            )

                            history_buffer.add(event)

                            if debug_callback is not None:
                                print_recent_chords(history_buffer.get_all())

                        # Новый активный аккорд
                        active_chord_signature = pending_signature
                        active_chord_started_at = now
                        active_chord_analysis = analysis

                        if debug_callback is not None:
                            debug_callback(pending_notes, best_candidate)

                        if best_candidate:
                            formatted_notes = format_candidate_notes(best_candidate)
                            formatted_name = format_candidate_chord_name(best_candidate)
                            print(f'{formatted_notes} -> {formatted_name}')
                        else:
                            print(f'{format_pressed_notes(pending_notes)} -> неизвестный аккорд')

                    last_output_signature = pending_signature

            time.sleep(sleep_seconds)
            
            
