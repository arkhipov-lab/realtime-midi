NOTE_NAMES_SHARP = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
NOTE_NAMES_FLAT = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']


def midi_note_to_name(note: int) -> str:
    octave = (note // 12) - 1
    name = NOTE_NAMES_SHARP[note % 12]
    return f'{name}{octave}'


def pitch_class_to_name(pc: int) -> str:
    return NOTE_NAMES_SHARP[pc % 12]


def pitch_class_to_pretty_name(pc: int) -> str:
    return NOTE_NAMES_SHARP[pc % 12]
