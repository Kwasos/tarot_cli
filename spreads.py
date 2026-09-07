import random
import actions as a


def pick_two(items):
    first = random.choice(items)
    rest = [item for item in items if item != first]
    second = random.choice(rest) if rest else first
    return first, second


def generate_daily_reading(card: a.TarotCard, is_reversed: bool = False) -> str:
    nouns: list[str] = card["nouns_reversed"] if is_reversed else card["nouns"]
    adjectives: list[str] = (
        card["adjectives_reversed"] if is_reversed else card["adjectives"]
    )
    meaning: str = card["meaning_reversed"] if is_reversed else card["meaning"]

    def template_noun_led():
        n1, n2 = pick_two(nouns)
        adj = random.choice(adjectives)
        return f"Today carries the weight of {n1} and {n2}. Expect a {adj} undertone to the hours ahead. {meaning}"

    def template_adjective_led():
        adj1, adj2 = pick_two(adjectives)
        noun = random.choice(nouns)
        return f"You may feel {adj1} today, maybe {adj2} too. At its heart, this is a day about {noun}. {meaning}"

    def template_meaning_led():
        noun = random.choice(nouns)
        adj = random.choice(adjectives)
        return f"{meaning} Let today be a little {adj}, and leave some room for {noun}."

    templates: list = [template_noun_led, template_adjective_led, template_meaning_led]
    reading: str = random.choice(templates)()

    return reading


def generate_1_card_reading(card: a.TarotCard, is_reversed: bool = False) -> str:
    nouns: list[str] = card["nouns_reversed"] if is_reversed else card["nouns"]
    adjectives: list[str] = (
        card["adjectives_reversed"] if is_reversed else card["adjectives"]
    )

    def template_noun_led():
        n1, n2 = pick_two(nouns)
        adj = random.choice(adjectives)
        return f"Your question relates to {n1} and {n2}. Consider a {adj} approach."

    def template_adjective_led():
        adj1, adj2 = pick_two(adjectives)
        noun = random.choice(nouns)
        return f"Accept the feeling of {adj1} and {adj2}. Prepare for an encounter with {noun}."

    def template_one_of_each():
        noun = random.choice(nouns)
        adj = random.choice(adjectives)
        return f"Anticipate a {adj} path, for your future may include {noun}."

    def template_4():
        n1, n2 = pick_two(nouns)
        adj = random.choice(adjectives)
        return f"Should the {adj} journey beckon, remember that {n1} whispers secerets only {n2} dares to hear"

    def template_5():
        n1, n2 = pick_two(nouns)
        adj1, adj2 = pick_two(adjectives)
        return f"Let the {adj1} {n1} give you direction in this {adj2} path of {n2}"

    templates: list = [
        template_noun_led,
        template_adjective_led,
        template_one_of_each,
        template_4,
        template_5,
    ]
    reading: str = random.choice(templates)()

    return reading
