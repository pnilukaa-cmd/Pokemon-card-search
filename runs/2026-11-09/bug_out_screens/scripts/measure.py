"""How a Bug Out deck plays: every attack, and for Bug Out where its Bug
Out Pokémon were. measure.py DECK GAMES_PER_OPP opp1.txt ..."""
import contextlib, io, os, random, re, sys, collections
sys.path.insert(0, os.environ.get("TREE", "/home/user/Pokemon-card-search"))
os.chdir(os.environ.get("TREE", "/home/user/Pokemon-card-search"))
import simulate_versus as SV, ability_engine as AE
deck, games, opps = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
A = SV.load_model(deck, "me")[0]
rows, ends, turns = [], collections.Counter(), collections.Counter()
orig_attack = SV.do_attack
SPEC = {"pokemon": True, "attack": "Bug Out"}

def do_attack(pl, opp, log):
    if pl.name != "me" or pl.active is None:
        return orig_attack(pl, opp, log)
    hit = lambda c: SV._reveal_match(pl, c, SPEC)
    kb = AE.known_bottom(pl)
    snap = dict(deck=len(pl.deck), in_deck=sum(map(hit, pl.deck)), bottom7=sum(map(hit, pl.deck[:7])),
                known=sum(map(hit, kb[:7])), in_play=sum(1 for p in pl.in_play() if hit(("Pokemon", p.name))),
                in_hand=sum(map(hit, pl.hand)), in_disc=sum(1 for n in pl.discard if hit(("Pokemon", n))),
                bench=len(pl.bench), rnd=pl.round_no)
    p0, n0 = pl.prizes, len(log)
    r = orig_attack(pl, opp, log)
    line = next((l for l in log[n0:] if " uses " in l and l.strip().startswith("me:")), None)
    if line:
        m = re.search(r"me: (.+?) uses (.+?)(?: for (\d+)[^>]*)?(?: ->|$)", line.strip())
        if m:
            rows.append(dict(snap, who=m.group(1), atk=m.group(2), dmg=int(m.group(3) or 0),
                             prizes=p0 - pl.prizes, ko=any("KO on" in l for l in log[n0:])))
    return r

SV.do_attack = do_attack
wins = n = 0
per_opp = {}
for i, o in enumerate(opps):
    B = SV.load_model(o, "opp")[0]
    random.seed(3000 + i); w = 0
    for _ in range(games):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r = SV.run_game(A, B, verbose=True)
        n += 1; w += r["winner"] == "me"
        out = buf.getvalue()
        why = re.findall(r"(me|opp) loses: (\w+)", out)
        ends[("win " if r["winner"] == "me" else "loss ") + (why[-1][1] if why else "prizes")] += 1
        turns[r["turns"] // 4] += 1
    wins += w; per_opp[os.path.basename(o)[:-4]] = w / games
print(f"wins {wins}/{n}")
for k, v in per_opp.items(): print(f"  {k:40s} {v * 100:5.1f}%")
print("game ends:", dict(ends))
by = collections.defaultdict(list)
for r in rows: by[(r["who"].split(" (")[0], r["atk"])].append(r)
tot = sum(r["prizes"] for r in rows)
print(f"\nattacks per game {len(rows) / n:.2f}, Prizes from attacks {tot / n:.2f} a game")
for (who, atk), rs in sorted(by.items(), key=lambda kv: -len(kv[1])):
    p = sum(r["prizes"] for r in rs)
    print(f"  {who:14s} {atk:20s} {len(rs) / n:5.2f}/game  avg dmg {sum(r['dmg'] for r in rs) / len(rs):5.0f}"
          f"  KO {sum(r['ko'] for r in rs) / len(rs) * 100:3.0f}%  Prizes {p / n:4.2f}/game ({p / max(1, tot) * 100:3.0f}%)")
bo = [r for r in rows if r["atk"] == "Bug Out"]
if bo:
    k = len(bo)
    print(f"\nBug Out, {k} attacks: avg Bug Out Pokémon in the bottom 7 {sum(r['bottom7'] for r in bo) / k:.2f}"
          f" (known {sum(r['known'] for r in bo) / k:.2f}); in deck {sum(r['in_deck'] for r in bo) / k:.1f}"
          f" of {sum(r['deck'] for r in bo) / k:.1f} cards; in play {sum(r['in_play'] for r in bo) / k:.1f},"
          f" hand {sum(r['in_hand'] for r in bo) / k:.1f}, discard {sum(r['in_disc'] for r in bo) / k:.1f}")
    print("  hits in the bottom 7:", dict(sorted(collections.Counter(r["bottom7"] for r in bo).items())))
    print("  attacker:", dict(collections.Counter(r["who"].split(" (")[0] for r in bo)))
