def get_chord_priority_bonus(chord_name: str) -> int:
    if any(tag in chord_name for tag in (
        '7(shell)', 'maj7(shell)', 'm7(shell)',
        '7(no3)', '7(no5)',
        'maj7(no3)', 'maj7(no5)',
        'm7(no3)', 'm7(no5)',
        'm(maj7)(no3)', 'm(maj7)(no5)',
        'm7b5(no3)', 'm7b5(no5)',
        'dim7(no3)', 'dim7(no5)',
    )):
        return 28

    if 'maj7#11' in chord_name:
        return 58

    if '13sus4' in chord_name:
        return 57

    if any(tag in chord_name for tag in ('7b9', '7#9', '7#11', '7b13')):
        return 55

    if '9sus4' in chord_name:
        return 53

    if any(tag in chord_name for tag in ('maj13', 'm13', '13')):
        return 60

    if any(tag in chord_name for tag in ('maj11', 'm11', '11')):
        return 55

    if '6/9' in chord_name:
        return 52

    if any(tag in chord_name for tag in ('maj9', 'm9', '9')):
        return 50

    if 'add9' in chord_name:
        return 36

    if any(tag in chord_name for tag in (
        'maj7', 'm7', 'dim7', 'm7b5', 'm(maj7)',
        '7#5', 'maj7#5', '7b5', 'maj7b5', '7sus4', '7sus2'
    )):
        return 25

    if chord_name.endswith('7'):
        return 25

    if chord_name.endswith('m6') or chord_name.endswith('6'):
        return 20

    if chord_name.endswith('quartal'):
        return 18

    if any(tag in chord_name for tag in ('5add9', 'sus4(no3)', 'sus2sus4', 'cluster5')):
        return 16

    if chord_name.endswith('5'):
        return 14

    return 0

