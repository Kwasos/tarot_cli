"""Tests for the spreads module."""

import re

from tarot_cli.models import TarotCard
from tarot_cli.spreads import (
    generate_1_card_reading,
    generate_daily_reading,
    _pick_two,
)


def _make_card(
    name: str = "The Fool",
    nouns: list[str] | None = None,
    adjectives: list[str] | None = None,
    meaning: str = "New beginnings",
    is_reversed: bool = False,
) -> TarotCard:
    """Helper to create a test card."""
    nouns = nouns or ["beginnings", "innocence", "adventure"]
    adjectives = adjectives or ["free", "innocent", "spontaneous"]
    return TarotCard(
        name=name,
        number="0",
        arcana="Major",
        suit=None,
        nouns=nouns,
        adjectives=adjectives,
        meaning=meaning,
        nouns_reversed=["recklessness", "gullibility", "foolishness"],
        adjectives_reversed=["reckless", "gullible", "foolish"],
        meaning_reversed="Recklessness",
    )


class TestPickTwo:
    """Test _pick_two helper."""

    def test_picks_two_distinct(self) -> None:
        items = ["a", "b", "c"]
        for _ in range(100):
            first, second = _pick_two(items)
            assert first != second

    def test_picks_from_list(self) -> None:
        items = ["a", "b"]
        first, second = _pick_two(items)
        assert first in items
        assert second in items

    def test_single_item_returns_same(self) -> None:
        items = ["a"]
        first, second = _pick_two(items)
        assert first == "a"
        assert second == "a"


class TestGenerateDailyReading:
    """Test daily reading generation."""

    def test_returns_string(self) -> None:
        card = _make_card()
        reading = generate_daily_reading(card)
        assert isinstance(reading, str)
        assert len(reading) > 0

    def test_contains_meaning(self) -> None:
        card = _make_card(meaning="Unique meaning here")
        for _ in range(20):
            reading = generate_daily_reading(card)
            assert "Unique meaning here" in reading

    def test_upright(self) -> None:
        card = _make_card()
        for _ in range(20):
            reading = generate_daily_reading(card, is_reversed=False)
            assert "New beginnings" in reading

    def test_reversed(self) -> None:
        card = _make_card()
        for _ in range(20):
            reading = generate_daily_reading(card, is_reversed=True)
            assert "Recklessness" in reading
            assert "New beginnings" not in reading

    def test_uses_nouns(self) -> None:
        card = _make_card(nouns=["courage", "wisdom"])
        for _ in range(50):
            reading = generate_daily_reading(card)
            # Each template uses at least one noun
            assert "courage" in reading or "wisdom" in reading


class TestGenerate1CardReading:
    """Test 1-card reading generation."""

    def test_returns_string(self) -> None:
        card = _make_card()
        reading = generate_1_card_reading(card)
        assert isinstance(reading, str)
        assert len(reading) > 0

    def test_uses_nouns(self) -> None:
        card = _make_card(nouns=["love", "change"])
        for _ in range(50):
            reading = generate_1_card_reading(card)
            assert "love" in reading or "change" in reading

    def test_uses_adjectives(self) -> None:
        card = _make_card(adjectives=["bold", "gentle"])
        for _ in range(50):
            reading = generate_1_card_reading(card)
            assert "bold" in reading or "gentle" in reading

    def test_reversed(self) -> None:
        card = _make_card()
        for _ in range(20):
            reading = generate_1_card_reading(card, is_reversed=True)
            # Reversed readings use nouns_reversed/adjectives_reversed
            # Templates randomly pick from them, so check at least one reversed keyword appears
            keywords = ["recklessness", "reckless", "foolishness", "foolish",
                        "gullibility", "gullible"]
            assert any(kw in reading.lower() for kw in keywords)

    def test_variety(self) -> None:
        """Test that multiple readings produce different templates."""
        card = _make_card(nouns=["a", "b", "c"], adjectives=["x", "y", "z"])
        readings = [generate_1_card_reading(card) for _ in range(100)]
        unique = set(readings)
        assert len(unique) > 1  # at least some variety
