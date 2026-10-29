"""Turns an Active Mega Froslass ex ends without attacking and without
Water, and where the deck's Energy went. water.py DECK GAMES opp..."""
import os, sys, random, collections, contextlib, io, re
sys.path.insert(0, "/home/user/Pokemon-card-search"); os.chdir("/home/user/Pokemon-card-search")
import simulate_versus as SV
deck, games, opps = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
A = SV.load_model(deck, "me")[0]
c = collections.Counter(); att = collections.Counter(); attacked = [False]
orig_fin, orig_atk = SV.finish_turn, SV.do_attack
def atk(pl, opp, log):
    n0 = len(log); r = orig_atk(pl, opp, log)
    if pl.name == "me" and any(" uses " in l and "me:" in l for l in log[n0:]):
        attacked[0] = True
    return r
def fin(pl, opp, log):
    if pl.name == "me" and pl.round_no >= 2:
        a = pl.active
        if a is not None and a.name == "Mega Froslass ex":
            c["Froslass Active turns"] += 1
            water = any("Water" in e for e in a.energy)
            if not attacked[0]:
                c["no attack"] += 1
                if not water: c["no attack, no Water on it"] += 1
                if not water and not any(k == "Energy" for k, _ in pl.hand): c["  ...and no Energy in hand"] += 1
    attacked[0] = False
    return orig_fin(pl, opp, log)
SV.finish_turn, SV.do_attack = fin, atk
n = 0
for i, o in enumerate(opps):
    B = SV.load_model(o, "opp")[0]
    random.seed(4000 + i)
    for _ in range(games):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            SV.run_game(A, B, verbose=True)
        n += 1
        for ln in buf.getvalue().splitlines():
            m = re.match(r"\s*me: attaches (.+?) to (.+)$", ln)
            if m: att[(m.group(1), m.group(2).split(" (")[0])] += 1
print(f"games {n}")
for k in ["Froslass Active turns", "no attack", "no attack, no Water on it", "  ...and no Energy in hand"]:
    print(f"  {k:32s} {c[k] / n:5.2f} a game")
print("  attachments a game:", ", ".join(f"{e.split()[0]}->{p} {v / n:.2f}" for (e, p), v in att.most_common(10)))
