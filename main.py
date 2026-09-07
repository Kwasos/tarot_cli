import actions as a
from random import choice
from rich import print
from rich.align import Align
from rich.console import Console

console = Console()


def main():
    try:
        deck: list[a.TarotCard] = a.create_deck()
        console.print(
            Align.center(
                f"[bold cyan]Welcome to the tarot_cli![/bold cyan]\n[italic]Type h or help to {a.commands['help | h']}[/italic]"
            )
        )
        while True:
            user_input = input("tarot_cli> ")
            user_input = user_input.lower().split()

            # create a new line with no input provided
            if len(user_input) < 1:
                continue

            match user_input[0]:
                case "draw":
                    if len(deck) == 0:
                        print("There are [red]no more cards[/red] in the deck!")
                        continue
                    if len(user_input) > 1:
                        if user_input[1].isdigit():
                            if len(deck) < int(user_input[1]):
                                print("[red]Not enough cards in the deck!")
                                continue
                            a.series(deck, int(user_input[1]))
                            continue
                    deck, card = a.draw(deck)
                    is_reversed: bool = choice([True, False])
                    a.print_card(card, is_reversed)

                case "deck":
                    print(
                        f"There are [bold yellow]{len(deck)} cards[/bold yellow] remaining in the deck"
                    )

                case "shuffle":
                    deck = a.shuffle()
                    print("[green italic]Deck shuffled")

                case "drawn":
                    if len(a.drawn_cards) == 0:
                        print("[red]There are currently no drawn cards")
                        continue
                    print("[italic]Drawn cards:")
                    for card in a.drawn_cards:
                        a.print_card(card)

                case "meaning":
                    if len(user_input) < 2:
                        print("Please specify a card name")
                        continue
                    if user_input[-1] == "reversed":
                        card_name: list[str] = user_input[1:-1]
                    else:
                        card_name: list[str] = user_input[1:]
                    deck: list[a.TarotCard] = a.create_deck()
                    for card in deck:
                        if card["name"].lower().split() == card_name:
                            if user_input[-1] == "reversed":
                                print(card["meaning_reversed"])
                                break
                            else:
                                print(card["meaning"])
                                break
                    else:
                        print("[red]Invalid card name")

                case "inspect":
                    if len(user_input) < 2:
                        print("Please specify a card name")
                        continue
                    if user_input[-1] == "reversed":
                        card_name: list[str] = user_input[1:-1]
                    else:
                        card_name: list[str] = user_input[1:]
                    deck: list[a.TarotCard] = a.create_deck()
                    for card in deck:
                        if card["name"].lower().split() == card_name:
                            a.inspect(card)
                            break
                    else:
                        print("[red]Invalid card name")

                case "reading":
                    if len(user_input) < 2:
                        deck = a.reading(deck, 1)
                    if len(user_input) > 1:
                        if user_input[1].isdigit():
                            if len(deck) < int(user_input[1]):
                                print("[red]Not enough cards in the deck!")
                                continue
                            deck = a.reading(deck, int(user_input[1]))

                case "daily":
                    card, reading = a.daily()
                    a.print_card(card)
                    print(reading)

                case "q" | "quit":
                    print("[cyan]The cards wait for another time...")
                    break

                case "h" | "help":
                    a.help()

                case _:
                    print("[red]unknown command")
    except KeyboardInterrupt:
        print("\n[red]Tarot interrupted, terminating program")


if __name__ == "__main__":
    main()
