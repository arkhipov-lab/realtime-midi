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


def get_context_confidence_multiplier(candidate: ChordCandidate) -> float:
    chord_name = candidate.chord_name

    if chord_name.endswith('5'):
        return 0.35

    if '(no' in chord_name:
        return 0.8

    if chord_name.endswith('sus2') or chord_name.endswith('sus4'):
        return 0.78

    if any(tag in chord_name for tag in ('sus4(no3)', 'sus2sus4', 'cluster5', '5add9')):
        return 0.65

    return 1.0


def build_context_score_breakdown(
    candidate: ChordCandidate,
    key_hypothesis: Optional[KeyHypothesis],
    previous_functional_label: Optional[str],
    movement_bonus: int,
) -> ContextScoreBreakdown:
    functional_bonus = 0
    cadence_bonus = 0

    multiplier = get_context_confidence_multiplier(candidate)
    adjusted_movement_bonus = int(round(movement_bonus * multiplier))

    if key_hypothesis is not None:
        functional_label = detect_functional_label(candidate, key_hypothesis)
        cadence_label = detect_cadence_label(previous_functional_label, functional_label)

        if functional_label is not None:
            raw_functional_bonus = FUNCTION_WEIGHTS.get(functional_label, 0)
            functional_bonus = int(round(raw_functional_bonus * multiplier))

        if cadence_label is not None:
            raw_cadence_bonus = CADENCE_WEIGHTS.get(cadence_label, 0)
            cadence_bonus = int(round(raw_cadence_bonus * multiplier))

    return ContextScoreBreakdown(
        base_score=candidate.score,
        movement_bonus=adjusted_movement_bonus,
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

