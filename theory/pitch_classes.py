from typing import List
from .notes import NOTE_NAMES_SHARP


def format_pitch_classes(notes: List[int]) -> str:
    pcs = sorted(set(note % 12 for note in notes))
    return ' '.join(NOTE_NAMES_SHARP[pc] for pc in pcs)

