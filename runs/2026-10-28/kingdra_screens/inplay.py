"""Share of a deck's own turns (from turn 3) with each named Pokemon in play,
and King's Order uses that passed up a Knock Out. inplay.py DECK GAMES NAMES opp..."""
import os, sys, random, collections
sys.path.insert(0, "/home/user/Pokemon-card-search"); os.chdir("/home/user/Pokemon-card-search")
import simulate_versus as SV
deck, games, names, opps = sys.argv[1], int(sys.argv[2]), sys.argv[3].split(","), sys.argv[4:]
A = SV.load_model(deck, "me")[0]
cnt, turns, ko_skips, ko_uses = collections.Counter(), [0], [0], [0]
orig_fin, orig_atk = SV.finish_turn, SV.do_attack
def fin(pl, opp, log):
    if pl.name == "me" and pl.round_no >= 3:
        turns[0] += 1
        have = set(pl.in_play_names())
        for n in names:
            cnt[n] += n in have
    return orig_fin(pl, opp, log)
def atk(pl, opp, log):
    n0 = len(log)
    if pl.name == "me" and pl.active is not None and pl.active.name == "Kingdra ex" and opp.active is not None:
        hp = next((a for a in pl.POKEMON["Kingdra ex"]["attacks"] if a["name"] == "Hydro Pump"), None)
        could = hp is not None and SV.can_pay(SV.effective_cost(pl, pl.active, hp["cost"], opp), pl.active.energy) \
            and SV.attack_damage(pl, opp, pl.active, hp, record=False) >= SV.effective_hp(opp, opp.active) - opp.active.damage
        r = orig_atk(pl, opp, log)
        if any("King's Order" in l for l in log[n0:]):
            ko_uses[0] += 1
            ko_skips[0] += bool(could)
        return r
    return orig_atk(pl, opp, log)
SV.finish_turn, SV.do_attack = fin, atk
for i, o in enumerate(opps):
    B = SV.load_model(o, "opp")[0]
    random.seed(4000 + i)
    for _ in range(games):
        SV.run_game(A, B)
t = max(turns[0], 1)
print(os.path.basename(deck), f"{turns[0]} turns:", ", ".join(f"{n} {100*cnt[n]/t:.0f}%" for n in names),
      f"| King's Order {ko_uses[0]}, of which Hydro Pump could have Knocked Out {ko_skips[0]}")
