from dataclasses import dataclass
from typing import List, Optional

from .chord_candidate import ChordCandidate
from .key_hypothesis import KeyHypothesis
from .context_score_breakdown import ContextScoreBreakdown


@dataclass
class ContextAnalysisResult:
    context_winner: Optional[ChordCandidate]
    ranked_candidates: List[ChordCandidate]
    key_hypothesis: Optional[KeyHypothesis]
    previous_functional_label: Optional[str]
    functional_label: Optional[str]
    cadence_label: Optional[str]
    movement_label: Optional[str]
    explanation: Optional[str]
    score_breakdowns: dict[str, ContextScoreBreakdown]
        
    