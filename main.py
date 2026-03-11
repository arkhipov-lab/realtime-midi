from config import DEBUG_MODE
from debug.candidate_debug import debug_print_candidates, debug_print_winner
from midi.ports import choose_midi_port
from midi.runtime import run_midi_listener


def debug_callback(notes, best_candidate) -> None:
    if DEBUG_MODE:
        debug_print_candidates(notes)
        debug_print_winner(best_candidate)


def main() -> None:
    port_name = choose_midi_port()
    print(f'\nСлушаю порт: {port_name}\n')
    run_midi_listener(
        port_name=port_name,
        debug_callback=debug_callback if DEBUG_MODE else None,
    )


if __name__ == '__main__':
    main()
    
    
    