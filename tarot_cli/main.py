"""CLI entry point for tarot_cli."""

from __future__ import annotations

import sys
from pathlib import Path

from rich.console import Console
from rich.align import Align

from tarot_cli.models import TarotCard
from tarot_cli.deck import DeckState
from tarot_cli.spreads import generate_1_card_reading
from tarot_cli import __version__

console = Console()


def _find_card(deck: list[TarotCard], name_parts: list[str]) -> TarotCard | None:
    """Find a card by its name parts (case-insensitive, split)."""
    search = [p.lower() for p in name_parts]
    for card in deck:
        if card["name"].lower().split() == search:
            return card
    return None


def _run_interactive() -> None:
    """Run the interactive REPL loop."""
    state = DeckState()
    deck = state.shuffle()

    console.print(
        Align.center(
            f"[bold cyan]Welcome to the tarot_cli![/bold cyan]\n"
            f"[italic]Type h or help to see available commands[/italic]"
        )
    )

    while True:
        try:
            user_input = input("tarot_cli> ")
        except EOFError:
            print("\n[cyan]The cards wait for another time...")
            break

        parts = user_input.lower().split()

        if len(parts) < 1:
            continue

        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else None

        match cmd:
            case "draw":
                if state.deck_size == 0:
                    print("There are [red]no more cards[/red] in the deck!")
                    continue
                if arg and arg.isdigit():
                    n = int(arg)
                    if state.deck_size < n:
                        print("[red]Not enough cards in the deck![/red]")
                        continue
                    for _ in range(n):
                        card, _ = state.draw_card()
                        is_reversed = bool(__import__("random").choice([True, False]))
                        state.print_card(card, is_reversed)
                else:
                    card, _ = state.draw_card()
                    is_reversed = bool(__import__("random").choice([True, False]))
                    state.print_card(card, is_reversed)

            case "deck":
                print(
                    f"There are [bold yellow]{state.deck_size} cards[/bold yellow] "
                    f"remaining in the deck"
                )

            case "shuffle":
                deck = state.shuffle()
                print("[green italic]Deck shuffled")

            case "drawn":
                if not state.drawn_cards:
                    print("[red]There are currently no drawn cards")
                    continue
                print("[italic]Drawn cards:")
                for card in state.drawn_cards:
                    state.print_card(card)

            case "meaning":
                if not arg:
                    print("Please specify a card name")
                    continue
                deck_list = state.create_deck()
                card_name = parts[1:-1] if parts[-1] == "reversed" else parts[1:]
                card = _find_card(deck_list, card_name)
                if card:
                    if parts[-1] == "reversed":
                        print(card["meaning_reversed"])
                    else:
                        print(card["meaning"])
                else:
                    print("[red]Invalid card name")

            case "inspect":
                if not arg:
                    print("Please specify a card name")
                    continue
                deck_list = state.create_deck()
                card_name = parts[1:-1] if parts[-1] == "reversed" else parts[1:]
                card = _find_card(deck_list, card_name)
                if card:
                    state.inspect(card)
                else:
                    print("[red]Invalid card name")

            case "reading":
                n = int(arg) if arg and arg.isdigit() else 1
                if state.deck_size < n:
                    print("[red]Not enough cards in the deck![/red]")
                    continue
                for _ in range(n):
                    card, _ = state.draw_card()
                    is_reversed = bool(__import__("random").choice([True, False]))
                    state.print_card(card, is_reversed)
                    print(generate_1_card_reading(card, is_reversed))

            case "daily":
                card, _ = state.daily()
                reading = generate_1_card_reading(card)
                state.print_card(card)
                print(reading)

            case "q" | "quit":
                print("[cyan]The cards wait for another time...")
                break

            case "h" | "help":
                print(state.help_text())

            case _:
                print("[red]unknown command")


def main() -> None:
    """Entry point for the CLI."""
    if len(sys.argv) > 1:
        match sys.argv[1]:
            case "--version" | "-V":
                print(__version__)
                return
            case "--help" | "-h":
                print("tarot_cli — A CLI for selecting and reading Tarot cards.")
                print()
                print("Usage: tarot_cli [command]")
                print()
                print("Commands:")
                print("  --version, -V  Show version")
                print("  --help, -h     Show this help")
                print("  (no args)      Start interactive mode")
                return
            case _:
                print(f"Unknown command: {sys.argv[1]}")
                print("Use --help for usage information.")
                sys.exit(1)
    else:
        _run_interactive()


if __name__ == "__main__":
    main()
