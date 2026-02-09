"""
Application entry point.
"""


"""
Minimal end-to-end demo runner.
"""

from app.orchestrator import process_turn


def main() -> None:
    print("\n=== Long-Term Memory System Demo ===\n")

    turn_id = 1

    while True:
        user_input = input(f"\n[Turn {turn_id}] You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        assistant_output = process_turn(
            user_message=user_input,
            turn_id=turn_id
        )

        print("\nAssistant:\n")
        print(assistant_output)

        turn_id += 1


if __name__ == "__main__":
    main()
