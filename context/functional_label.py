from typing import Optional

from models.chord_candidate import ChordCandidate
from models.key_hypothesis import KeyHypothesis


MAJOR_FUNCTIONS = {
    0: 'I',
    2: 'ii',
    4: 'iii',
    5: 'IV',
    7: 'V',
    9: 'vi',
    11: 'vii°',
}

MINOR_FUNCTIONS = {
    0: 'i',
    2: 'ii°',
    3: 'III',
    5: 'iv',
    7: 'v',
    8: 'VI',
    10: 'VII',
}


def detect_functional_label(
    candidate: Optional[ChordCandidate],
    key_hypothesis: Optional[KeyHypothesis],
) -> Optional[str]:
    if candidate is None or key_hypothesis is None:
        return None

    degree = (candidate.root_pc - key_hypothesis.tonic_pc) % 12

    if key_hypothesis.mode == 'major':
        return MAJOR_FUNCTIONS.get(degree)

    return MINOR_FUNCTIONS.get(degree)

