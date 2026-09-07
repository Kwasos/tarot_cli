"""Deck management — create, draw, shuffle, and track cards."""

from __future__ import annotations

import json
import random
import time
from pathlib import Path
from typing import Iterator

from rich.console import Console
from rich.align import Align

from tarot_cli.models import TarotCard

console = Console()

# Card suit -> ANSI color mapping
_SUIT_COLORS: dict[str, str] = {
    "Cups": "red",
    "Pentacles": "green",
    "Swords": "blue",
    "Wands": "yellow",
}

# Major arcana get magenta
_DEFAULT_COLOR = "magenta"


def _card_color(card: TarotCard, is_reversed: bool) -> str:
    """Return the rich color string for a card."""
    suit = card.get("suit") or _DEFAULT_COLOR
    color = _SUIT_COLORS.get(suit, _DEFAULT_COLOR)
    return color


class DeckState:
    """Encapsulates the mutable state of the deck and drawn cards.

    This replaces the module-level ``drawn_cards`` list so that
    tests can create independent instances without leaking state.
    """

    def __init__(self, deck_path: str | Path = "cards/tarot.json") -> None:
        self._deck_path = Path(deck_path)
        self._deck: list[TarotCard] = []
        self._drawn: list[TarotCard] = []
        self._load_deck()

    # -- public helpers --------------------------------------------------

    @property
    def deck_size(self) -> int:
        return len(self._deck)

    @property
    def drawn_cards(self) -> list[TarotCard]:
        return list(self._drawn)

    def clear_drawn(self) -> None:
        """Clear the drawn-cards list without touching the deck."""
        self._drawn.clear()

    def reset_drawn(self) -> None:
        """Alias for ``clear_drawn`` for backwards compatibility."""
        self.clear_drawn()

    # -- deck operations -------------------------------------------------

    def _load_deck(self) -> None:
        """Load and parse the tarot JSON into the deck."""
        text = self._deck_path.read_text(encoding="utf-8")
        data = json.loads(text)
        self._deck = list(data["cards"])

    def create_deck(self) -> list[TarotCard]:
        """Return a copy of the current deck."""
        return list(self._deck)

    def draw_card(self) -> tuple[TarotCard, list[TarotCard]]:
        """Draw one card from the deck.

        Returns:
            A tuple of (drawn_card, remaining_deck).
        Raises:
            ValueError: if the deck is empty.
        """
        if not self._deck:
            raise ValueError("No more cards in the deck")
        index = random.randrange(len(self._deck))
        card = self._deck.pop(index)
        self._drawn.append(card)
        return card, self._deck

    def draw_cards(self, n: int) -> tuple[list[TarotCard], list[TarotCard]]:
        """Draw *n* cards from the deck.

        Returns:
            A tuple of (drawn_cards, remaining_deck).
        Raises:
            ValueError: if fewer than *n* cards remain.
        """
        if len(self._deck) < n:
            raise ValueError(f"Not enough cards in the deck (need {n}, have {len(self._deck)})")
        drawn: list[TarotCard] = []
        for _ in range(n):
            card, _ = self.draw_card()
            drawn.append(card)
        return drawn, self._deck

    def shuffle(self) -> list[TarotCard]:
        """Shuffle the deck and clear drawn cards.

        Returns:
            The shuffled deck.
        """
        self._load_deck()
        random.shuffle(self._deck)
        self._drawn.clear()
        return list(self._deck)

    # -- daily spread ----------------------------------------------------

    def daily(self) -> tuple[TarotCard, str]:
        """Return the deterministic daily card.

        Uses the current day-of-year + year as the random seed so the
        same card is drawn every day.
        """
        self._load_deck()
        date = time.localtime()
        seed_val = int(str(date.tm_yday) + str(date.tm_year))
        random.seed(seed_val)
        index = random.randrange(len(self._deck))
        card = self._deck.pop(index)
        # Re-seed to avoid polluting subsequent randomness
        t = 1000 * time.time()
        random.seed(int(t) % 2**32)
        return card, ""  # caller gets the reading from spreads module

    # -- printing --------------------------------------------------------

    @staticmethod
    def print_card(card: TarotCard, is_reversed: bool = False) -> None:
        """Print a card name with suit-appropriate color."""
        color = _card_color(card, is_reversed)
        suffix = " Reversed" if is_reversed else ""
        console.print(f"[{color}]{card['name']}{suffix}[/]")

    @staticmethod
    def inspect(card: TarotCard) -> None:
        """Print all details for a card."""
        print(f"""
    [bold]name:[/bold] {card['name']}
    [bold]number:[/bold] {card['number']}
    [bold]arcana:[/bold] {card['arcana']}
    [bold]suit:[/bold] {card['suit']}
    [bold]nouns:[/bold] {card['nouns']}
    [bold]adjectives:[/bold] {card['adjectives']}
    [bold]meaning:[/bold] {card['meaning']}
    [bold]nouns_reversed:[/bold] {card['nouns_reversed']}
    [bold]adjectives_reversed:[/bold] {card['adjectives_reversed']}
    [bold]meaning_reversed:[/bold] {card['meaning_reversed']}""")

    @staticmethod
    def help_text() -> str:
        """Return the help text as a string (for tests)."""
        lines = [
            "[bold cyan]Deck commands:[/bold cyan]",
            "  draw (X)     draw the specified number of cards",
            "  shuffle      return all cards to the deck",
            "  deck         display the current number of cards in the deck",
            "  drawn        display drawn cards, currently not in the deck",
            "  inspect      display all card details for the specified card",
            "  meaning      display the meaning of a card",
            "",
            "[bold magenta]Spreads:[/bold magenta]",
            "  daily        deterministic selection based on the current date",
            "  reading (X)  draw X cards with readings",
            "",
            "[bold bright_red]System commands:[/bold bright_red]",
            "  help | h     print this help text",
            "  quit | q     close the program",
        ]
        return "\n".join(lines)


# Module-level convenience functions for direct imports
def create_deck(deck_path: str | Path = "cards/tarot.json") -> list[TarotCard]:
    """Create and return a fresh deck."""
    state = DeckState(deck_path)
    return state.create_deck()


def draw_card(deck_path: str | Path = "cards/tarot.json") -> tuple[TarotCard, list[TarotCard]]:
    """Draw one card from a fresh deck."""
    state = DeckState(deck_path)
    return state.draw_card()


def shuffle_deck(deck_path: str | Path = "cards/tarot.json") -> list[TarotCard]:
    """Shuffle and return a fresh deck."""
    state = DeckState(deck_path)
    return state.shuffle()


def get_deck_size(deck_path: str | Path = "cards/tarot.json") -> int:
    """Return the number of cards in a fresh deck."""
    return len(DeckState(deck_path).create_deck())


def get_drawn_cards(deck_path: str | Path = "cards/tarot.json") -> list[TarotCard]:
    """Return the list of drawn cards from a fresh deck."""
    return DeckState(deck_path).drawn_cards


def clear_drawn_cards(deck_path: str | Path = "cards/tarot.json") -> None:
    """Clear the drawn cards from a fresh deck."""
    state = DeckState(deck_path)
    state.clear_drawn()


def reset_drawn_cards(deck_path: str | Path = "cards/tarot.json") -> None:
    """Reset drawn cards (alias for clear_drawn_cards)."""
    clear_drawn_cards(deck_path)
