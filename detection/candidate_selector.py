from typing import List, Optional

from models.chord_candidate import ChordCandidate
from detection.stateless_analyzer import analyze_notes_stateless


def choose_best_chord_candidate(notes: List[int]) -> Optional[ChordCandidate]:
    analysis = analyze_notes_stateless(notes)
    return analysis.stateless_winner


