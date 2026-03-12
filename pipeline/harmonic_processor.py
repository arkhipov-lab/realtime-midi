from typing import List

from config import ANALYSIS_MODE
from context.context_analyzer import ContextAnalyzer
from context.event_factory import build_chord_event
from context.history_buffer import ChordHistoryBuffer
from context.history_debug import print_recent_chords
from debug.context_debug import print_context_result
from debug.key_hypothesis_debug import print_key_hypothesis_debug
from detection.stateless_analyzer import analyze_notes_stateless
from midi.live_state import LiveRuntimeState
from models.processing_result import ProcessingResult
from rendering.cli_renderer import render_best_candidate_or_unknown


def close_active_chord_if_needed(
    *,
    state: LiveRuntimeState,
    now: float,
    history_buffer: ChordHistoryBuffer,
    debug_enabled: bool,
) -> None:
    if (
        state.active_chord_signature is None
        or state.active_chord_analysis is None
        or state.active_chord_started_at is None
    ):
        return

    event = build_chord_event(
        timestamp_start=state.active_chord_started_at,
        timestamp_end=now,
        analysis=state.active_chord_analysis,
    )

    history_buffer.add(event)

    if debug_enabled:
        print_recent_chords(history_buffer.get_all())


def process_chord_snapshot(
    *,
    notes: List[int],
    now: float,
    state: LiveRuntimeState,
    history_buffer: ChordHistoryBuffer,
    context_analyzer: ContextAnalyzer,
    debug_callback,
) -> ProcessingResult:
    close_active_chord_if_needed(
        state=state,
        now=now,
        history_buffer=history_buffer,
        debug_enabled=debug_callback is not None,
    )

    analysis = analyze_notes_stateless(notes)

    if analysis.stateless_winner is None:
        render_result = render_best_candidate_or_unknown(notes, None)
        return ProcessingResult(
            analysis=analysis,
            best_candidate=None,
            context_result=None,
            output_text=render_result.text,
        )

    context_result = None
    best_candidate = analysis.stateless_winner

    if ANALYSIS_MODE == 'context':
        context_result = context_analyzer.analyze(
            stateless_analysis=analysis,
            history_buffer=history_buffer,
        )
        best_candidate = context_result.context_winner

    if ANALYSIS_MODE == 'context' and debug_callback is not None:
        stateless_winner = analysis.stateless_winner.chord_name if analysis.stateless_winner else 'None'
        context_winner = context_result.context_winner.chord_name if context_result and context_result.context_winner else 'None'
        print(f'DEBUG: stateless_winner = {stateless_winner}')
        print(f'DEBUG: context_winner   = {context_winner}')
        if context_result is not None:
            print_context_result(context_result)
        print_key_hypothesis_debug(history_buffer.get_all())

    state.active_chord_signature = state.pending_signature
    state.active_chord_started_at = now
    state.active_chord_analysis = analysis

    render_result = render_best_candidate_or_unknown(notes, best_candidate)
    output_text = render_result.text

    return ProcessingResult(
        analysis=analysis,
        best_candidate=best_candidate,
        context_result=context_result,
        output_text=output_text,
    )
    
