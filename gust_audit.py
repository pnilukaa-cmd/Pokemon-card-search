"""Why Boss's Orders sat in hand: on each of a deck's turns with Boss's
Orders in hand and a Benched target, what the AI did with it.

  played          -- it was played (for a Knock Out, or to strand)
  other Supporter -- a target was there, but another Supporter went first
  Active is the KO -- the Active could be Knocked Out for as many Prizes
  no Knock Out    -- the Active could attack, but nothing on their Bench
                     could be Knocked Out (or stranded)
  no attacker     -- the Active couldn't attack this turn, even with the
                     Energy still to attach

Same per-opponent seeding as vs_field.py for a given tag.

Usage:  python3 gust_audit.py <deck.txt> <field_dir> <games> [tag]
"""
import collections
import glob
import hashlib
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import simulate_versus as SV

BOSS = ("Supporter", "Boss's Orders")
ORDER = ("played", "other Supporter", "Active is the KO", "no Knock Out", "no attacker")


def _can_attack(pl, opp):
    """Could the Active attack this turn, counting the Energy still to be
    attached from hand?"""
    a = pl.active
    n_e, n_names = len(a.energy), len(a.energy_names)
    extra = SV._helpful_energy(pl, a)
    if extra is not None:
        name = pl.hand[extra][1]
        a.energy.extend(SV._provisions_on(pl, name, a.name))
        a.energy_names.append(name)
    try:
        return SV._ready_damage(pl, opp, a) > 0
    finally:
        del a.energy[n_e:], a.energy_names[n_names:]


def classify(pl, opp):
    """What stood between this turn and a Boss's Orders, before the
    Supporter is chosen. None when Boss's Orders isn't in hand."""
    if BOSS not in pl.hand or not opp.bench or opp.active is None or pl.active is None:
        return None
    if SV.choose_gust_target(pl, opp) is not None:
        return "target"
    if not _can_attack(pl, opp):
        return "no attacker"
    if SV._ko_this_turn(pl, opp, opp.active):
        return "Active is the KO"
    return "no Knock Out"


def main():
    deck, field, games = sys.argv[1], sys.argv[2], int(sys.argv[3])
    tag = sys.argv[4] if len(sys.argv) > 4 else "ga1"
    me = os.path.splitext(os.path.basename(deck))[0]
    A = SV.load_model(deck, me)[0]
    count = collections.Counter()
    turns = [0]
    orig = SV.play_supporter

    def spy(pl, opp, turn, log):
        mine = pl.name == me and not pl.supporter_played
        why = classify(pl, opp) if mine else None
        r = orig(pl, opp, turn, log)
        if why is None:
            return r
        turns[0] += 1
        if why == "target":
            why = "played" if "Boss's Orders" in pl.played_supporters_this_turn else "other Supporter"
        count[why] += 1
        return r

    SV.play_supporter = spy
    n = 0
    for f in sorted(glob.glob(os.path.join(field, "*.txt"))):
        if os.path.abspath(f) == os.path.abspath(deck):
            continue
        opp = os.path.splitext(os.path.basename(f))[0]
        B = SV.load_model(f, opp + ("_opp" if opp == me else ""))[0]
        random.seed(int(hashlib.sha256(f"{tag}|{opp}".encode()).hexdigest()[:12], 16))
        for _ in range(games):
            SV.run_game(A, B)
            n += 1
    t = max(turns[0], 1)
    print(f"{me}: {n} games, {turns[0]} turns with Boss's Orders in hand ({turns[0]/n:.2f} a game)")
    for k in ORDER:
        print(f"  {k:17s} {100*count[k]/t:5.1f}%  ({count[k]/n:.2f} a game)")


if __name__ == "__main__":
    main()
