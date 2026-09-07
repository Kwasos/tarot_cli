"""Tests for the DeckState class."""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from tarot_cli.deck import DeckState
from tarot_cli.models import TarotCard


def _make_tarot_json(cards: list[dict]) -> str:
    """Create a minimal tarot.json string."""
    return json.dumps({"cards": cards})


class TestDeckStateInit:
    """Test DeckState initialization."""

    def test_loads_deck(self, tmp_path: Path) -> None:
        json_file = tmp_path / "tarot.json"
        json_file.write_text(_make_tarot_json([
            {"name": "The Fool", "number": "0", "arcana": "Major", "suit": None,
             "nouns": [], "adjectives": [], "meaning": "",
             "nouns_reversed": [], "adjectives_reversed": [], "meaning_reversed": ""},
        ]))
        state = DeckState(json_file)
        assert state.deck_size == 1

    def test_deck_size_matches_json(self, tmp_path: Path) -> None:
        cards = [
            {"name": f"Card {i}", "number": str(i), "arcana": "Major", "suit": None,
             "nouns": [], "adjectives": [], "meaning": "",
             "nouns_reversed": [], "adjectives_reversed": [], "meaning_reversed": ""}
            for i in range(22)
        ]
        json_file = tmp_path / "tarot.json"
        json_file.write_text(_make_tarot_json(cards))
        state = DeckState(json_file)
        assert state.deck_size == 22


class TestDrawCard:
    """Test card drawing."""

    def test_draw_returns_card(self, tmp_path: Path) -> None:
        cards = [
            {"name": f"Card {i}", "number": str(i), "arcana": "Major", "suit": None,
             "nouns": [], "adjectives": [], "meaning": "",
             "nouns_reversed": [], "adjectives_reversed": [], "meaning_reversed": ""}
            for i in range(5)
        ]
        json_file = tmp_path / "tarot.json"
        json_file.write_text(_make_tarot_json(cards))
        state = DeckState(json_file)
        card, remaining = state.draw_card()
        assert card["name"] in [f"Card {i}" for i in range(5)]
        assert len(remaining) == 4

    def test_draw_decreases_deck_size(self, tmp_path: Path) -> None:
        cards = [
            {"name": f"Card {i}", "number": str(i), "arcana": "Major", "suit": None,
             "nouns": [], "adjectives": [], "meaning": "",
             "nouns_reversed": [], "adjectives_reversed": [], "meaning_reversed": ""}
            for i in range(5)
        ]
        json_file = tmp_path / "tarot.json"
        json_file.write_text(_make_tarot_json(cards))
        state = DeckState(json_file)
        state.draw_card()
        assert state.deck_size == 4

    def test_draw_raises_on_empty_deck(self, tmp_path: Path) -> None:
        json_file = tmp_path / "tarot.json"
        json_file.write_text(_make_tarot_json([]))
        state = DeckState(json_file)
        with pytest.raises(ValueError, match="No more cards"):
            state.draw_card()

    def test_drawn_cards_tracked(self, tmp_path: Path) -> None:
        cards = [
            {"name": f"Card {i}", "number": str(i), "arcana": "Major", "suit": None,
             "nouns": [], "adjectives": [], "meaning": "",
             "nouns_reversed": [], "adjectives_reversed": [], "meaning_reversed": ""}
            for i in range(5)
        ]
        json_file = tmp_path / "tarot.json"
        json_file.write_text(_make_tarot_json(cards))
        state = DeckState(json_file)
        state.draw_card()
        state.draw_card()
        assert len(state.drawn_cards) == 2

    def test_drawn_cards_returns_copy(self, tmp_path: Path) -> None:
        cards = [
            {"name": f"Card {i}", "number": str(i), "arcana": "Major", "suit": None,
             "nouns": [], "adjectives": [], "meaning": "",
             "nouns_reversed": [], "adjectives_reversed": [], "meaning_reversed": ""}
            for i in range(5)
        ]
        json_file = tmp_path / "tarot.json"
        json_file.write_text(_make_tarot_json(cards))
        state = DeckState(json_file)
        drawn = state.drawn_cards
        drawn.append("fake")  # should not affect state
        assert len(state.drawn_cards) == 0


class TestDrawCards:
    """Test drawing multiple cards."""

    def test_draw_multiple(self, tmp_path: Path) -> None:
        cards = [
            {"name": f"Card {i}", "number": str(i), "arcana": "Major", "suit": None,
             "nouns": [], "adjectives": [], "meaning": "",
             "nouns_reversed": [], "adjectives_reversed": [], "meaning_reversed": ""}
            for i in range(10)
        ]
        json_file = tmp_path / "tarot.json"
        json_file.write_text(_make_tarot_json(cards))
        state = DeckState(json_file)
        drawn, remaining = state.draw_cards(3)
        assert len(drawn) == 3
        assert len(remaining) == 7

    def test_draw_exceeds_raises(self, tmp_path: Path) -> None:
        cards = [
            {"name": f"Card {i}", "number": str(i), "arcana": "Major", "suit": None,
             "nouns": [], "adjectives": [], "meaning": "",
             "nouns_reversed": [], "adjectives_reversed": [], "meaning_reversed": ""}
            for i in range(3)
        ]
        json_file = tmp_path / "tarot.json"
        json_file.write_text(_make_tarot_json(cards))
        state = DeckState(json_file)
        with pytest.raises(ValueError, match="Not enough cards"):
            state.draw_cards(5)


