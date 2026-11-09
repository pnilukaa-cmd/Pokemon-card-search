"""How a mill deck wins: every attack (cards milled from the opponent's
deck, Maushold in play), how each game ended, the Prizes it gave up.
measure_mill.py DECK GAMES_PER_OPP opp1.txt ..."""
import contextlib, io, os, random, re, sys, collections
sys.path.insert(0, os.environ.get("TREE", "/home/user/Pokemon-card-search"))
os.chdir(os.environ.get("TREE", "/home/user/Pokemon-card-search"))
import simulate_versus as SV
deck, games, opps = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
A = SV.load_model(deck, "me")[0]
rows = []
orig_attack = SV.do_attack

def do_attack(pl, opp, log):
    if pl.name != "me" or pl.active is None:
        return orig_attack(pl, opp, log)
    d0, h0, n0 = len(opp.deck), len(opp.hand), len(log)
    maus = sum(1 for p in pl.in_play() if p.name == "Maushold")
    r = orig_attack(pl, opp, log)
    line = next((l for l in log[n0:] if " uses " in l and l.strip().startswith("me:")), None)
    if line:
        m = re.search(r"me: (.+?) uses (.+?)(?: for (\d+)[^>]*)?(?: ->|$)", line.strip())
        if m:
            rows.append(dict(who=m.group(1).split(" (")[0], atk=m.group(2), milled=d0 - len(opp.deck),
                             maus=maus, opp_deck=len(opp.deck), ko=any("KO on" in l for l in log[n0:])))
    return r

SV.do_attack = do_attack
res, per_opp, ends = [], {}, collections.Counter()
for i, o in enumerate(opps):
    B = SV.load_model(o, "opp")[0]
    random.seed(4000 + i); w = 0
    for _ in range(games):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r = SV.run_game(A, B, verbose=True)
        out = buf.getvalue()
        why = re.findall(r"(me|opp) loses: (\w+)", out)
        end = ("win " if r["winner"] == "me" else "loss ") + (why[-1][1] if why else "prizes")
        ends[end] += 1; w += r["winner"] == "me"
        res.append(dict(win=r["winner"] == "me", end=end, turns=r["turns"], gave=6 - r["prizes_b"],
                        took=6 - r["prizes_a"]))
    per_opp[os.path.basename(o)[:-4]] = w / games
n = len(res)
print(f"wins {sum(x['win'] for x in res)}/{n}")
for k, v in per_opp.items(): print(f"  {k:40s} {v * 100:5.1f}%")
print("game ends:", dict(ends))
print(f"turns a game {sum(x['turns'] for x in res) / n:.1f}; Prizes the opponent took {sum(x['gave'] for x in res) / n:.2f};"
      f" Prizes this deck took {sum(x['took'] for x in res) / n:.2f}")
by = collections.defaultdict(list)
for r in rows: by[(r["who"], r["atk"])].append(r)
print(f"\nattacks per game {len(rows) / n:.2f}, cards milled by attacks {sum(r['milled'] for r in rows) / n:.1f} a game")
for (who, atk), rs in sorted(by.items(), key=lambda kv: -len(kv[1])):
    print(f"  {who:12s} {atk:18s} {len(rs) / n:5.2f}/game  milled {sum(r['milled'] for r in rs) / len(rs):4.2f} each"
          f"  Maushold in play {sum(r['maus'] for r in rs) / len(rs):3.1f}  KO {sum(r['ko'] for r in rs) / len(rs) * 100:3.0f}%")
g = [r for r in rows if r["atk"] == "Gnaw Together"]
if g:
    print("\nGnaw Together by Maushold in play: n, milled each")
    for k in range(0, 6):
        h = [r for r in g if r["maus"] == k]
        if h: print(f"  {k}: {len(h):4d}  {sum(r['milled'] for r in h) / len(h):4.2f}")
