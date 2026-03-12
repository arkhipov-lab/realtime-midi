from typing import Optional


def detect_cadence_label(
    previous_functional_label: Optional[str],
    current_functional_label: Optional[str],
) -> Optional[str]:
    if previous_functional_label is None or current_functional_label is None:
        return None

    # Authentic cadence
    if previous_functional_label == 'V' and current_functional_label == 'I':
        return 'authentic-cadence'

    if previous_functional_label == 'V' and current_functional_label == 'i':
        return 'authentic-cadence-minor'

    # Plagal motion
    if previous_functional_label == 'IV' and current_functional_label == 'I':
        return 'plagal-motion'

    if previous_functional_label == 'iv' and current_functional_label == 'i':
        return 'plagal-motion-minor'

    # Predominant -> Dominant
    if previous_functional_label == 'ii' and current_functional_label == 'V':
        return 'predominant-to-dominant'

    if previous_functional_label == 'iv' and current_functional_label == 'V':
        return 'predominant-to-dominant-minor'

    # Deceptive cadence
    if previous_functional_label == 'V' and current_functional_label == 'vi':
        return 'deceptive-cadence'

    if previous_functional_label == 'V' and current_functional_label == 'VI':
        return 'deceptive-cadence-minor'

    return None
