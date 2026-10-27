"""Score every attack a copy attacker could borrow, as it would use it.

Mew ex's Memory Helix uses the attacks of any of your Benched Pokemon, and
the Energy is paid by Mew. So the question for a Mew deck is which attacks,
at a given Energy cost, do the most when MEW uses them. "This Pokemon" in a
borrowed attack is the copier (Mega Gallade ex's "if this Pokemon has no
damage counters" reads Mew's), and the donor only has to sit on the Bench.

For every printing in the pool with an attack of exactly COST Energy: the
copier Active with COST Energy of the attack's type (Colorless: Psychic),
the donor and two other Pokemon on the Bench, against the named Active of a
field deck (3 Energy on it, 6 cards in hand, its real list as the cards we
can't see). Damage is the mean over 40 seeds, so coin flips read as their
expected value; "rider" is the engine's value for everything else the
attack does. Both are this one board, not a matchup result.

Usage:  python3 copy_attack_scan.py OPP_DECK "OPP ACTIVE" OUT.json [COST] [top N]
"""
import collections
import json
import os
import random
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tcg_model as M
import simulate_versus as V

COPIER = "Mew ex 30C 152"


def main():
    opp_deck, opp_active, out = sys.argv[1], sys.argv[2], sys.argv[3]
    cost_n = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    top = int(sys.argv[5]) if len(sys.argv) > 5 else 30
    cards = M.load_cards()
    V._CARDS_BY_NAME.update(M.build_card_index(cards)[0])
    V.RETALIATE_CARDS = V.build_retaliate_index(cards)
    O = V.load_model(opp_deck, "o")[0]
    EO = V.compile_effects_for(O[1], O[3])
    copier = COPIER.rsplit(" ", 2)[0]

    def paid(a):
        return [x for x in (a.get("cost") or []) if x != "Free"]
    # One model can hold one printing of a name, so printings go in batches.
    byname = collections.defaultdict(list)
    for c in cards:
        if c.get("supertype") != "Pokémon" or c["name"] == copier:
            continue
        if any(len(paid(a)) == cost_n for a in c.get("attacks") or []):
            code = c["set"].get("ptcgoCode") or (c.get("printings") or [["?"]])[0][0]
            byname[c["name"]].append(f"{c['name']} {code} {c['number']}")
    rows = []
    for k in range(max(len(v) for v in byname.values())):
        batch = [v[k] for v in byname.values() if len(v) > k]
        text = (f"Pokémon: {len(batch) + 1}\n1 {COPIER}\n" + "".join(f"1 {b}\n" for b in batch)
                + "\nEnergy: 10\n10 Basic Psychic Energy\n")
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
            f.write(text)
        try:
            D = V.load_model(f.name, "me")[0]
        finally:
            os.unlink(f.name)
        E = V.compile_effects_for(D[1], D[3])
        fill = [n for n in D[1] if D[1][n]["stage"] == "Basic" and n != copier][:3]
        for b in batch:
            name = b.rsplit(" ", 2)[0]
            info = D[1].get(name)
            for atk in (info or {}).get("attacks") or []:
                cost = paid(atk)
                if len(cost) != cost_n:
                    continue
                types = ["Psychic" if t == "Colorless" else t for t in cost]
                me, op = V.Player("me", D[1], list(D[2]), E), V.Player("o", O[1], list(O[2]), EO)
                me.round_no = op.round_no = 5
                me._opp_ref, op._opp_ref = op, me
                me.energy_types = set(types)
                op.energy_types = {t for p in O[1].values() for a in p.get("attacks") or []
                                   for t in a.get("cost") or [] if t != "Colorless"}
                me.active = V.InPlay(copier, 1)
                me.active.energy = [[t] for t in types]
                me.active.energy_names = [f"{t} Energy" for t in types]
                me.bench = [V.InPlay(name, 1)] + [V.InPlay(x, 1) for x in fill if x != name][:2]
                me.hand = [("Energy", "Psychic Energy")] * 3 + [("Pokemon", fill[0])] * 3
                me.discard = fill[:2] + ["Psychic Energy"] * 3
                me.deck = [("Energy", "Psychic Energy")] * 30
                me.prizes = op.prizes = 4
                op.active = V.InPlay(opp_active, 1)
                op.active.energy = [["Colorless"]] * 3
                op.active.energy_names = ["Energy"] * 3
                op.bench = [V.InPlay(n, 1) for n in O[1] if n != opp_active][:3]
                op.hand = [c for c in O[2] if c[0] != "Energy"][:4] + \
                    [c for c in O[2] if c[0] == "Energy"][:2]
                op.deck = list(O[2])
                random.seed(1)
                random.shuffle(op.deck)
                lent = any(a["name"] == atk["name"]
                           for a in V.AE.query_extra_attacks(me, me.active))
                tot = 0
                for sd in range(40):
                    random.seed(sd)
                    tot += V.attack_damage(me, op, me.active, atk, record=False)
                rider = V.attack_rider_value(me, op, atk, me.active)
                subs = info.get("subtypes") or []
                rows.append({"card": b, "stage": info["stage"], "mega": "MEGA" in subs,
                             "ex": info.get("prize_value", 1) >= 2, "hp": info.get("hp"),
                             "evolves_from": info.get("evolves_from"), "cost": cost,
                             "attack": atk["name"], "printed": atk.get("damage"),
                             "text": atk.get("text") or "", "lent": lent,
                             "damage": round(tot / 40), "rider": round(rider, 1)})
    json.dump(rows, open(out, "w"), indent=0)
    rows.sort(key=lambda r: -(r["damage"] + r["rider"]))
    print(f"{len(rows)} attacks costing {cost_n} scored as {copier} against {opp_active}")
    for r in rows[:top]:
        tag = r["stage"] + (" MEGA" if r["mega"] else "") + (" ex" if r["ex"] else "")
        print(f"{r['damage']:4d} +{r['rider']:5.0f}  {tag:16s} {r['card']:28s} "
              f"{'/'.join(r['cost'])} {r['attack']}")


if __name__ == "__main__":
    main()
