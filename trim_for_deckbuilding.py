"""Trim pokemon_standard_cards.json down to the fields relevant for deckbuilding,
dropping pricing data and images to keep the file small for use as LLM context."""

import json

INPUT_FILE = "pokemon_standard_cards.json"
OUTPUT_FILE = "pokemon_standard_cards_deckbuilding.json"

KEEP_FIELDS = [
    "id",
    "name",
    "supertype",
    "subtypes",
    "types",
    "hp",
    "evolvesFrom",
    "evolvesTo",
    "attacks",
    "abilities",
    "weaknesses",
    "resistances",
    "retreatCost",
    "convertedRetreatCost",
    "rules",
    "regulationMark",
]


def trim_card(card):
    trimmed = {field: card[field] for field in KEEP_FIELDS if field in card}
    trimmed["set"] = card["set"]["name"]
    return trimmed


def main():
    with open(INPUT_FILE) as f:
        cards = json.load(f)

    trimmed_cards = [trim_card(c) for c in cards]

    with open(OUTPUT_FILE, "w") as f:
        json.dump(trimmed_cards, f, indent=4)

    print(f"Trimmed {len(trimmed_cards)} cards to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
