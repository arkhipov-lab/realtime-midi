from typing import List, Dict
from itertools import combinations
from typing import List


def get_pitch_class_note_map(notes: List[int]) -> Dict[int, int]:
    pc_map: Dict[int, int] = {}
    for note in sorted(set(notes)):
        pc = note % 12
        if pc not in pc_map:
            pc_map[pc] = note
    return pc_map


def generate_pitch_class_subsets(notes: List[int]) -> List[List[int]]:
    unique_notes = sorted(set(notes))
    pc_map = get_pitch_class_note_map(unique_notes)
    pitch_classes = sorted(pc_map.keys())

    subsets: List[List[int]] = []

    max_subset_size = min(len(pitch_classes), 6)
    for size in range(2, max_subset_size + 1):
        for combo in combinations(pitch_classes, size):
            subset_notes = [pc_map[pc] for pc in combo]
            subsets.append(sorted(subset_notes))

    return subsets


