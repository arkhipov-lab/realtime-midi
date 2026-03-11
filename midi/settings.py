import json
from pathlib import Path

SETTINGS_FILE = Path.home() / ".midi_chord_detector.json"


def load_settings() -> dict:
    if not SETTINGS_FILE.exists():
        return {}

    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}


def save_settings(data: dict) -> None:
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)
        
