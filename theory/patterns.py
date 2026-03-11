CHORD_PATTERNS = {
    (0, 4, 7): '',        # major triad: A
    (0, 3, 7): 'm',       # minor triad: Am
    (0, 3, 6): 'dim',     # diminished triad: Adim
    (0, 4, 8): 'aug',     # augmented triad: Aaug
    (0, 2, 7): 'sus2',    # Asus2
    (0, 5, 7): 'sus4',    # Asus4
    (0, 2, 4): 'add2',    # Aadd2 (без квинты)
    (0, 4, 5): 'add4',    # Aadd4 (без квинты)
}


SIXTH_CHORD_PATTERNS = {
    (0, 4, 7, 9): '6',    # C6
    (0, 3, 7, 9): 'm6',   # Cm6
}


SEVENTH_CHORD_PATTERNS = {
    (0, 4, 7, 10): '7',        # dominant seventh
    (0, 4, 7, 11): 'maj7',     # major seventh
    (0, 3, 7, 10): 'm7',       # minor seventh
    (0, 3, 7, 11): 'm(maj7)',  # minor major seventh
    (0, 3, 6, 10): 'm7b5',     # half-diminished
    (0, 3, 6, 9): 'dim7',      # diminished seventh
    (0, 4, 8, 10): '7#5',      # augmented seventh
    (0, 4, 8, 11): 'maj7#5',   # augmented major seventh
    (0, 4, 6, 10): '7b5',      # dominant seventh flat five
    (0, 4, 6, 11): 'maj7b5',   # major seventh flat five
    (0, 5, 7, 10): '7sus4',    # suspended seventh
    (0, 2, 7, 10): '7sus2',    # suspended second seventh
}


EXTENDED_CHORD_PATTERNS = {
    # 9 chords
    (0, 2, 4, 7, 10): '9',
    (0, 2, 4, 7, 11): 'maj9',
    (0, 2, 3, 7, 10): 'm9',

    # add9 / 6/9
    (0, 2, 4, 7): 'add9',
    (0, 2, 4, 7, 9): '6/9',

    # altered dominant chords
    (0, 1, 4, 7, 10): '7b9',
    (0, 3, 4, 7, 10): '7#9',
    (0, 4, 6, 7, 10): '7#11',
    (0, 4, 7, 8, 10): '7b13',

    # 11 chords
    (0, 2, 4, 5, 7, 10): '11',
    (0, 2, 4, 5, 7, 11): 'maj11',
    (0, 2, 3, 5, 7, 10): 'm11',

    # maj7#11
    (0, 4, 6, 7, 11): 'maj7#11',

    # sus extensions
    (0, 2, 5, 7, 10): '9sus4',
    (0, 2, 5, 7, 9, 10): '13sus4',

    # 13 chords
    (0, 2, 4, 7, 9, 10): '13',
    (0, 2, 4, 7, 9, 11): 'maj13',
    (0, 2, 3, 7, 9, 10): 'm13',
}


INCOMPLETE_SEVENTH_CHORD_PATTERNS = [
    # Dominant 7
    {'suffix': '7(no5)', 'required': {0, 4, 10}, 'missing': {7}},
    {'suffix': '7(no3)', 'required': {0, 7, 10}, 'missing': {4}},
    {'suffix': '7(shell)', 'required': {0, 4, 10}, 'missing': {7}},

    # Major 7
    {'suffix': 'maj7(no5)', 'required': {0, 4, 11}, 'missing': {7}},
    {'suffix': 'maj7(no3)', 'required': {0, 7, 11}, 'missing': {4}},
    {'suffix': 'maj7(shell)', 'required': {0, 4, 11}, 'missing': {7}},

    # Minor 7
    {'suffix': 'm7(no5)', 'required': {0, 3, 10}, 'missing': {7}},
    {'suffix': 'm7(no3)', 'required': {0, 7, 10}, 'missing': {3}},
    {'suffix': 'm7(shell)', 'required': {0, 3, 10}, 'missing': {7}},

    # Minor-major 7
    {'suffix': 'm(maj7)(no5)', 'required': {0, 3, 11}, 'missing': {7}},
    {'suffix': 'm(maj7)(no3)', 'required': {0, 7, 11}, 'missing': {3}},

    # Half-diminished
    {'suffix': 'm7b5(no3)', 'required': {0, 6, 10}, 'missing': {3}},
    {'suffix': 'm7b5(no5)', 'required': {0, 3, 10}, 'missing': {6}},

    # Diminished 7
    {'suffix': 'dim7(no5)', 'required': {0, 3, 9}, 'missing': {6}},
    {'suffix': 'dim7(no3)', 'required': {0, 6, 9}, 'missing': {3}},
]


INCOMPLETE_EXTENDED_CHORD_PATTERNS = [
    {'suffix': 'add9', 'required': {0, 4, 2}, 'optional': {7}},
    {'suffix': '6/9', 'required': {0, 4, 2, 9}, 'optional': {7}},

    {'suffix': '9', 'required': {0, 4, 10, 2}, 'optional': {7}},
    {'suffix': 'maj9', 'required': {0, 4, 11, 2}, 'optional': {7}},
    {'suffix': 'm9', 'required': {0, 3, 10, 2}, 'optional': {7}},

    {'suffix': '11', 'required': {0, 4, 10, 5}, 'optional': {7, 2}},
    {'suffix': 'maj11', 'required': {0, 4, 11, 5}, 'optional': {7, 2}},
    {'suffix': 'm11', 'required': {0, 3, 10, 5}, 'optional': {7, 2}},

    {'suffix': 'maj7#11', 'required': {0, 4, 11, 6}, 'optional': {7}},

    {'suffix': '13', 'required': {0, 4, 10, 9}, 'optional': {7, 2}},
    {'suffix': 'maj13', 'required': {0, 4, 11, 9}, 'optional': {7, 2}},
    {'suffix': 'm13', 'required': {0, 3, 10, 9}, 'optional': {7, 2}},

    {'suffix': '9sus4', 'required': {0, 5, 10, 2}, 'optional': {7}},
    {'suffix': '13sus4', 'required': {0, 5, 10, 9}, 'optional': {7, 2}},

    {'suffix': '7b9', 'required': {0, 4, 10, 1}, 'optional': {7}},
    {'suffix': '7#9', 'required': {0, 4, 10, 3}, 'optional': {7}},
    {'suffix': '7#11', 'required': {0, 4, 10, 6}, 'optional': {7}},
    {'suffix': '7b13', 'required': {0, 4, 10, 8}, 'optional': {7}},
]
