from typing import Optional

from context.cadence_label import detect_cadence_label
from context.functional_label import detect_functional_label
from models.chord_candidate import ChordCandidate
from models.context_score_breakdown import ContextScoreBreakdown
from models.key_hypothesis import KeyHypothesis


FUNCTION_WEIGHTS = {
    'I': 20,
    'i': 22,
    'V': 18,
    'v': 14,
    'IV': 10,
    'iv': 10,
    'vi': 8,
    'VI': 8,
    'ii': 8,
    'ii°': 8,
    'III': 6,
    'iii': 4,
    'VII': 4,
    'vii°': 4,
}

CADENCE_WEIGHTS = {
    'authentic-cadence': 28,
    'authentic-cadence-minor': 30,
    'plagal-motion': 14,
    'plagal-motion-minor': 14,
    'predominant-to-dominant': 12,
    'predominant-to-dominant-minor': 12,
    'deceptive-cadence': 10,
    'deceptive-cadence-minor': 10,
    'half-cadence': 10,
    'dominant-to-mediant': 6,
}


def build_context_score_breakdown(
    candidate: ChordCandidate,
    key_hypothesis: Optional[KeyHypothesis],
    previous_functional_label: Optional[str],
    movement_bonus: int,
) -> ContextScoreBreakdown:
    functional_bonus = 0
    cadence_bonus = 0

    if key_hypothesis is not None:
        functional_label = detect_functional_label(candidate, key_hypothesis)
        cadence_label = detect_cadence_label(previous_functional_label, functional_label)

        if functional_label is not None:
            functional_bonus = FUNCTION_WEIGHTS.get(functional_label, 0)

        if cadence_label is not None:
            cadence_bonus = CADENCE_WEIGHTS.get(cadence_label, 0)

    return ContextScoreBreakdown(
        base_score=candidate.score,
        movement_bonus=movement_bonus,
        functional_bonus=functional_bonus,
        cadence_bonus=cadence_bonus,
    )


def score_candidate_in_context(
    candidate: ChordCandidate,
    key_hypothesis: Optional[KeyHypothesis],
    previous_functional_label: Optional[str],
    movement_bonus: int = 0,
) -> int:
    breakdown = build_context_score_breakdown(
        candidate=candidate,
        key_hypothesis=key_hypothesis,
        previous_functional_label=previous_functional_label,
        movement_bonus=movement_bonus,
    )
    return breakdown.total_score

