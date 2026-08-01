"""Fetch all Standard-legal Pokemon TCG cards and save them to a local JSON file."""

import json
import time

import requests

API_URL = "https://api.pokemontcg.io/v2/cards"
PAGE_SIZE = 250
OUTPUT_FILE = "pokemon_standard_cards.json"
MAX_RETRIES = 8
MAX_WAIT_SECONDS = 30

# pokemontcg.io's legalities.standard flag is not kept in sync with rotation,
# so filter by regulation mark instead. H/I/J are legal as of the March 2026
# Standard rotation (G rotated out); update this set when the format rotates again.
#
# IMPORTANT: query by regulationMark directly (one query per mark, see
# fetch_all_standard_cards below), not via `legalities.standard:legal` -- that
# flag is exactly the unreliable one this whole workaround exists to route
# around, so filtering the initial fetch by it defeats the purpose: any card
# the API's own stale flag marks "Not Legal" would never be fetched at all,
# regardless of its actual regulation mark. Confirmed this was silently
# dropping real, currently-legal cards (e.g. me3-113 Poke Pad, Regulation
# Mark J, live legalities.standard: "Not Legal") -- about 1,140 cards across
# nearly every set in the dataset were missing because of this.
#
# The API's OR syntax for combining multiple values on one field
# (`regulationMark:H OR regulationMark:I`, `regulationMark:(H OR I)`,
# `regulationMark:H,I`) all return 500/400 errors as of this writing --
# querying each mark separately and merging is what actually works.
ACTIVE_REGULATION_MARKS = {"H", "I", "J"}


def fetch_page(query, page):
    for attempt in range(1, MAX_RETRIES + 1):
        response = requests.get(
            API_URL,
            params={"q": query, "page": page, "pageSize": PAGE_SIZE},
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


def fetch_all_for_mark(mark):
    query = f"regulationMark:{mark}"
    cards = []
    page = 1

    while True:
        page_cards = fetch_page(query, page)

        if not page_cards:
            break

        cards.extend(page_cards)
        print(f"  regulationMark:{mark} page {page}: fetched {len(page_cards)} cards (mark total so far: {len(cards)})")
        page += 1

    return cards


def fetch_all_standard_cards():
    all_cards = []
    for mark in sorted(ACTIVE_REGULATION_MARKS):
        print(f"Fetching regulationMark:{mark}...")
        all_cards.extend(fetch_all_for_mark(mark))
    return all_cards


def main():
    cards = fetch_all_standard_cards()

    # Each card was already fetched by an exact regulationMark:X query, so no
    # further regulation-mark filtering is needed here (unlike the old
    # legalities.standard:legal-based fetch, which needed a second filter
    # pass to route around that field's staleness -- see the comment above
    # ACTIVE_REGULATION_MARKS for why that didn't fully work).
    print(f"Fetched {len(cards)} cards across regulation marks {sorted(ACTIVE_REGULATION_MARKS)}")

    unique_cards = dedupe_by_signature(cards)
    print(f"Deduped cosmetic reprints (alt art, rarity, etc.): {len(unique_cards)} unique cards")

    with open(OUTPUT_FILE, "w") as f:
        json.dump(unique_cards, f, indent=4)

    print(f"Saved {len(unique_cards)} cards to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
