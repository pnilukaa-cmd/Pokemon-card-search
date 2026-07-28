"""Fetch all Standard-legal Pokemon TCG cards and save them to a local JSON file."""

import json
import time

import requests

API_URL = "https://api.pokemontcg.io/v2/cards"
QUERY = "legalities.standard:legal"
PAGE_SIZE = 250
OUTPUT_FILE = "pokemon_standard_cards.json"
MAX_RETRIES = 8
MAX_WAIT_SECONDS = 30

# pokemontcg.io's legalities.standard flag is not kept in sync with rotation,
# so filter by regulation mark instead. H/I/J are legal as of the March 2026
# Standard rotation (G rotated out); update this set when the format rotates again.
ACTIVE_REGULATION_MARKS = {"H", "I", "J"}


def fetch_page(page):
    for attempt in range(1, MAX_RETRIES + 1):
        response = requests.get(
            API_URL,
            params={"q": QUERY, "page": page, "pageSize": PAGE_SIZE},
        )
        if response.status_code >= 500 and attempt < MAX_RETRIES:
            wait = min(2 ** attempt, MAX_WAIT_SECONDS)
            print(f"Page {page}: server error {response.status_code}, retrying in {wait}s (attempt {attempt}/{MAX_RETRIES})")
            time.sleep(wait)
            continue
        response.raise_for_status()
        return response.json().get("data", [])


def card_signature(card):
    """Identity of a card's gameplay function, ignoring cosmetic printing details
    like set, card number, artist, rarity, and images."""
    return (
        card.get("name"),
        card.get("supertype"),
        card.get("hp"),
        tuple(card.get("types") or []),
        tuple(card.get("subtypes") or []),
        tuple(card.get("rules") or []),
        tuple(
            (a.get("name"), tuple(a.get("cost") or []), a.get("damage"), a.get("text"))
            for a in (card.get("attacks") or [])
        ),
        tuple((a.get("name"), a.get("text")) for a in (card.get("abilities") or [])),
        tuple((w.get("type"), w.get("value")) for w in (card.get("weaknesses") or [])),
        tuple((r.get("type"), r.get("value")) for r in (card.get("resistances") or [])),
        card.get("convertedRetreatCost"),
    )


def dedupe_by_signature(cards):
    seen = set()
    unique_cards = []
    for card in cards:
        sig = card_signature(card)
        if sig not in seen:
            seen.add(sig)
            unique_cards.append(card)
    return unique_cards


def fetch_all_standard_cards():
    all_cards = []
    page = 1

    while True:
        cards = fetch_page(page)

        if not cards:
            break

        all_cards.extend(cards)
        print(f"Page {page}: fetched {len(cards)} cards (total so far: {len(all_cards)})")
        page += 1

    return all_cards


def main():
    cards = fetch_all_standard_cards()

    standard_cards = [c for c in cards if c.get("regulationMark") in ACTIVE_REGULATION_MARKS]
    print(f"Fetched {len(cards)} cards, {len(standard_cards)} currently Standard-legal by regulation mark")

    unique_cards = dedupe_by_signature(standard_cards)
    print(f"Deduped cosmetic reprints (alt art, rarity, etc.): {len(unique_cards)} unique cards")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(unique_cards, f, indent=4)

    print(f"Saved {len(unique_cards)} cards to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
