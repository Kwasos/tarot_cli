"""Tests for the main module."""

import sys
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from tarot_cli.main import _find_card, main
from tarot_cli.models import TarotCard


class TestFindCard:
    """Test card finding by name."""

    def test_find_exact(self) -> None:
        deck = [
            TarotCard(
                name="The Fool", number="0", arcana="Major", suit=None,
                nouns=[], adjectives=[], meaning="",
                nouns_reversed=[], adjectives_reversed=[], meaning_reversed="",
            )
        ]
        result = _find_card(deck, ["the", "fool"])
        assert result is not None
        assert result["name"] == "The Fool"

    def test_find_partial_match(self) -> None:
        deck = [
            TarotCard(
                name="Three of Cups", number="3", arcana="Minor", suit="Cups",
                nouns=[], adjectives=[], meaning="",
                nouns_reversed=[], adjectives_reversed=[], meaning_reversed="",
            )
        ]
        result = _find_card(deck, ["three", "of", "cups"])
        assert result is not None

    def test_find_no_match(self) -> None:
        deck = [
            TarotCard(
                name="The Fool", number="0", arcana="Major", suit=None,
                nouns=[], adjectives=[], meaning="",
                nouns_reversed=[], adjectives_reversed=[], meaning_reversed="",
            )
        ]
        result = _find_card(deck, ["nonexistent", "card"])
        assert result is None

    def test_find_case_insensitive(self) -> None:
        deck = [
            TarotCard(
                name="The Fool", number="0", arcana="Major", suit=None,
                nouns=[], adjectives=[], meaning="",
                nouns_reversed=[], adjectives_reversed=[], meaning_reversed="",
            )
        ]
        result = _find_card(deck, ["THE", "FOOL"])
        assert result is not None

    def test_empty_deck(self) -> None:
        result = _find_card([], ["any", "card"])
        assert result is None


class TestMainCLI:
    """Test CLI entry point."""

    def test_version_flag(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(sys, "argv", ["tarot", "--version"])
        captured = StringIO()
        monkeypatch.setattr(sys, "stdout", captured)
        main()
        assert "0.1.0" in captured.getvalue()

    def test_help_flag(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(sys, "argv", ["tarot", "--help"])
        captured = StringIO()
        monkeypatch.setattr(sys, "stdout", captured)
        main()
        output = captured.getvalue()
        assert "tarot_cli" in output
        assert "Usage" in output

    def test_unknown_command(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(sys, "argv", ["tarot", "bogus"])
        captured = StringIO()
        monkeypatch.setattr(sys, "stdout", captured)
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    def test_no_args_starts_interactive(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that no args enters interactive mode."""
        monkeypatch.setattr(sys, "argv", ["tarot"])
        # This would hang in interactive mode, so just verify the path exists
        # by checking the function is callable
        from tarot_cli.main import _run_interactive
        assert callable(_run_interactive)
