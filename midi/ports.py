import mido

from .settings import load_settings, save_settings


def choose_midi_port() -> str:
    input_names = mido.get_input_names()

    if not input_names:
        raise RuntimeError("MIDI input-порты не найдены")

    settings = load_settings()
    last_port = settings.get("last_midi_port")

    print("Доступные MIDI input-порты:")

    default_index = 0

    for i, name in enumerate(input_names):
        marker = ""
        if name == last_port:
            marker = " (last used)"
            default_index = i
        print(f"{i}: {name}{marker}")

    raw = input(f"\nВыбери MIDI input-порт [Enter = {default_index}]: ").strip()

    if raw == "":
        selected_index = default_index
    else:
        try:
            selected_index = int(raw)
        except ValueError:
            raise RuntimeError(f"Некорректный индекс порта: {raw}")

    if selected_index < 0 or selected_index >= len(input_names):
        raise RuntimeError(f"Индекс вне диапазона: {selected_index}")

    port_name = input_names[selected_index]

    save_settings({"last_midi_port": port_name})

    return port_name


