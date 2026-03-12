from context.chord_probability import score_candidate_in_context
from models.chord_candidate import ChordCandidate
from models.key_hypothesis import KeyHypothesis


def make_candidate(name: str, root_pc: int) -> ChordCandidate:
    return ChordCandidate(
        chord_name=name,
        root_pc=root_pc,
        pattern=(0, 4, 7),
        used_notes=[60, 64, 67],
        full_notes=[60, 64, 67],
        bass_note=60,
        is_slash=False,
        ignored_notes_count=0,
        score=100,
    )


def test_score_candidate_in_context_prefers_tonic_in_c_major():
    key = KeyHypothesis(tonic_pc=0, mode='major', score=100)

    tonic = make_candidate('C', 0)
    mediant = make_candidate('E', 4)

    tonic_score = score_candidate_in_context(
        candidate=tonic,
        key_hypothesis=key,
        previous_functional_label=None,
    )
    mediant_score = score_candidate_in_context(
        candidate=mediant,
        key_hypothesis=key,
        previous_functional_label=None,
    )

    assert tonic_score > mediant_score


def test_score_candidate_in_context_rewards_deceptive_resolution():
    key = KeyHypothesis(tonic_pc=0, mode='major', score=100)

    vi = make_candidate('Am', 9)
    iii = make_candidate('Em', 4)

    vi_score = score_candidate_in_context(
        candidate=vi,
        key_hypothesis=key,
        previous_functional_label='V',
    )
    iii_score = score_candidate_in_context(
        candidate=iii,
        key_hypothesis=key,
        previous_functional_label='V',
    )

    assert vi_score > iii_score
    
