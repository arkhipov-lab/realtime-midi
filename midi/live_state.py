from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


Signature = Tuple[str, Tuple[int, ...]]


@dataclass
class LiveRuntimeState:
    pressed_notes: Dict[Tuple[int, int], int]
    last_output_signature: Optional[Signature]
    pending_signature: Optional[Signature]
    pending_notes: Optional[List[int]]
    pending_since: Optional[float]
    active_chord_signature: Optional[Signature]
    active_chord_started_at: Optional[float]
    active_chord_analysis: object


def create_live_runtime_state() -> LiveRuntimeState:
    return LiveRuntimeState(
        pressed_notes={},
        last_output_signature=None,
        pending_signature=None,
        pending_notes=None,
        pending_since=None,
        active_chord_signature=None,
        active_chord_started_at=None,
        active_chord_analysis=None,
    )


def build_signature(notes: List[int]) -> Optional[Signature]:
    unique_pitch_classes_count = len(set(note % 12 for note in notes))
    pressed_notes_count = len(notes)

    if unique_pitch_classes_count < 2:
        return None

    if unique_pitch_classes_count == 2 and pressed_notes_count == 2:
        return ('interval', tuple(notes))

    return ('chord_detect', tuple(notes))


def apply_midi_note_event(
    state: LiveRuntimeState,
    *,
    channel: int,
    note: int,
    is_note_on: bool,
) -> List[int]:
    key = (channel, note)

    if is_note_on:
        state.pressed_notes[key] = note
    else:
        state.pressed_notes.pop(key, None)

    return sorted(set(state.pressed_notes.values()))


def reset_pending_state(state: LiveRuntimeState) -> None:
    state.last_output_signature = None
    state.pending_signature = None
    state.pending_notes = None
    state.pending_since = None


def update_pending_state(
    state: LiveRuntimeState,
    current_notes: List[int],
    now: float,
) -> Optional[Signature]:
    current_signature = build_signature(current_notes)

    if current_signature is None:
        reset_pending_state(state)
        return None

    if current_signature != state.pending_signature:
        state.pending_signature = current_signature
        state.pending_notes = current_notes.copy()
        state.pending_since = now

    return current_signature


def is_pending_ready(
    state: LiveRuntimeState,
    stabilize_ms: int,
    now: float,
) -> bool:
    if (
        state.pending_signature is None
        or state.pending_notes is None
        or state.pending_since is None
    ):
        return False

    elapsed_ms = (now - state.pending_since) * 1000
    return elapsed_ms >= stabilize_ms and state.pending_signature != state.last_output_signature
