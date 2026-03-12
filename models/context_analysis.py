from dataclasses import dataclass
from typing import List, Optional

from .chord_candidate import ChordCandidate
from .key_hypothesis import KeyHypothesis


@dataclass
class ContextAnalysisResult:
    context_winner: Optional[ChordCandidate]
    ranked_candidates: List[ChordCandidate]
    key_hypothesis: Optional[KeyHypothesis]
    functional_label: Optional[str]
    cadence_label: Optional[str]
    movement_label: Optional[str]
    explanation: Optional[str]
