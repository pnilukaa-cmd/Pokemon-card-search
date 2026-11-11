"""How a heal wall plays: each heal Item (damage before, healed, the
Stadium in play), each attack, the Prizes on both sides, how games end.
measure_wall.py DECK GAMES_PER_OPP opp1.txt ..."""
import contextlib, io, os, random, re, sys, collections
sys.path.insert(0, os.environ.get("TREE", "/home/user/Pokemon-card-search"))
os.chdir(os.environ.get("TREE", "/home/user/Pokemon-card-search"))
import simulate_versus as SV
deck, games, opps = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
A = SV.load_model(deck, "me")[0]
HEALS = {"Tasty Rice Ball", "Jumbo Ice Cream"}
heals, atks, stad = [], [], collections.Counter()
orig_tr, orig_atk = SV.play_trainer_from_ir, SV.do_attack

def tr(pl, opp, kind, name, log, turn, *a, **k):
    if pl.name == "me" and name in HEALS and pl.active is not None:
        before, who = pl.active.damage, pl.active.name
        r = orig_tr(pl, opp, kind, name, log, turn, *a, **k)
        if r:
            heals.append(dict(name=name, before=before, healed=before - pl.active.damage,
                              stadium=pl.stadium or pl._opp_stadium, who=who))
        return r
    return orig_tr(pl, opp, kind, name, log, turn, *a, **k)

def atk(pl, opp, log):
    if pl.name == "me":
        stad[pl.stadium or getattr(pl, "_opp_stadium", None) or "none"] += 1
    if pl.name != "me" or pl.active is None:
        return orig_atk(pl, opp, log)
    n0, p0 = len(log), pl.prizes
    r = orig_atk(pl, opp, log)
    line = next((l for l in log[n0:] if " uses " in l and l.strip().startswith("me:")), None)
    if line:
        m = re.search(r"me: (.+?) uses (.+?)(?: for (\d+)[^>]*)?(?: ->|$)", line.strip())
        if m:
            atks.append(dict(who=m.group(1).split(" (")[0], atk=m.group(2), dmg=int(m.group(3) or 0),
                             prizes=p0 - pl.prizes))
    return r

SV.play_trainer_from_ir, SV.do_attack = tr, atk
res, per_opp, ends, gave_by = [], {}, collections.Counter(), collections.Counter()
for i, o in enumerate(opps):
    B = SV.load_model(o, "opp")[0]
    random.seed(5000 + i); w = 0
    for _ in range(games):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            r = SV.run_game(A, B, verbose=True)
        out = buf.getvalue()
        for m in re.finditer(r"opp: KO on (.+?) \(\+(\d+) prizes?\)", out):
            gave_by[m.group(1).split(" (")[0]] += int(m.group(2))
        why = re.findall(r"(me|opp) loses: (\w+)", out)
        ends[("win " if r["winner"] == "me" else "loss ") + (why[-1][1] if why else "prizes")] += 1
        w += r["winner"] == "me"
        res.append(dict(turns=r["turns"], gave=6 - r["prizes_b"], took=6 - r["prizes_a"]))
    per_opp[os.path.basename(o)[:-4]] = w / games
n = len(res)
print(f"wins {sum(per_opp.values()) * games:.0f}/{n}")
for k, v in per_opp.items(): print(f"  {k:40s} {v * 100:5.1f}%")
print("game ends:", dict(ends))
print(f"turns {sum(x['turns'] for x in res) / n:.1f}; Prizes taken by the opponent {sum(x['gave'] for x in res) / n:.2f}, by this deck {sum(x['took'] for x in res) / n:.2f}")
print("Prizes given up, by the Pokemon Knocked Out:", {k: round(v / n, 2) for k, v in gave_by.most_common()})
by = collections.defaultdict(list)
for a in atks: by[(a["who"], a["atk"])].append(a)
print(f"\nattacks per game {len(atks) / n:.2f}")
for (who, nm), rs in sorted(by.items(), key=lambda kv: -len(kv[1])):
    print(f"  {who:18s} {nm:18s} {len(rs) / n:5.2f}/game  avg {sum(r['dmg'] for r in rs) / len(rs):4.0f}  Prizes {sum(r['prizes'] for r in rs) / n:4.2f}/game")
print("\nStadium in play at this deck's attack step:", {k: round(v / n, 2) for k, v in stad.most_common()})
for nm in sorted(HEALS):
    hs = [h for h in heals if h["name"] == nm]
    if hs:
        print(f"{nm}: {len(hs) / n:.2f}/game, damage before {sum(h['before'] for h in hs) / len(hs):.0f}, healed {sum(h['healed'] for h in hs) / len(hs):.0f}"
              f" (Trench up {sum(1 for h in hs if h['stadium'] == 'Legendary Trench') / len(hs) * 100:.0f}%), on {dict(collections.Counter(h['who'] for h in hs))}")
