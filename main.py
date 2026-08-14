import json
import random


# Load json card data
def get_cards() -> str:
    with open("cards/tarot.json") as f:
        file_contents = f.read()
    return file_contents


# Create deck
def create_deck() -> list[dict]:
    cards = get_cards()

    # Using JSONDecoder to parse JSON
    decoder = json.JSONDecoder()
    cards = decoder.decode(cards)

    # Create and add cards to the deck
    deck = []
    for card in cards["cards"]:
        deck.append(card)

    return deck


def draw(deck: list[dict]) -> tuple[list[dict], str]:
    # Select a card by index
    index: int = random.randrange(len(deck))
    selected_card: dict = deck[index]
    # Assign reversed
    reversed: str = random.choice(["", "Reversed"])
    card_name: str = f"{selected_card['name']} {reversed}"
    del deck[index]
    return deck, card_name


def main():
    deck = create_deck()
    print("Press Enter after each card to continue drawing")
    user_input = input("How many cards would you like to pull? ")

    for _ in range(1, int(user_input)):
        deck, card = draw(deck)
        print(card)
        input()

    # Select a card
    selected_card = random.choices(deck)

    # Assign reversed
    reversed = random.choice(["", "Reversed"])

    # Reveal card
    try:
        print(f"{selected_card[0]['name']} {reversed}")
    except Exception as error:
        print(f"invalid cards json provided: {error}")


if __name__ == "__main__":
    main()
