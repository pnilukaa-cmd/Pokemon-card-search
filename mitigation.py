"""How much damage a deck's walls take off, measured in play.

For every attack the opponent lands on this deck's Active, records the damage
before mitigation (after Weakness and Resistance), whether it was prevented
outright, and how much the reductions took off: Abilities and Stadiums
(Tundra Wall, Curly Wall), the Tool on the Active (Sacred Charm, Berries) and
one-turn shields (Jasmine's Gaze, Frost Barrier), read off the damage the
Active actually took. Each hit counts up to the HP the Active had left. A
list of "takes N less damage" cards says what could happen; this says what
did.

Two things a wall does besides taking less, per game: the HP its heals
took back off its Pokemon (Jumbo Ice Cream, Cook, Good Sleep), and the
Energy its disruption took off the opponent's (Crushing Hammer). Both are
read off the board around each effect this deck resolves.

Usage:  python3 mitigation.py <deck.txt> <field_dir> <games per opponent> [tag]

Same per-opponent seeding as vs_field.py.
"""
import glob
import hashlib
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import simulate_versus as SV
import ability_engine as AE
import ability_ir as IR

deck, field, games = sys.argv[1], sys.argv[2], int(sys.argv[3])
tag = sys.argv[4] if len(sys.argv) > 4 else "mt1"
me = os.path.splitext(os.path.basename(deck))[0]
A = SV.load_model(deck, me)[0]

hits = []            # {"raw", "prevented", "taken"} per hit on this deck's Active


def _on_me(defender):
    return getattr(defender, "name", None) == me and not SV._LOOKAHEAD[0]


_prevented = AE.query_prevented


def query_prevented(pl, spot, opp=None, attacker=None, amount=None):
    out = _prevented(pl, spot, opp, attacker, amount)
    # Only the attack's own damage step passes the hit's amount.
    if amount is not None and _on_me(pl) and spot is pl.active and _pending:
        _pending[-1].update(raw=amount, prevented=bool(out))
    return out


AE.query_prevented = query_prevented
_pending = []
_do_attack = SV.do_attack


def do_attack(pl, opp, log, *a, **k):
    """The damage the Active actually took, whatever took it off."""
    if not _on_me(opp) or opp.active is None:
        return _do_attack(pl, opp, log, *a, **k)
    spot, before = opp.active, opp.active.damage
    # A hit counts up to the HP the Active had left: "Knock Out the Active"
    # attacks report a sentinel, not a number.
    left = max(0, SV.effective_hp(opp, spot) - before)
    _pending.append({})
    try:
        return _do_attack(pl, opp, log, *a, **k)
    finally:
        h = _pending.pop()
        if "raw" in h and h["raw"] > 0:        # an attack that dealt no damage is no hit
            h["raw"] = min(h["raw"], left)
            h["taken"] = min(max(0, spot.damage - before), left)
            hits.append(h)


SV.do_attack = do_attack

healed = [0]           # HP healed off this deck's Pokemon
stripped = [0]         # Energy removed from the opponent's Pokemon
_apply = AE.apply_action


def apply_action(act, pl, opp, *a, **k):
    if getattr(pl, "name", None) != me or SV._LOOKAHEAD[0] or act.op not in (
            IR.Op.HEAL, IR.Op.DISCARD_ENERGY_FROM_OPPONENT):
        return _apply(act, pl, opp, *a, **k)
    dmg = sum(p.damage for p in pl.in_play())
    energy = sum(p.energy_count() for p in opp.in_play()) if opp is not pl else 0
    out = _apply(act, pl, opp, *a, **k)
    if act.op == IR.Op.HEAL:
        healed[0] += max(0, dmg - sum(p.damage for p in pl.in_play()))
    elif opp is not pl:
        stripped[0] += max(0, energy - sum(p.energy_count() for p in opp.in_play()))
    return out


AE.apply_action = apply_action
played = [0]

for f in sorted(glob.glob(os.path.join(field, "*.txt"))):
    opp = os.path.splitext(os.path.basename(f))[0]
    if os.path.abspath(f) == os.path.abspath(deck):
        continue
    B = SV.load_model(f, opp)[0]
    if opp == me:
        B = (opp + "_opp",) + B[1:]
    random.seed(int(hashlib.sha256(f"{tag}|{opp}".encode()).hexdigest()[:12], 16))
    SV._LOOKAHEAD_SEQ[0] = 0
    for _ in range(games):
        SV.run_game(A, B)
        played[0] += 1

n = len(hits)
if not n:
    print(f"{me}: no hits recorded")
    sys.exit()
raw = sum(h["raw"] for h in hits)
taken = sum(min(h["taken"], h["raw"]) for h in hits)
prev = sum(1 for h in hits if h["prevented"])
print(f"{me}: {n} damaging attacks on the Active, {games} games against each field deck")
print(f"  average hit before mitigation   {raw / n:6.1f}")
print(f"  prevented outright              {100.0 * prev / n:5.1f}% of hits")
print(f"  average damage taken            {taken / n:6.1f} per hit")
print(f"  share of damage mitigated       {100.0 * (raw - taken) / max(raw, 1):5.1f}%")
print(f"  HP healed per game              {healed[0] / played[0]:6.1f}")
print(f"  opponent's Energy removed/game  {stripped[0] / played[0]:6.2f}")
