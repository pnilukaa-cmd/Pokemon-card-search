"""What Snorlax does in a list: Collapse uses, Good Sleep heals and HP healed,
Snorlax Knock Outs taken, per game.  goodsleep.py deck.txt games_per_opp"""
import glob, hashlib, os, random, sys
sys.path.insert(0, "/home/user/Pokemon-card-search"); os.chdir("/home/user/Pokemon-card-search")
import simulate_versus as SV
deck, games = sys.argv[1], int(sys.argv[2])
me = os.path.splitext(os.path.basename(deck))[0]
A = SV.load_model(deck, me)[0]
st = {"games": 0, "collapse": 0, "heals": 0, "healed": 0, "snor_ko": 0, "turns_asleep": 0}
_chk = SV._checkup_abilities
def chk(pl, opp, log):
    if pl.name != me or SV._LOOKAHEAD[0]:
        return _chk(pl, opp, log)
    before = {id(p): p.damage for p in pl.in_play() if p.name == "Snorlax"}
    _chk(pl, opp, log)
    for p in pl.in_play():
        if id(p) in before and p.damage < before[id(p)]:
            st["heals"] += 1; st["healed"] += before[id(p)] - p.damage
SV._checkup_abilities = chk
_atk = SV.do_attack
def atk(pl, opp, log, *a, **k):
    if not SV._LOOKAHEAD[0]:
        if pl.name == me and pl.active is not None and pl.active.name == "Snorlax":
            st["collapse"] += 1
        tgt = opp.active
        r = _atk(pl, opp, log, *a, **k)
        if opp.name == me and tgt is not None and tgt.name == "Snorlax" and tgt not in opp.in_play():
            st["snor_ko"] += 1
        return r
    return _atk(pl, opp, log, *a, **k)
SV.do_attack = atk
for f in sorted(glob.glob("decks/field/*.txt")):
    opp = os.path.splitext(os.path.basename(f))[0]
    B = SV.load_model(f, opp)[0]
    random.seed(int(hashlib.sha256(f"gs1|{opp}".encode()).hexdigest()[:12], 16))
    for _ in range(games):
        SV.run_game(A, B); st["games"] += 1
g = st["games"]
print(f"{me}: {g} games")
print(f"  Snorlax attacks per game     {st['collapse']/g:.2f}")
print(f"  Good Sleep heals per game    {st['heals']/g:.2f}  ({st['healed']/max(st['heals'],1):.0f} HP each)")
print(f"  Snorlax Knocked Out per game {st['snor_ko']/g:.2f}")
