"""One candidate deck against every playable deck in a field directory.

Same seeding scheme as roundrobin.py (one deterministic seed per pairing,
common random numbers), so two candidates run with the same tag face the
same dice and their difference is paired -- the Paralysis-vs-control
measurement depends on that. The candidate's own file is skipped if it
also sits in the field.

Usage:  python3 vs_field.py <deck.txt> <field_dir> <games> [tag] [out.json]
"""
import glob
import hashlib
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import simulate_versus as SV
import tcg_model as M

deck, field, games = sys.argv[1], sys.argv[2], int(sys.argv[3])
tag = sys.argv[4] if len(sys.argv) > 4 else "vf1"
out_path = sys.argv[5] if len(sys.argv) > 5 else None

_cards = M.load_cards()
by_name, by_setnum = M.build_card_index(_cards)


def basics_in(path):
    n = 0
    for e in M.parse_decklist_entries(open(path).read()):
        c, _ = M.resolve_card(e, by_name, by_setnum)
        if c and (c.get("supertype") == "Pokémon" or M.fossil_stats(c)) \
                and M.stage_of(c) == "Basic":
            n += e["count"]
    return n


me = os.path.splitext(os.path.basename(deck))[0]
A = SV.load_model(deck, me)[0]
res, unplayable = {}, []
for f in sorted(glob.glob(os.path.join(field, "*.txt"))):
    opp = os.path.splitext(os.path.basename(f))[0]
    if os.path.abspath(f) == os.path.abspath(deck):
        continue
    if basics_in(f) == 0:
        unplayable.append(opp)
        continue
    B = SV.load_model(f, opp)[0]
    if opp == me:                      # same slug, different file: keep names distinct
        B = (opp + "_opp",) + B[1:]
    seed = int(hashlib.sha256(f"{tag}|{opp}".encode()).hexdigest()[:12], 16)
    random.seed(seed)
    wins = sum(SV.run_game(A, B)["winner"] == A[0] for _ in range(games))
    res[opp] = wins
    print(f"  {opp:<50} {100.0 * wins / games:6.2f}", flush=True)

rates = [100.0 * w / games for w in res.values()]
mean = sum(rates) / len(rates)
# binomial SE of the mean over independent pairings
se = math.sqrt(sum(r * (100 - r) / games for r in rates)) / len(rates)
print(f"{me}: {mean:.2f}% (±{se:.2f}) over {len(rates)} decks at {games} games, "
      f"winning {sum(r > 50 for r in rates)}")
if unplayable:
    print("unplayable, skipped:", ", ".join(unplayable))
if out_path:
    json.dump({"deck": me, "games": games, "tag": tag, "results": res,
               "unplayable": unplayable}, open(out_path, "w"))
