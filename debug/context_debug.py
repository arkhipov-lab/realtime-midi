from models.context_analysis import ContextAnalysisResult
from theory.notes import pitch_class_to_name


def format_key_hypothesis(key_hypothesis) -> str:
    if key_hypothesis is None:
        return 'None'
    tonic = pitch_class_to_name(key_hypothesis.tonic_pc)
    return f'{tonic} {key_hypothesis.mode} ({key_hypothesis.score})'


def print_context_result(result: ContextAnalysisResult) -> None:
    print('DEBUG: ===== CONTEXT RESULT =====')

    if result.context_winner is not None:
        print(f'DEBUG: context_winner = {result.context_winner.chord_name} ({result.context_winner.score})')
    else:
        print('DEBUG: context_winner = None')

    if result.ranked_candidates:
        formatted = ', '.join(
            f'{candidate.chord_name}({candidate.score})'
            for candidate in result.ranked_candidates[:3]
        )
        print(f'DEBUG: context_top3 = [{formatted}]')
    else:
        print('DEBUG: context_top3 = []')

    print(f'DEBUG: key_hypothesis = {format_key_hypothesis(result.key_hypothesis)}')
    print(f'DEBUG: functional_label = {result.functional_label}')
    print(f'DEBUG: cadence_label = {result.cadence_label}')
    print(f'DEBUG: movement_label = {result.movement_label}')
    print(f'DEBUG: explanation = {result.explanation}')
    print('DEBUG: ==========================\n')
    
