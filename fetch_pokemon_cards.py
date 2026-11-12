"""Fetch all Standard-legal Pokemon TCG cards and save them to a local JSON file."""

import json
import re
import sys
import time

import requests

API_URL = "https://api.pokemontcg.io/v2/cards"
PAGE_SIZE = 250
OUTPUT_FILE = "pokemon_standard_cards.json"
MAX_RETRIES = 8
MAX_WAIT_SECONDS = 30

# pokemontcg.io's legalities.standard flag is not kept in sync with rotation,
# so filter by regulation mark instead. H/I/J are legal per the real 2026
# Standard rotation (in-person Play! Pokemon cutover April 10 2026, PTCG Live
# March 26 2026 -- confirmed via pokemon.com's own rotation announcement and
# corroborated by TCGplayer's rotation guide): G was explicitly called out as
# rotating OUT, with E and F having already rotated out earlier (F was
# removed April 11 2025). Update this set when the format actually rotates
# again.
#
# DO NOT re-derive this by checking what fraction of each mark's cards the
# API's own legalities.standard field claims are Legal, even in aggregate --
# tried exactly that and it's actively misleading, not just noisy: it showed
# ~100% "Legal" across E, F, and G alike (1201/1202, 1180/1180, 1639/1639)
# indistinguishable from the genuinely-current H/I/J marks (1302/1302,
# 1226/1226, 419/419), and would have reintroduced ~4,000 cards that
# actually rotated out a year-plus ago, based purely on a stale bulk flag
# the API apparently never updated after the real rotation. Only D showed
# the expected mostly-Not-Legal pattern (35/1261, ~3%). The field's
# staleness isn't limited to a few just-released stragglers (the original
# me3-113 Poke Pad case) -- it can be wrong for an entire regulation mark's
# worth of cards at once. Regulation-mark legality has to be established
# from an authoritative rotation announcement (or a working, non-blocked
# legality tracker), never from this field, no matter how it's aggregated.
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
#
# Also pass orderBy=id on every page request (see fetch_page below): without
# an explicit sort, the API's default ordering isn't stable across separate
# paginated requests, so paging through a query can silently skip or
# duplicate cards even though totalCount is correct. Confirmed this directly:
# me3-113 matched a `regulationMark:J` query on its own, but was missing from
# a full unordered pagination of that same query; adding orderBy=id fixed it
# with no duplicates.
ACTIVE_REGULATION_MARKS = {"H", "I", "J"}


