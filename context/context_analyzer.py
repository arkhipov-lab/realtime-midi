from models.context_analysis import ContextAnalysisResult
from models.stateless_analysis import StatelessAnalysis
from models.chord_candidate import ChordCandidate
from context.history_buffer import ChordHistoryBuffer
from context.key_hypothesis import detect_key_hypothesis
from context.functional_label import detect_functional_label
from context.cadence_label import detect_cadence_label


class ContextAnalyzer:
    
    MOVEMENT_REORDER_THRESHOLD = 12
    
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

    def _rerank_with_movement_awareness(
        self,
        previous_root_pc: int,
        candidates: list[ChordCandidate],
    ) -> list[ChordCandidate]:
        if not candidates:
            return candidates

        if len(candidates) == 1:
            return candidates

        top_score = candidates[0].score

        close_candidates = [
            candidate
            for candidate in candidates
            if (top_score - candidate.score) <= self.MOVEMENT_REORDER_THRESHOLD
        ]

        far_candidates = [
            candidate
            for candidate in candidates
            if (top_score - candidate.score) > self.MOVEMENT_REORDER_THRESHOLD
        ]

        reranked_close = sorted(
            close_candidates,
            key=lambda candidate: (
                candidate.score + self._get_root_movement_bonus(previous_root_pc, candidate),
                candidate.score,
            ),
            reverse=True,
        )

        return reranked_close + far_candidates

    def analyze(
        self,
        stateless_analysis: StatelessAnalysis,
        history_buffer: ChordHistoryBuffer,
    ) -> ContextAnalysisResult:
        latest_event = history_buffer.get_latest()
        key_hypothesis = detect_key_hypothesis(history_buffer.get_all())

        if latest_event is None or latest_event.analysis.stateless_winner is None:
            passthrough_winner = stateless_analysis.stateless_winner
            functional_label = detect_functional_label(
                candidate=passthrough_winner,
                key_hypothesis=key_hypothesis,
            )

            return ContextAnalysisResult(
                context_winner=passthrough_winner,
                ranked_candidates=stateless_analysis.ranked_candidates,
                key_hypothesis=key_hypothesis,
                functional_label=functional_label,
                cadence_label=None,
                movement_label=None,
                explanation='Context analyzer: no history, passthrough to stateless winner',
            )

        previous_root_pc = latest_event.analysis.stateless_winner.root_pc

        ranked_candidates = self._rerank_with_movement_awareness(
            previous_root_pc=previous_root_pc,
            candidates=stateless_analysis.ranked_candidates,
        )

        context_winner = ranked_candidates[0] if ranked_candidates else None
        movement_label = None

        if context_winner is not None:
            movement_label = self._get_movement_label(previous_root_pc, context_winner.root_pc)

        functional_label = detect_functional_label(
            candidate=context_winner,
            key_hypothesis=key_hypothesis,
        )

        previous_functional_label = None

        if latest_event.analysis.stateless_winner is not None and key_hypothesis is not None:
            previous_root_pc = latest_event.analysis.stateless_winner.root_pc

            if key_hypothesis.mode == 'major':
                major_functions = {
                    0: 'I',
                    2: 'ii',
                    4: 'iii',
                    5: 'IV',
                    7: 'V',
                    9: 'vi',
                    11: 'vii°',
                }
                previous_functional_label = major_functions.get(
                    (previous_root_pc - key_hypothesis.tonic_pc) % 12
                )
            else:
                minor_functions = {
                    0: 'i',
                    2: 'ii°',
                    3: 'III',
                    5: 'iv',
                    7: 'V',
                    8: 'VI',
                    10: 'VII',
                }
                previous_functional_label = minor_functions.get(
                    (previous_root_pc - key_hypothesis.tonic_pc) % 12
                )

        cadence_label = detect_cadence_label(
            previous_functional_label=previous_functional_label,
            current_functional_label=functional_label,
        )

        return ContextAnalysisResult(
            context_winner=context_winner,
            ranked_candidates=ranked_candidates,
            key_hypothesis=key_hypothesis,
            functional_label=functional_label,
            cadence_label=cadence_label,
            movement_label=movement_label,
            explanation=f'Context analyzer: applied root movement bonus from previous root_pc={previous_root_pc}',
        )
        
