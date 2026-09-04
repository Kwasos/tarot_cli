import random
from json import JSONDecoder
import time
from typing import TypedDict, Optional
from rich import print


class TarotCard(TypedDict):
    name: str
    number: str
    arcana: str
    suit: Optional[str]
    nouns: list[str]
    adjectives: list[str]
    meaning: str
    nouns_reversed: list[str]
    adjectives_reversed: list[str]
    meaning_reversed: str


deck_commands = {
    "draw": "draw the specified number of cards, if no number is given, draw a single card from the deck",
    "shuffle": "return all cards to the deck",
    "deck": "display the current number of cards in the deck",
    "drawn": "display drawn cards, currently not in the deck",
    "inspect": "display all card details for the specified card",
}

spreads = {
    "daily": "deterministic selection of a random card based on the current date, always uses a fresh deck and draws the card upright",
}

commands = {
    "help | h": "print a list of avaiable commands",
    "quit | q": "closes the program",
}

drawn_cards: list[TarotCard] = []


def help() -> None:
    print("[bold cyan]Deck commands:[/bold cyan]")
    for command in deck_commands:
        print(f"> [cyan]{command}[/cyan] --- {deck_commands[command]}")

    print("[bold magenta]Spreads:[/bold magenta]")
    for command in spreads:
        print(f"> [magenta]{command}[/magenta] --- {spreads[command]}")

    print("[bold bright_red]System commands:[/bold bright_red]")
    for command in commands:
        print(f"> [bright_red]{command}[/bright_red] --- {commands[command]}")


# Load json card data
def get_cards() -> str:
    with open("cards/tarot.json") as f:
        file_contents = f.read()
    return file_contents


# Create deck
def create_deck() -> list[TarotCard]:
    cards = get_cards()

    # Using JSONDecoder to parse JSON
    decoder = JSONDecoder()
    cards = decoder.decode(cards)

    # Create and add cards to the deck
    deck: list[TarotCard] = []
    for card in cards["cards"]:
        deck.append(card)

    return deck


def draw(deck: list[TarotCard]) -> tuple[list[TarotCard], TarotCard]:
    index: int = random.randrange(len(deck))
    selected_card: TarotCard = deck.pop(index)
    drawn_cards.append(selected_card)
    return deck, selected_card


def shuffle() -> list[TarotCard]:
    deck: list[TarotCard] = create_deck()
    drawn_cards.clear()
    return deck


def inspect(card: TarotCard) -> None:
    print(f"""
    [bold]name:[/bold] {card["name"]}
    [bold]number:[/bold] {card["number"]}
    [bold]arcana:[/bold] {card["arcana"]}
    [bold]suit:[/bold] {card["suit"]}
    [bold]nouns:[/bold] {card["nouns"]}
    [bold]adjectives:[/bold] {card["adjectives"]}
    [bold]meaning:[/bold] {card["meaning"]}
    [bold]nouns_reversed:[/bold] {card["nouns_reversed"]}
    [bold]adjectives_reversed:[/bold] {card["adjectives_reversed"]}
    [bold]meaning_reversed:[/bold] {card["meaning_reversed"]}""")


# Drawing a series of cards
def series(deck: list[TarotCard], n: int) -> None:
    for _ in range(0, n):
        input()
        deck, card = draw(deck)
        # Assign reversed
        is_reversed: bool = random.choice((True, False))
        print_card(card, is_reversed)


# Fixed card per day
def daily() -> TarotCard:
    deck: list[TarotCard] = create_deck()
    date = time.localtime()
    date = int(str(date.tm_yday) + str(date.tm_year))
    random.seed(date)
    index: int = random.randrange(len(deck))
    selected_card: TarotCard = deck.pop(index)

    # Randomizing the seed again
    t = 1000 * time.time()
    random.seed(int(t) % 2**32)
    return selected_card


def print_card(card: TarotCard, is_reversed: bool = False) -> None:
    match card["suit"]:
        case "Cups":
            if not is_reversed:
                print(f"[red]{card['name']}")
            else:
                print(f"[red]{card['name']} Reversed")
        case "Pentacles":
            if not is_reversed:
                print(f"[green]{card['name']}")
            else:
                print(f"[green]{card['name']} Reversed")
        case "Swords":
            if not is_reversed:
                print(f"[blue]{card['name']}")
            else:
                print(f"[blue]{card['name']} Reversed")
        case "Wands":
            if not is_reversed:
                print(f"[yellow]{card['name']}")
            else:
                print(f"[yellow]{card['name']} Reversed")
        case _:
            if not is_reversed:
                print(f"[magenta]{card['name']}")
            else:
                print(f"[magenta]{card['name']} Reversed")
