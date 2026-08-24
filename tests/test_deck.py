import actions
import unittest


class TestingDeck(unittest.TestCase):
    def test_changed_deck(self):
        deck = actions.create_deck()
        deck_modified, _ = actions.draw(deck)
        self.assertNotEqual(deck, deck_modified)

    def test_restored_deck(self):
        deck = actions.create_deck()
        deck_modified, card = actions.draw(deck)
        deck_modified = actions.put_back(deck_modified, card)
        self.assertEqual(
            sorted(deck, key=lambda c: c["name"]),
            sorted(deck_modified, key=lambda c: c["name"]),
        )
