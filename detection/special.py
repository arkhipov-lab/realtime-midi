from typing import List, Tuple, Optional

from .basic import is_bass_in_chord


from theory.notes import midi_note_to_name, pitch_class_to_pretty_name
from formatting.chord_notes import format_detected_chord_notes

from .basic import (
    detect_power_chord,
    detect_chord,
    detect_quartal_chord,
    detect_ambiguous_voicing,
    detect_sixth_chord,
)

from .extended import (
    detect_extended_chord,
    detect_incomplete_extended_chord,
)

from .seventh import (
    detect_seventh_chord,
    detect_incomplete_seventh_chord,
)


def detect_any_chord(notes: List[int]) -> Optional[Tuple[str, int, Tuple[int, ...]]]:
    unique_pitch_classes = set(note % 12 for note in notes)

    if len(unique_pitch_classes) == 3:
        detected = detect_chord(notes)
        if detected:
            chord_name, root_pc, pattern = detected
            return chord_name, root_pc, pattern

    if len(unique_pitch_classes) == 4:
        detected = detect_seventh_chord(notes)
        if detected:
            chord_name, root_pc, pattern = detected
            return chord_name, root_pc, pattern

    if len(unique_pitch_classes) >= 5:
        detected = detect_extended_chord(notes)
        if detected:
            chord_name, root_pc, pattern = detected
            return chord_name, root_pc, pattern

    return None


def detect_non_chord_bass_slash_chord(notes: List[int]) -> Optional[Tuple[str, str]]:
    if len(notes) < 4:
        return None

    sorted_notes = sorted(set(notes))
    bass_note = sorted_notes[0]
    upper_notes = sorted_notes[1:]

    detected = detect_any_chord(upper_notes)
    if not detected:
        return None

    chord_name, root_pc, pattern = detected

    if is_bass_in_chord(root_pc, bass_note, pattern):
        return None

    upper_formatted = format_detected_chord_notes(upper_notes, root_pc, pattern)
    bass_formatted = midi_note_to_name(bass_note)
    bass_pc_name = pitch_class_to_pretty_name(bass_note % 12)

    formatted_notes = f'{bass_formatted} + {upper_formatted}'
    slash_name = f'{chord_name}/{bass_pc_name}'

    return formatted_notes, slash_name


def detect_chord_from_notes(notes: List[int]) -> Optional[Tuple[str, int, Tuple[int, ...]]]:
    unique_pitch_classes = sorted(set(note % 12 for note in notes))

    if len(unique_pitch_classes) == 2:
        return detect_power_chord(notes)

    if len(unique_pitch_classes) == 3:
        triad = detect_chord(notes)
        incomplete_seventh = detect_incomplete_seventh_chord(notes)
        quartal = detect_quartal_chord(notes)
        ambiguous = detect_ambiguous_voicing(notes)

        candidates = [c for c in (triad, incomplete_seventh, quartal, ambiguous) if c is not None]
        if not candidates:
            return None

        def local_score(item: Tuple[str, int, Tuple[int, ...]]) -> int:
            chord_name, _, pattern = item

            if chord_name.endswith('quartal'):
                return 18

            if any(tag in chord_name for tag in ('5add9', 'sus4(no3)', 'sus2sus4', 'cluster5')):
                return 16

            if any(tag in chord_name for tag in ('7(shell)', 'maj7(shell)', 'm7(shell)')):
                return 24

            if any(tag in chord_name for tag in (
                '7(no3)', '7(no5)',
                'maj7(no3)', 'maj7(no5)',
                'm7(no3)', 'm7(no5)',
                'm(maj7)(no3)', 'm(maj7)(no5)',
                'm7b5(no3)', 'm7b5(no5)',
                'dim7(no3)', 'dim7(no5)',
            )):
                return 22

            return len(pattern) + 30

        candidates.sort(key=local_score, reverse=True)
        return candidates[0]

    if len(unique_pitch_classes) == 4:
        sixth = detect_sixth_chord(notes)
        seventh = detect_seventh_chord(notes)
        extended = detect_extended_chord(notes)
        quartal = detect_quartal_chord(notes)

        candidates = [c for c in (sixth, seventh, extended, quartal) if c is not None]

        incomplete_extended = detect_incomplete_extended_chord(notes)
        if incomplete_extended:
            candidates.append(incomplete_extended)

        if not candidates:
            return None

        def local_score(item: Tuple[str, int, Tuple[int, ...]]) -> int:
            chord_name, root_pc, pattern = item
            bass_pc = min(notes) % 12

            score = 0

            if 'quartal' in chord_name:
                score += 18
            if 'add9' in chord_name:
                score += 42
            if 'maj7#11' in chord_name:
                score += 44
            if any(tag in chord_name for tag in ('7b9', '7#9', '7#11', '7b13', '9(', '11(', '13(')):
                score += 40
            if chord_name.endswith(('6', 'm6')):
                score += 35
            if chord_name.endswith(('maj7', 'm7', '7', 'dim7', 'm7b5', 'm(maj7)', '7#5', 'maj7#5', '7b5', 'maj7b5', '7sus4', '7sus2')):
                score += 30

            # Новый кусок: корень в басу важен
            if root_pc == bass_pc:
                score += 20

            return score

        # def local_score(item: Tuple[str, int, Tuple[int, ...]]) -> int:
        #     chord_name, _, pattern = item

        #     if 'quartal' in chord_name:
        #         return 18
        #     if 'add9' in chord_name:
        #         return 42
        #     if 'maj7#11' in chord_name:
        #         return 44
        #     if any(tag in chord_name for tag in ('7b9', '7#9', '7#11', '7b13', '9(', '11(', '13(')):
        #         return 40
        #     if chord_name.endswith(('maj7', 'm7', '7', 'dim7', 'm7b5', 'm(maj7)', '7#5', 'maj7#5', '7b5', 'maj7b5', '7sus4', '7sus2')):
        #         return 30
        #     if chord_name.endswith(('6', 'm6')):
        #         return 20

        #     return len(pattern)

        candidates.sort(key=local_score, reverse=True)
        return candidates[0]

    if len(unique_pitch_classes) >= 5:
        full_extended = detect_extended_chord(notes)
        quartal = detect_quartal_chord(notes)

        candidates = []
        if full_extended:
            candidates.append(full_extended)
        if quartal:
            candidates.append(quartal)

        incomplete_extended = detect_incomplete_extended_chord(notes)
        if incomplete_extended:
            candidates.append(incomplete_extended)

        if not candidates:
            return None

        def local_score(item: Tuple[str, int, Tuple[int, ...]]) -> int:
            chord_name, _, pattern = item

            if 'quartal' in chord_name:
                return 18
            if 'maj7#11' in chord_name:
                return 58
            if '13sus4' in chord_name:
                return 57
            if any(tag in chord_name for tag in ('7b9', '7#9', '7#11', '7b13')):
                return 55
            if '9sus4' in chord_name:
                return 53
            if '6/9' in chord_name:
                return 52
            if any(tag in chord_name for tag in ('maj13', 'm13', '13')):
                return 60
            if any(tag in chord_name for tag in ('maj11', 'm11', '11')):
                return 55
            if any(tag in chord_name for tag in ('maj9', 'm9', '9')):
                return 50

            return len(pattern)

        candidates.sort(key=local_score, reverse=True)
        return candidates[0]

    return None
