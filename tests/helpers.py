from detection.candidate_selector import choose_best_chord_candidate
from formatting.candidate_formatting import format_candidate_notes
from formatting.chord_name import format_candidate_chord_name


def detect_candidate(notes):
    return choose_best_chord_candidate(notes)


def detect_name(notes):
    candidate = choose_best_chord_candidate(notes)
    return None if candidate is None else format_candidate_chord_name(candidate)


def detect_notes(notes):
    candidate = choose_best_chord_candidate(notes)
    return None if candidate is None else format_candidate_notes(candidate)


