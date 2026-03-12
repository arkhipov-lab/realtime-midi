from models.context_analysis import ContextAnalysisResult
from models.stateless_analysis import StatelessAnalysis
from models.chord_candidate import ChordCandidate
from context.history_buffer import ChordHistoryBuffer


class ContextAnalyzer:
    def _get_root_movement_bonus(
        self,
        previous_root_pc: int,
        candidate: ChordCandidate,
    ) -> int:
        interval = (candidate.root_pc - previous_root_pc) % 12

        # Самые естественные движения:
        # по кварте/квинте, по секунде, удержание центра
        if interval in (5, 7):   # P4 / P5
            return 24
        if interval in (1, 2, 10, 11):  # stepwise
            return 10
        if interval == 0:  # same root
            return 6
        if interval in (3, 4, 8, 9):  # thirds / sixths
            return 4

        return 0

    def analyze(
        self,
        stateless_analysis: StatelessAnalysis,
        history_buffer: ChordHistoryBuffer,
    ) -> ContextAnalysisResult:
        latest_event = history_buffer.get_latest()

        # Если истории нет — passthrough
        if latest_event is None or latest_event.analysis.stateless_winner is None:
            return ContextAnalysisResult(
                context_winner=stateless_analysis.stateless_winner,
                ranked_candidates=stateless_analysis.ranked_candidates,
                key_hypothesis=None,
                functional_label=None,
                cadence_label=None,
                explanation='Context analyzer: no history, passthrough to stateless winner',
            )

        previous_root_pc = latest_event.analysis.stateless_winner.root_pc

        ranked_candidates = sorted(
            stateless_analysis.ranked_candidates,
            key=lambda candidate: (
                candidate.score + self._get_root_movement_bonus(previous_root_pc, candidate),
                candidate.score,
            ),
            reverse=True,
        )

        context_winner = ranked_candidates[0] if ranked_candidates else None

        return ContextAnalysisResult(
            context_winner=context_winner,
            ranked_candidates=ranked_candidates,
            key_hypothesis=None,
            functional_label=None,
            cadence_label=None,
            explanation=f'Context analyzer: applied root movement bonus from previous root_pc={previous_root_pc}',
        )
        
