import actions
import unittest


# depreciated
class TestingDeck(unittest.TestCase):
    def test_changed_deck(self):
        deck = actions.create_deck()
        deck_modified, _ = actions.draw(deck)
        self.assertNotEqual(deck, deck_modified)
