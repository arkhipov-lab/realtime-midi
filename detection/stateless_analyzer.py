from typing import List

from models.stateless_analysis import StatelessAnalysis
from detection.candidate_builder import build_chord_candidates


def analyze_notes_stateless(notes: List[int]) -> StatelessAnalysis:
    unique_notes = sorted(set(notes))
    candidates = build_chord_candidates(unique_notes)

    ranked_candidates = sorted(
        candidates,
        key=lambda c: (
            c.score,
            len(set(n % 12 for n in c.used_notes)),
            -c.ignored_notes_count,
            0 if not c.is_slash else -1,
        ),
        reverse=True,
    )

    stateless_winner = ranked_candidates[0] if ranked_candidates else None
    bass_note = min(unique_notes) if unique_notes else None
    highest_note = max(unique_notes) if unique_notes else None

    return StatelessAnalysis(
        notes=unique_notes,
        candidates=candidates,
        ranked_candidates=ranked_candidates,
        stateless_winner=stateless_winner,
        bass_note=bass_note,
        highest_note=highest_note,
    )
    
