from typing import Tuple, List
from dataclasses import dataclass


@dataclass
class ChordCandidate:
    chord_name: str
    root_pc: int
    pattern: Tuple[int, ...]
    used_notes: List[int]
    full_notes: List[int]
    bass_note: int
    is_slash: bool
    ignored_notes_count: int
    score: int
    
    
    