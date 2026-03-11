from typing import List, Optional

from models.chord_candidate import ChordCandidate
from .candidate_builder import build_chord_candidates


def choose_best_chord_candidate(notes: List[int]) -> Optional[ChordCandidate]:
    candidates = build_chord_candidates(notes)
    if not candidates:
        return None

    candidates.sort(
        key=lambda c: (
            c.score,
            len(set(n % 12 for n in c.used_notes)),
            -c.ignored_notes_count,
            0 if not c.is_slash else -1,
        ),
        reverse=True,
    )
    return candidates[0]

