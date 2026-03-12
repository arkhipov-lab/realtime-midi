from models.context_analysis import ContextAnalysisResult
from models.stateless_analysis import StatelessAnalysis
from models.chord_candidate import ChordCandidate
from context.history_buffer import ChordHistoryBuffer
from context.key_hypothesis import detect_key_hypothesis


class ContextAnalyzer:
    def _get_root_movement_bonus(
        self,
        previous_root_pc: int,
        candidate: ChordCandidate,
    ) -> int:
        interval = (candidate.root_pc - previous_root_pc) % 12

        if interval in (5, 7):   # P4 / P5
            return 24
        if interval in (1, 2, 10, 11):  # stepwise
            return 10
        if interval == 0:  # same root
            return 6
        if interval in (3, 4, 8, 9):  # thirds / sixths
            return 4

        return 0

    def _get_movement_label(
        self,
        previous_root_pc: int,
        current_root_pc: int,
    ) -> str:
        interval = (current_root_pc - previous_root_pc) % 12

        if interval == 0:
            return 'same-root'
        if interval in (1, 2, 10, 11):
            return 'step-motion'
        if interval in (3, 4, 8, 9):
            return 'third-motion'
        if interval == 5:
            return 'dominant-like'
        if interval == 7:
            return 'subdominant-like'

        return 'other-motion'

    def analyze(
        self,
        stateless_analysis: StatelessAnalysis,
        history_buffer: ChordHistoryBuffer,
    ) -> ContextAnalysisResult:
        latest_event = history_buffer.get_latest()
        key_hypothesis = detect_key_hypothesis(history_buffer.get_all())

        if latest_event is None or latest_event.analysis.stateless_winner is None:
            return ContextAnalysisResult(
                context_winner=stateless_analysis.stateless_winner,
                ranked_candidates=stateless_analysis.ranked_candidates,
                key_hypothesis=key_hypothesis,
                functional_label=None,
                cadence_label=None,
                movement_label=None,
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
        movement_label = None

        if context_winner is not None:
            movement_label = self._get_movement_label(previous_root_pc, context_winner.root_pc)

        return ContextAnalysisResult(
            context_winner=context_winner,
            ranked_candidates=ranked_candidates,
            key_hypothesis=key_hypothesis,
            functional_label=None,
            cadence_label=None,
            movement_label=movement_label,
            explanation=f'Context analyzer: applied root movement bonus from previous root_pc={previous_root_pc}',
        )
        
