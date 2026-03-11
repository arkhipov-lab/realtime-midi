# from detection.candidate_selector import choose_best_chord_candidate
# from formatting.chord_name import format_candidate_chord_name
# from formatting.candidate_formatting import format_candidate_notes
# from debug.candidate_debug import debug_print_candidates

# notes = [36, 40, 43, 45]  # C2 E2 G2 A2

# candidate = choose_best_chord_candidate(notes)
# print(candidate)
# if candidate:
#     print(format_candidate_chord_name(candidate))
#     print(format_candidate_notes(candidate))

# debug_print_candidates(notes)

from detection.special import detect_chord_from_notes

print(detect_chord_from_notes([36, 40, 43, 45]))  # C E G A