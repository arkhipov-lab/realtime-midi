import re


def simplify_chord_name(chord_name: str) -> str:
    # Убираем все (...) с noX внутри
    simplified = re.sub(r'\(no[^)]*\)', '', chord_name)

    # На случай лишних пробелов
    simplified = simplified.strip()

    return simplified

