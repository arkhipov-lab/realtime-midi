from dataclasses import dataclass
from typing import Optional

from models.context_analysis import ContextAnalysisResult
from models.stateless_analysis import StatelessAnalysis
from models.chord_candidate import ChordCandidate


@dataclass
class ProcessingResult:
    analysis: StatelessAnalysis
    best_candidate: Optional[ChordCandidate]
    context_result: Optional[ContextAnalysisResult]
    output_text: str
    
