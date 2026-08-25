import actions as a


def main():
    try:
        deck = a.create_deck()
        print(f"Welcome to the tarot_cli\nType h or help to {a.commands['help']}")
        while True:
            user_input = input("tarot_cli> ")
            user_input = user_input.lower().split()

            # create a new line with no input provided
            if len(user_input) < 1:
                continue

            match user_input[0]:
                case "series":
                    a.series(deck)
                case "draw":
                    deck, card = a.draw(deck)
                    print(f"There are {len(deck)} cards remaining in the deck\n")
                    print(card["name"])
                case "daily":
                    card = a.daily(deck)
                    print(card["name"])
                case "shuffle":
                    deck = a.create_deck()
                    print("Deck shuffled")
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
