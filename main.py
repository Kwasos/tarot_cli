import actions as a


def main():
    deck = a.create_deck()
    user_input = input("What would you like to do?\n")
    match user_input:
        case "series":
            a.series(deck)
        case "draw":
            deck, card = a.draw(deck)
            print(card["name"])
        case "daily":
            card = a.daily(deck)
            print(card["name"])


if __name__ == "__main__":
    main()
