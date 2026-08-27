import actions as a
from random import choice


def main():
    try:
        deck: list[a.TarotCard] = a.create_deck()
        print(f"Welcome to the tarot_cli\nType h or help to {a.commands['help | h']}")
        while True:
            user_input = input("tarot_cli> ")
            user_input = user_input.lower().split()

            # create a new line with no input provided
            if len(user_input) < 1:
                continue

            match user_input[0]:
                case "draw":
                    if len(deck) == 0:
                        print("There are no more cards in the deck!")
                        continue
                    if len(user_input) > 1:
                        if user_input[1].isdigit():
                            if len(deck) < int(user_input[1]):
                                print("Not enough cards in the deck!")
                                continue
                            a.series(deck, int(user_input[1]))
                            continue
                    deck, card = a.draw(deck)
                    reversed: str = choice(["", "Reversed"])
                    print(f"{card['name']} {reversed}")
                case "deck":
                    print(f"There are {len(deck)} cards remaining in the deck")
                case "shuffle":
                    deck = a.shuffle()
                    print("Deck shuffled")
                case "drawn":
                    if len(a.drawn_cards) == 0:
                        print("There are currently no drawn cards")
                        continue
                    print("Drawn cards:")
                    for card in a.drawn_cards:
                        print(card["name"])
                case "daily":
                    card: a.TarotCard = a.daily()
                    print(card["name"])
                case "q" | "quit":
                    print("The cards wait for another time...")
                    break
                case "h" | "help":
                    a.help()
                case _:
                    print("unknown command")
    except KeyboardInterrupt:
        print("\nTarot interrupted, terminating program")


if __name__ == "__main__":
    main()