class TestShuffle:
    """Test deck shuffling."""

    def test_shuffle_resets_deck(self, tmp_path: Path) -> None:
        cards = [
            {"name": f"Card {i}", "number": str(i), "arcana": "Major", "suit": None,
             "nouns": [], "adjectives": [], "meaning": "",
             "nouns_reversed": [], "adjectives_reversed": [], "meaning_reversed": ""}
            for i in range(5)
        ]
        json_file = tmp_path / "tarot.json"
        json_file.write_text(_make_tarot_json(cards))
        state = DeckState(json_file)
        state.draw_card()
        assert state.deck_size == 4
        state.shuffle()
        assert state.deck_size == 5

    def test_shuffle_clears_drawn(self, tmp_path: Path) -> None:
        cards = [
            {"name": f"Card {i}", "number": str(i), "arcana": "Major", "suit": None,
             "nouns": [], "adjectives": [], "meaning": "",
             "nouns_reversed": [], "adjectives_reversed": [], "meaning_reversed": ""}
            for i in range(5)
        ]
        json_file = tmp_path / "tarot.json"
        json_file.write_text(_make_tarot_json(cards))
        state = DeckState(json_file)
        state.draw_card()
        assert len(state.drawn_cards) == 1
        state.shuffle()
        assert len(state.drawn_cards) == 0


class TestCreateDeck:
    """Test creating a deck copy."""

    def test_create_deck_returns_copy(self, tmp_path: Path) -> None:
        cards = [
            {"name": f"Card {i}", "number": str(i), "arcana": "Major", "suit": None,
             "nouns": [], "adjectives": [], "meaning": "",
             "nouns_reversed": [], "adjectives_reversed": [], "meaning_reversed": ""}
            for i in range(5)
        ]
        json_file = tmp_path / "tarot.json"
        json_file.write_text(_make_tarot_json(cards))
        state = DeckState(json_file)
        deck = state.create_deck()
        assert len(deck) == 5
        assert deck is not state._deck  # different object


class TestClearDrawn:
    """Test clearing drawn cards."""

    def test_clear_drawn(self, tmp_path: Path) -> None:
        cards = [
            {"name": f"Card {i}", "number": str(i), "arcana": "Major", "suit": None,
             "nouns": [], "adjectives": [], "meaning": "",
             "nouns_reversed": [], "adjectives_reversed": [], "meaning_reversed": ""}
            for i in range(5)
        ]
        json_file = tmp_path / "tarot.json"
        json_file.write_text(_make_tarot_json(cards))
        state = DeckState(json_file)
        state.draw_card()
        assert len(state.drawn_cards) == 1
        state.clear_drawn()
        assert len(state.drawn_cards) == 0

    def test_reset_drawn_alias(self, tmp_path: Path) -> None:
        cards = [
            {"name": f"Card {i}", "number": str(i), "arcana": "Major", "suit": None,
             "nouns": [], "adjectives": [], "meaning": "",
             "nouns_reversed": [], "adjectives_reversed": [], "meaning_reversed": ""}
            for i in range(5)
        ]
        json_file = tmp_path / "tarot.json"
        json_file.write_text(_make_tarot_json(cards))
        state = DeckState(json_file)
        state.draw_card()
        assert len(state.drawn_cards) == 1
        state.reset_drawn()
        assert len(state.drawn_cards) == 0


class TestPrintCard:
    """Test card printing."""

    def test_print_card_upright(self, tmp_path: Path) -> None:
        card = TarotCard(
            name="Three of Cups",
            number="3",
            arcana="Minor",
            suit="Cups",
            nouns=[],
            adjectives=[],
            meaning="",
            nouns_reversed=[],
            adjectives_reversed=[],
            meaning_reversed="",
        )
        with patch("tarot_cli.deck.console.print") as mock_print:
            DeckState.print_card(card, is_reversed=False)
            mock_print.assert_called_once()
            assert "Three of Cups" in mock_print.call_args[0][0]

    def test_print_card_reversed(self, tmp_path: Path) -> None:
        card = TarotCard(
            name="Three of Cups",
            number="3",
            arcana="Minor",
            suit="Cups",
            nouns=[],
            adjectives=[],
            meaning="",
            nouns_reversed=[],
            adjectives_reversed=[],
            meaning_reversed="",
        )
        with patch("tarot_cli.deck.console.print") as mock_print:
            DeckState.print_card(card, is_reversed=True)
            mock_print.assert_called_once()
            assert "Reversed" in mock_print.call_args[0][0]

    def test_print_card_major_arcana(self, tmp_path: Path) -> None:
        card = TarotCard(
            name="The Fool",
            number="0",
            arcana="Major",
            suit=None,
            nouns=[],
            adjectives=[],
            meaning="",
            nouns_reversed=[],
            adjectives_reversed=[],
            meaning_reversed="",
        )
        with patch("tarot_cli.deck.console.print") as mock_print:
            DeckState.print_card(card)
            mock_print.assert_called_once()


class TestHelpText:
    """Test help text generation."""

    def test_help_text_contains_commands(self) -> None:
        text = DeckState.help_text()
        assert "draw" in text
        assert "shuffle" in text
        assert "deck" in text
        assert "quit" in text
        assert "help" in text
