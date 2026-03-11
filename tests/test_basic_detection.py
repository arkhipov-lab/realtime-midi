import pytest

from detection.special import detect_chord_from_notes


def test_detect_major_triad():
    result = detect_chord_from_notes([60, 64, 67])  # C E G
    assert result == ('C', 0, (0, 4, 7))


def test_detect_minor_triad():
    result = detect_chord_from_notes([60, 63, 67])  # C Eb G
    assert result == ('Cm', 0, (0, 3, 7))


def test_detect_diminished_triad():
    result = detect_chord_from_notes([60, 63, 66])  # C Eb Gb
    assert result == ('Cdim', 0, (0, 3, 6))


def test_detect_augmented_triad():
    result = detect_chord_from_notes([60, 64, 68])  # C E G#
    assert result == ('Caug', 0, (0, 4, 8))


def test_detect_power_chord_two_pitch_classes():
    result = detect_chord_from_notes([36, 43])  # C G
    assert result == ('C5', 0, (0, 7))


def test_detect_dominant_seventh():
    result = detect_chord_from_notes([60, 64, 67, 70])  # C E G Bb
    assert result == ('C7', 0, (0, 4, 7, 10))


def test_detect_major_seventh():
    result = detect_chord_from_notes([60, 64, 67, 71])  # C E G B
    assert result == ('Cmaj7', 0, (0, 4, 7, 11))


def test_detect_minor_seventh():
    result = detect_chord_from_notes([60, 63, 67, 70])  # C Eb G Bb
    assert result == ('Cm7', 0, (0, 3, 7, 10))


def test_detect_major_ninth():
    result = detect_chord_from_notes([60, 64, 67, 71, 74])  # C E G B D
    assert result == ('Cmaj9', 0, (0, 2, 4, 7, 11))


def test_detect_add9():
    result = detect_chord_from_notes([60, 64, 67, 74])  # C E G D
    assert result == ('Cadd9', 0, (0, 2, 4, 7))


def test_detect_incomplete_dominant_seventh_shell():
    result = detect_chord_from_notes([55, 62, 65])  # G D F
    assert result is not None
    assert result[0] in ('G7(no3)', 'G7(shell)')


def test_detect_quartal():
    result = detect_chord_from_notes([60, 65, 70])  # C F Bb
    assert result == ('Fsus4', 5, (0, 5, 7))
    
