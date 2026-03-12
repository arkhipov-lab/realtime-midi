from dataclasses import dataclass
from typing import List, Optional

from .chord_candidate import ChordCandidate


@dataclass
class ContextAnalysisResult:
    context_winner: Optional[ChordCandidate]
    ranked_candidates: List[ChordCandidate]
    key_hypothesis: Optional[str]
    functional_label: Optional[str]
    cadence_label: Optional[str]
    explanation: Optional[str]
    
