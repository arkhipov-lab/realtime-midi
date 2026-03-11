from typing import Tuple


INTERVAL_NAMES = {
    0: 'чистая прима',
    1: 'малая секунда',
    2: 'большая секунда',
    3: 'малая терция',
    4: 'большая терция',
    5: 'чистая кварта',
    6: 'тритон',
    7: 'чистая квинта',
    8: 'малая секста',
    9: 'большая секста',
    10: 'малая септима',
    11: 'большая септима',
    12: 'чистая октава',
}


def get_interval_name(note1: int, note2: int) -> str:
    low = min(note1, note2)
    high = max(note1, note2)
    semitones = high - low

    if semitones <= 12:
        return INTERVAL_NAMES.get(semitones, f'{semitones} полутонов')

    octaves = semitones // 12
    remainder = semitones % 12

    if remainder == 0:
        if octaves == 1:
            return 'чистая октава'
        return f'{octaves} октавы'

    base_name = INTERVAL_NAMES.get(remainder, f'{remainder} полутонов')
    return f'{base_name} + {octaves} окт.'


def interval_to_missing_label(interval: int, chord_suffix: str) -> str:
    if interval == 7:
        return '5'
    if interval == 2:
        return '9'
    if interval == 5:
        return '11'
    if interval == 9:
        return '13' if '13' in chord_suffix else '6'
    if interval == 1:
        return 'b9'
    if interval == 3:
        if '7#9' in chord_suffix:
            return '#9'
        return 'b3'
    if interval == 4:
        return '3'
    if interval == 6:
        return '#11' if '#11' in chord_suffix else 'b5'
    if interval == 8:
        return 'b13'
    if interval == 10:
        return 'b7'
    if interval == 11:
        return '7'
    return str(interval)


def get_triad_inversion(root_pc: int, bass_note: int, pattern: Tuple[int, int, int]) -> str:
    bass_pc = bass_note % 12
    intervals_in_chord = {(root_pc + interval) % 12: interval for interval in pattern}

    bass_interval = intervals_in_chord.get(bass_pc)
    if bass_interval is None:
        return 'unknown'

    if bass_interval == 0:
        return 'root position'
    if bass_interval in (3, 4):
        return '1st inversion'
    if bass_interval == 7:
        return '2nd inversion'

    return 'unknown'

