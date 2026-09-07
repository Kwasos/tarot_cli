"""Tests for the TarotCard model."""

from tarot_cli.models import TarotCard


class TestTarotCard:
    """Test the TarotCard dict subclass."""

    def test_creation(self) -> None:
        card = TarotCard(
            name="The Fool",
            number="0",
            arcana="Major",
            suit=None,
            nouns=["beginnings", "innocence"],
            adjectives=["free", "innocent"],
            meaning="New beginnings, innocence, spontaneity",
            nouns_reversed=["recklessness", "gullibility"],
            adjectives_reversed=["reckless", "gullible"],
            meaning_reversed="Recklessness, gullibility, foolishness",
        )
        assert card["name"] == "The Fool"
        assert card.name == "The Fool"
        assert card.arcana == "Major"

    def test_properties(self) -> None:
        card = TarotCard(
            name="The Fool",
            number="0",
            arcana="Major",
            suit=None,
            nouns=["beginnings", "innocence"],
            adjectives=["free", "innocent"],
            meaning="New beginnings",
            nouns_reversed=["recklessness"],
            adjectives_reversed=["reckless"],
            meaning_reversed="Recklessness",
        )
        assert card.name == "The Fool"
        assert card.number == "0"
        assert card.arcana == "Major"
        assert card.suit is None
        assert card.nouns == ["beginnings", "innocence"]
        assert card.adjectives == ["free", "innocent"]
        assert card.meaning == "New beginnings"
        assert card.nouns_reversed == ["recklessness"]
        assert card.adjectives_reversed == ["reckless"]
        assert card.meaning_reversed == "Recklessness"

    def test_major_arcana_has_no_suit(self) -> None:
        card = TarotCard(
            name="The Magician",
            number="I",
            arcana="Major",
            suit=None,
            nouns=[],
            adjectives=[],
            meaning="",
            nouns_reversed=[],
            adjectives_reversed=[],
            meaning_reversed="",
        )
        assert card.suit is None

    def test_minor_arcana_has_suit(self) -> None:
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
        assert card.suit == "Cups"
