"""tarot_cli — A CLI for selecting and reading Tarot cards."""

__version__ = "0.1.0"

from tarot_cli.models import TarotCard
from tarot_cli.deck import (
    create_deck,
    draw_card,
    shuffle_deck,
    get_deck_size,
    get_drawn_cards,
    clear_drawn_cards,
    reset_drawn_cards,
)
from tarot_cli.spreads import generate_daily_reading, generate_1_card_reading

__all__ = [
    "TarotCard",
    "create_deck",
    "draw_card",
    "shuffle_deck",
    "get_deck_size",
    "get_drawn_cards",
    "clear_drawn_cards",
    "reset_drawn_cards",
    "generate_daily_reading",
    "generate_1_card_reading",
]
