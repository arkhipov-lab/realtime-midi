from models.context_analysis import ContextAnalysisResult
from models.stateless_analysis import StatelessAnalysis
from context.history_buffer import ChordHistoryBuffer


class ContextAnalyzer:
    def analyze(
        self,
        stateless_analysis: StatelessAnalysis,
        history_buffer: ChordHistoryBuffer,
    ) -> ContextAnalysisResult:
        # Пока просто passthrough
        return ContextAnalysisResult(
            context_winner=stateless_analysis.stateless_winner,
            ranked_candidates=stateless_analysis.ranked_candidates,
            key_hypothesis=None,
            functional_label=None,
            cadence_label=None,
            explanation='Context analyzer skeleton: passthrough to stateless winner',
        )
        
