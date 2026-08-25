import random
from json import JSONDecoder
import time

commands = {
    "series": "draw a selected number of cards from the same deck, then shuffle",
    "draw": "draw a single card from the deck",
    "shuffle": "return all cards to the deck",
    "daily": "deterministic selection of a random card based on the current date",
    "help": "print a list of avaiable commands",
    "quit": "closes the program",
}


def help() -> None:
    for command in commands:
        print(f"COMMAND: {command}\nDESCRIPTION: {commands[command]}\n")


# Load json card data
def get_cards() -> str:
    with open("cards/tarot.json") as f:
        file_contents = f.read()
    return file_contents


# Create deck
def create_deck() -> list[dict]:
    cards = get_cards()

    # Using JSONDecoder to parse JSON
    decoder = JSONDecoder()
    cards = decoder.decode(cards)

    # Create and add cards to the deck
    deck = []
    for card in cards["cards"]:
        deck.append(card)

    return deck


def draw(deck: list[dict]) -> tuple[list[dict], dict]:
    deck = deck.copy()
    index: int = random.randrange(len(deck))
    selected_card: dict = deck.pop(index)
    return deck, selected_card


def put_back(deck: list[dict], card: dict) -> list[dict]:
    deck.append(card)
    return deck


# Drawing a series of cards
def series(deck: list[dict]) -> None:
    user_input = input("How many cards would you like to pull? ")
    print("Press Enter to draw cards")

    for _ in range(0, int(user_input)):
        input()
        deck, card = draw(deck)
        # Assign reversed
        reversed: str = random.choice(["", "Reversed"])
        card_name: str = f"{card['name']} {reversed}"
        print(card_name)


# Fixed card per day
def daily(deck: list[dict]) -> dict:
    deck = deck.copy()
    date = time.localtime()
    date = int(str(date.tm_yday) + str(date.tm_year))
    random.seed(date)
    index: int = random.randrange(len(deck))
    selected_card: dict = deck.pop(index)

    # Randomizing the seed again (for now, might not be needed)
    t = 1000 * time.time()
    random.seed(int(t) % 2**32)
    return selected_card
