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

    with open(OUTPUT_FILE, "w") as f:
        json.dump(cards, f, indent=4)

    print(f"Saved {len(cards)} cards to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
