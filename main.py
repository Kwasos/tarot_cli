import json
import random


# Load json card data
def get_cards():
    with open("cards/tarot.json") as f:
        file_contents = f.read()
    return file_contents


def main():
    cards = get_cards()

    # Using JSONDecoder to parse JSON
    decoder = json.JSONDecoder()
    cards = decoder.decode(cards)

    # Select a card
    selected_card = random.choices(cards["cards"])

    # Assign reversed
    reversed = random.choice(["", "Reversed"])
    try:
        print(f"{selected_card[0]['name']} {reversed}")
    except Exception as error:
        print(f"invalid cards json provided: {error}")


if __name__ == "__main__":
    main()
