"""Data models for tarot cards."""

from __future__ import annotations

from typing import Optional


class TarotCard(dict):
    """A tarot card as a typed dictionary.

    Keys: name, number, arcana, suit, nouns, adjectives, meaning,
          nouns_reversed, adjectives_reversed, meaning_reversed.
    """

    __slots__ = ()  # type: ignore[override]

    @property
    def name(self) -> str:
        return self["name"]

    @property
    def number(self) -> str:
        return self["number"]

    @property
    def arcana(self) -> str:
        return self["arcana"]

    @property
    def suit(self) -> Optional[str]:
        return self["suit"]

    @property
    def nouns(self) -> list[str]:
        return self["nouns"]

    @property
    def adjectives(self) -> list[str]:
        return self["adjectives"]

    @property
    def meaning(self) -> str:
        return self["meaning"]

    @property
    def nouns_reversed(self) -> list[str]:
        return self["nouns_reversed"]

    @property
    def adjectives_reversed(self) -> list[str]:
        return self["adjectives_reversed"]

    @property
    def meaning_reversed(self) -> str:
        return self["meaning_reversed"]
