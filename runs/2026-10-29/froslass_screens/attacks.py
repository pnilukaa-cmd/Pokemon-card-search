"""How a hand-size deck takes its Prizes: each of its attacks, the opposing
hand size it hit, the cards it added to that hand itself that turn, and the
Prizes it took. attacks.py DECK GAMES_PER_OPP opp1.txt ..."""
import contextlib, io, os, random, re, sys, collections
sys.path.insert(0, os.environ.get("TREE", "/home/user/Pokemon-card-search"))
os.chdir("/home/user/Pokemon-card-search")
import simulate_versus as SV
deck, games, opps = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
A = SV.load_model(deck, "me")[0]
rows, turn_start, ends = [], {}, collections.Counter()
orig_turn, orig_attack = SV.take_turn, SV.do_attack

def take_turn(pl, opp, *a, **k):
    if pl.name == "me":
        turn_start["h"] = len(opp.hand)
        turn_start["n"] = turn_start.get("n", 0) + 1
    return orig_turn(pl, opp, *a, **k)

def do_attack(pl, opp, log):
    if pl.name != "me" or pl.active is None:
        return orig_attack(pl, opp, log)
    h, p0, n0 = len(opp.hand), pl.prizes, len(log)
    r = orig_attack(pl, opp, log)
    line = next((l for l in log[n0:] if " uses " in l and l.strip().startswith("me:")), None)
    if line:
        m = re.search(r"me: (.+?) uses (.+?)(?: for (\d+)[^>]*)?(?: ->|$)", line.strip())
        if m:
            rows.append(dict(who=m.group(1), atk=m.group(2), dmg=int(m.group(3) or 0),
                             hand=h, added=h - turn_start["h"], prizes=p0 - pl.prizes,
                             ko=any("KO on" in l for l in log[n0:])))
    return r

SV.take_turn, SV.do_attack = take_turn, do_attack
wins = n = 0
per_opp = {}
for i, o in enumerate(opps):
    B = SV.load_model(o, "opp")[0]
    random.seed(2000 + i); w = 0
    for _ in range(games):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r = SV.run_game(A, B, verbose=True)
        n += 1; w += r["winner"] == "me"
        out = buf.getvalue()
        if r["winner"] == "me":
            ends["prizes" if r["prizes_a"] <= 0 else
                 ("opponent decked out" if "opp loses: deck_out" in out else
                  "opponent out of Pokémon" if "opp loses: no_pokemon" in out else "no Pokémon left after a KO")] += 1
        else:
            ends["lost"] += 1
    wins += w; per_opp[os.path.basename(o)[:-4]] = w / games
print(f"wins {wins}/{n}")
for k, v in per_opp.items(): print(f"  {k:40s} {v * 100:5.1f}%")
print("game ends:", dict(ends))
by = collections.defaultdict(list)
for r in rows: by[(r["who"].split(" (")[0], r["atk"])].append(r)
tot_p = sum(r["prizes"] for r in rows)
print(f"\nattacks per game {len(rows) / n:.2f}, Prizes from attacks {tot_p / n:.2f} a game")
for (who, atk), rs in sorted(by.items(), key=lambda kv: -sum(r['prizes'] for r in kv[1])):
    p = sum(r["prizes"] for r in rs)
    print(f"  {who:18s} {atk:20s} {len(rs) / n:5.2f}/game  KO {sum(r['ko'] for r in rs) / len(rs) * 100:4.0f}%"
          f"  Prizes {p / n:4.2f}/game ({p / max(1, tot_p) * 100:3.0f}%)  hand avg {sum(r['hand'] for r in rs) / len(rs):4.1f}"
          f"  added that turn {sum(r['added'] for r in rs) / len(rs):+4.1f}")
rr = [r for r in rows if r["atk"] == "Resentful Refrain"]
if rr:
    print("\nResentful Refrain by opposing hand size: n  KO%  share of its Prizes")
    hp = sum(r["prizes"] for r in rr)
    for h in range(0, 13):
        g = [r for r in rr if min(r["hand"], 12) == h]
        if g: print(f"  {h:2d}{'+' if h == 12 else ' '} {len(g):5d} {sum(r['ko'] for r in g) / len(g) * 100:5.0f}%  {sum(r['prizes'] for r in g) / max(1, hp) * 100:4.0f}%")
    print("  cards the deck itself added that turn (Alluring Light, Lucian):",
          dict(sorted(collections.Counter(max(-3, min(r['added'], 4)) for r in rr).items())))