def fetch_page(query, page):
    for attempt in range(1, MAX_RETRIES + 1):
        response = requests.get(
            API_URL,
            # orderBy=id makes pagination deterministic. Without it, the API's
            # default (relevance-ish) ordering isn't stable across separate
            # page requests, so paging through a query can silently skip or
            # duplicate cards even though the totalCount is correct -- caught
            # this because me3-113 (Poke Pad) matched `regulationMark:J` on
            # its own but was missing from a full paginated fetch of that
            # same query; adding orderBy=id made it show up with no
            # duplicates across pages.
            params={"q": query, "page": page, "pageSize": PAGE_SIZE, "orderBy": "id"},
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


# The Scarlet & Violet promo set comes back from the API with
# ptcgoCode: null, so every promo silently lost its set code and became
# unresolvable. PTCG Live calls that set PR-SV.
SET_CODE_FALLBACK = {"svp": "PR-SV"}


def fill_set_codes(cards):
    """Give every card its set's ptcgoCode when the card itself lacks it.

    A just-released set can come back with no ptcgoCode on its cards even
    though the set record has one: Delta Reign's /v2/sets entry says DLR,
    its cards' own set objects say nothing. Every card then had no printing
    to record, so no decklist line could ever name it."""
    codes = {}
    for card in cards:
        s = card.get("set") or {}
        if s.get("ptcgoCode") or s.get("id") in SET_CODE_FALLBACK or not s.get("id"):
            continue
        if s["id"] not in codes:
            codes[s["id"]] = None
            # The single-set endpoint 500s more often than the search one
            # (it did on every try once), so ask the search endpoint too.
            for attempt in range(1, MAX_RETRIES + 1):
                for url, params in (("https://api.pokemontcg.io/v2/sets", {"q": f"id:{s['id']}"}),
                                    (f"https://api.pokemontcg.io/v2/sets/{s['id']}", None)):
                    try:
                        r = requests.get(url, params=params, timeout=60)
                        data = r.json().get("data") if r.ok else None
                    except (requests.RequestException, ValueError):
                        data = None
                    if isinstance(data, list):
                        data = next((x for x in data if x.get("id") == s["id"]), None)
                    if data and data.get("ptcgoCode"):
                        codes[s["id"]] = data["ptcgoCode"]
                        break
                if codes[s["id"]]:
                    break
                time.sleep(min(2 ** attempt, MAX_WAIT_SECONDS))
            print(f"  set {s['id']}: cards carry no ptcgoCode, the set record "
                  f"says {codes[s['id']]}")
        if codes[s["id"]]:
            s["ptcgoCode"] = codes[s["id"]]
    return cards


def set_code_of(card):
    s = card.get("set") or {}
    return s.get("ptcgoCode") or SET_CODE_FALLBACK.get(s.get("id"))


def dedupe_by_signature(cards):
    """Keep one entry per distinct gameplay function -- but record EVERY
    printing of it.

    This used to drop the reprints outright, keeping only the first set and
    number seen. That silently made the file unusable for the one job it
    gets asked to do most: checking a SET NUM off a real decklist. A user's
    `Poke Pad POR 81`, `Gwynn PBL 78`, `Buddy-Buddy Poffin ASC 184` and
    `Night Stretcher ASC 196` all came back "not in pool" and all four were
    correct -- they were simply functionally identical to a printing that
    happened to be kept instead. Every card now carries a `printings` list
    of every (ptcgoCode, number) the API returned for it, so any legal
    printing resolves while the gameplay data stays deduplicated.
    """
    by_sig = {}
    order = []
    for card in cards:
        sig = card_signature(card)
        entry = (set_code_of(card), str(card.get("number")))
        if sig not in by_sig:
            by_sig[sig] = card
            card["printings"] = []
            order.append(sig)
        kept = by_sig[sig]
        if entry[0] and entry not in kept["printings"]:
            kept["printings"].append(entry)
    for sig in order:
        by_sig[sig]["printings"].sort()
    return [by_sig[sig] for sig in order]


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


# Marks to probe for existence even though they are not in the active set.
# A brand-new expansion can introduce a mark, and the failure mode is silent:
# the fetch returns exactly the same cards as last time and nothing says the
# newest set is missing. Checked when 30th Celebration (30C) was announced --
# mark K was empty then, so the pool legitimately had nothing to add, but
# "empty" and "not looked at" have to be distinguishable.
PROBE_REGULATION_MARKS = {"K", "L"}


def mark_count(mark):
    """How many cards the API has for a regulation mark, or None on error."""
    for attempt in range(1, 4):
        try:
            r = requests.get(API_URL, params={"q": f"regulationMark:{mark}",
                                              "pageSize": 1})
            if r.status_code >= 500:
                time.sleep(min(2 ** attempt, MAX_WAIT_SECONDS))
                continue
            r.raise_for_status()
            return r.json().get("totalCount")
        except Exception:
            time.sleep(min(2 ** attempt, MAX_WAIT_SECONDS))
    return None


def warn_about_new_marks():
    """Shout if a regulation mark outside the active set has cards.

    Rotation and new-set legality are decided by an announcement, never by
    this API (see ACTIVE_REGULATION_MARKS), so this does NOT add the mark
    automatically. It just makes the omission impossible to miss.
    """
    for mark in sorted(PROBE_REGULATION_MARKS - ACTIVE_REGULATION_MARKS):
        n = mark_count(mark)
        if n is None:
            print(f"  regulationMark:{mark}: could not be checked")
        elif n:
            print(f"  *** regulationMark:{mark} now has {n} cards and is NOT "
                  f"in ACTIVE_REGULATION_MARKS. If that mark is Standard-legal, "
                  f"add it there -- otherwise this fetch is silently missing "
                  f"an entire set. ***")
        else:
            print(f"  regulationMark:{mark}: 0 cards, nothing to add")


def fetch_all_standard_cards():
    all_cards = []
    for mark in sorted(ACTIVE_REGULATION_MARKS):
        print(f"Fetching regulationMark:{mark}...")
        all_cards.extend(fetch_all_for_mark(mark))
    print("Checking for regulation marks outside the active set...")
    warn_about_new_marks()
    return fill_set_codes(all_cards)


def fetch_set(set_id):
    """Every card of one set, paged with the same retries and ordering."""
    cards, page = [], 1
    while True:
        page_cards = fetch_page(f"set.id:{set_id}", page)
        if not page_cards:
            return cards
        cards.extend(page_cards)
        print(f"  set.id:{set_id} page {page}: fetched {len(page_cards)} cards")
        page += 1


_REMINDER_RE = re.compile(
    r"^(?:you may play (?:only 1|any number of) [^.]*during your turn\."
    r"|you may play only 1 stadium card during your turn\..*)$", re.I | re.S)


def reprint_key(card):
    """card_signature, minus what a new set's data is often missing.

    A just-released set comes back thinner than an old one: Delta Reign's
    Pokémon Catcher and Emcee's Hype had no "You may play any number of
    Item cards" reminder line, and its Bubbly Water / Growing Grass / Nitro
    Fire Energy had no subtypes and a different paragraph break. Matched on
    card_signature they became second records under the same name, which a
    decklist line then resolves to by set number. Rules text here drops the
    play-rule reminders and collapses whitespace; subtypes are compared
    separately, and only when both cards have them."""
    sig = list(card_signature(card))
    sig[4] = None
    sig[5] = tuple(" ".join(r.split()) for r in sig[5]
                   if not _REMINDER_RE.match(" ".join(r.split())))
    return tuple(sig)


# Records pokemontcg.io has wrong, checked against TCGdex. Applied to every
# fetch, so a re-fetch cannot quietly bring the error back.
DATA_FIXES = {
    # Listed as a Pokemon Tool with its effect as a rules line; TCGdex lists
    # it as an Item. The text ("Search your deck for a Basic Fire Energy card
    # and a Basic Lightning Energy card ... put them into your hand") only
    # does anything when played, so as a Tool it was attached and never used.
    "Adventure Lantern": {"subtypes": ["Item"]},
}


def apply_data_fixes(cards):
    for card in cards:
        fix = DATA_FIXES.get(card.get("name"))
        if fix:
            card.update(fix)
    return cards


def merge_set(pool, fetched, set_id):
    """Merge one set's cards into an existing pool without re-fetching the
    rest of it.

    A full re-fetch re-reads every card, so any text the API corrected in
    another set lands in the same commit as the new set, and a field result
    from before can no longer be told apart from a change in the pool. This
    adds only the new set: a card with the same gameplay as a pool record
    becomes another printing of it, the rest become new records (deduped
    among themselves the same way).

    Records marked `provisional` for this set (cards typed in from another
    source before the API carried them) are dropped: the API's own version
    replaces them. Returns (pool, added, reprints, dropped).
    """
    dropped = [c for c in pool
               if c.get("provisional") and (c.get("set") or {}).get("id") == set_id]
    pool = [c for c in pool if c not in dropped]
    by_sig = {reprint_key(c): c for c in pool}
    old_sigs = set(by_sig)
    added = reprints = 0
    for card in fetched:
        if card.get("regulationMark") not in ACTIVE_REGULATION_MARKS:
            continue
        entry = [set_code_of(card), str(card.get("number"))]
        sig = reprint_key(card)
        kept = by_sig.get(sig)
        if kept is not None and card.get("subtypes") and kept.get("subtypes") \
                and card["subtypes"] != kept["subtypes"]:
            kept = None                  # same text, different card kind
        if kept is None:
            card["printings"] = []
            by_sig[sig] = kept = card
            pool.append(card)
            added += 1
        elif sig in old_sigs:
            reprints += 1
        if entry[0] and entry not in [list(p) for p in kept["printings"]]:
            kept["printings"].append(entry)
            kept["printings"].sort()
    return pool, added, reprints, dropped


def main():
    check_only = "--check" in sys.argv
    if "--merge-set" in sys.argv:
        set_id = sys.argv[sys.argv.index("--merge-set") + 1]
        with open(OUTPUT_FILE) as f:
            pool = json.load(f)
        fetched = apply_data_fixes(fill_set_codes(fetch_set(set_id)))
        missing = sorted({c["number"] for c in fetched if not set_code_of(c)})
        if missing:
            # Without a set code a card has no printing, and no decklist line
            # can name it: a pool written now would look complete and not be.
            sys.exit(f"{set_id}: {len(missing)} cards have no set code "
                     f"(the API's set record could not be read); nothing written")
        pool, added, reprints, dropped = merge_set(pool, fetched, set_id)
        print(f"{set_id}: {len(fetched)} fetched, {added} new records, "
              f"{reprints} reprints of pool cards, "
              f"{len(dropped)} provisional records replaced"
              + (f" ({', '.join(c['name'] for c in dropped)})" if dropped else ""))
        if check_only:
            print("  nothing written")
            return
        with open(OUTPUT_FILE, "w") as f:
            json.dump(pool, f, indent=4)
        print(f"Saved {len(pool)} cards to {OUTPUT_FILE}")
        return
    cards = apply_data_fixes(fetch_all_standard_cards())

    # Each card was already fetched by an exact regulationMark:X query, so no
    # further regulation-mark filtering is needed here (unlike the old
    # legalities.standard:legal-based fetch, which needed a second filter
    # pass to route around that field's staleness -- see the comment above
    # ACTIVE_REGULATION_MARKS for why that didn't fully work).
    print(f"Fetched {len(cards)} cards across regulation marks {sorted(ACTIVE_REGULATION_MARKS)}")

    unique_cards = dedupe_by_signature(cards)
    print(f"Deduped cosmetic reprints (alt art, rarity, etc.): {len(unique_cards)} unique cards")

    # --check reports what WOULD change and writes nothing. The output file is
    # the input to every measurement in this repo, so "is the pool current?"
    # must be answerable without risking it on an API having a bad day.
    if check_only:
        try:
            with open(OUTPUT_FILE) as f:
                on_disk = json.load(f)
        except FileNotFoundError:
            on_disk = []
        have = {c["name"] for c in on_disk}
        fetched_names = {c["name"] for c in unique_cards}
        new_names = sorted(fetched_names - have)
        gone = sorted(have - fetched_names)
        # Records and NAMES are different counts -- a name can hold more than
        # one record when two printings differ in gameplay text (Ultra Ball
        # MEG 131 and ASC 213 are separate records). Print both, labelled, so
        # the comparison is not read as a discrepancy.
        print(f"\n--check: {len(unique_cards)} records fetched "
              f"({len(fetched_names)} distinct names) vs {len(on_disk)} "
              f"records on disk ({len(have)} distinct names)")
        print(f"  new names: {len(new_names)}"
              + (f" -> {', '.join(new_names[:12])}" if new_names else ""))
        print(f"  names on disk but not fetched: {len(gone)}"
              + (f" -> {', '.join(gone[:12])}" if gone else ""))
        print("  nothing written")
        return

    with open(OUTPUT_FILE, "w") as f:
        json.dump(unique_cards, f, indent=4)

    print(f"Saved {len(unique_cards)} cards to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
