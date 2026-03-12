from dataclasses import dataclass
from typing import List, Optional

from .chord_candidate import ChordCandidate


@dataclass
class StatelessAnalysis:
    notes: List[int]
    candidates: List[ChordCandidate]
    ranked_candidates: List[ChordCandidate]
    stateless_winner: Optional[ChordCandidate]
    bass_note: Optional[int]
    highest_note: Optional[int]
    
