from typing import List, Dict
from itertools import combinations

from models.chord_candidate import ChordCandidate

from .special import detect_chord_from_notes
from .subsets import generate_pitch_class_subsets

from scoring.candidate_scoring import score_chord_candidate


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


def build_chord_candidates(notes: List[int]) -> List[ChordCandidate]:
    sorted_notes = sorted(set(notes))
    if len(sorted_notes) < 2:
        return []

    bass_note = min(sorted_notes)
    candidates: List[ChordCandidate] = []
    seen: set[tuple[str, int, tuple[int, ...], bool, int]] = set()

    # 1. Полный набор как кандидат
    detected_full = detect_chord_from_notes(sorted_notes)
    if detected_full:
        chord_name, root_pc, pattern = detected_full
        full_is_slash = (bass_note % 12) != root_pc

        score = score_chord_candidate(
            chord_name=chord_name,
            root_pc=root_pc,
            pattern=pattern,
            used_notes=sorted_notes,
            full_notes=sorted_notes,
            bass_note=bass_note,
            is_slash=full_is_slash,
        )
        key = (chord_name, root_pc, pattern, full_is_slash, bass_note % 12)
        if key not in seen:
            seen.add(key)
            candidates.append(ChordCandidate(
                chord_name=chord_name,
                root_pc=root_pc,
                pattern=pattern,
                used_notes=sorted_notes,
                full_notes=sorted_notes,
                bass_note=bass_note,
                is_slash=full_is_slash,
                ignored_notes_count=0,
                score=score,
            ))

    # 2. Полный набор без баса как slash-кандидат
    if len(sorted_notes) >= 4:
        upper_notes = sorted_notes[1:]
        detected_upper = detect_chord_from_notes(upper_notes)
        if detected_upper:
            chord_name, root_pc, pattern = detected_upper
            score = score_chord_candidate(
                chord_name=chord_name,
                root_pc=root_pc,
                pattern=pattern,
                used_notes=upper_notes,
                full_notes=sorted_notes,
                bass_note=bass_note,
                is_slash=True,
            )
            key = (chord_name, root_pc, pattern, True, bass_note % 12)
            if key not in seen:
                seen.add(key)
                candidates.append(ChordCandidate(
                    chord_name=chord_name,
                    root_pc=root_pc,
                    pattern=pattern,
                    used_notes=upper_notes,
                    full_notes=sorted_notes,
                    bass_note=bass_note,
                    is_slash=True,
                    ignored_notes_count=len(set(n % 12 for n in sorted_notes)) - len(set(n % 12 for n in upper_notes)),
                    score=score,
                ))

    # 3. Подмножества как ядра аккорда
    subsets = generate_pitch_class_subsets(sorted_notes)
    for subset_notes in subsets:
        detected = detect_chord_from_notes(subset_notes)
        if not detected:
            continue

        chord_name, root_pc, pattern = detected

        is_slash = (bass_note % 12) != root_pc

        score = score_chord_candidate(
            chord_name=chord_name,
            root_pc=root_pc,
            pattern=pattern,
            used_notes=subset_notes,
            full_notes=sorted_notes,
            bass_note=bass_note,
            is_slash=is_slash,
        )

        # Небольшой штраф за использование не полного набора как ядра
        full_pcs = set(n % 12 for n in sorted_notes)
        subset_pcs = set(n % 12 for n in subset_notes)
        omitted_count = len(full_pcs - subset_pcs)
        score -= omitted_count * 15

        key = (chord_name, root_pc, pattern, is_slash, bass_note % 12)
        if key in seen:
            continue

        seen.add(key)
        candidates.append(ChordCandidate(
            chord_name=chord_name,
            root_pc=root_pc,
            pattern=pattern,
            used_notes=subset_notes,
            full_notes=sorted_notes,
            bass_note=bass_note,
            is_slash=is_slash,
            ignored_notes_count=omitted_count,
            score=score,
        ))

    return candidates
