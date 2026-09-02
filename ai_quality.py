"""Does the AI actually play well? (A3 quality metric)

A win rate cannot answer this. Every AI change applies to BOTH sides, so
a better policy can leave the win rate flat while playing visibly better
-- and a worse one can look fine. What is measurable is whether the AI
takes lines that were available to it.

Reports, per 100 turns:
  missed lethal   a Benched Pokemon could have Knocked Out the defender
                  this turn and the AI attacked with something that did not
  overkill        it used an attack far larger than the Knock Out needed,
                  when a smaller one would also have killed
  idle            it had an attack available and did not attack at all
"""

import glob
import os
import sys

import simulate_versus as SV


def probe(deck_a, deck_b, games, seed):
    stats = dict(turns=0, missed_lethal=0, overkill=0, idle=0,
                 idle_late=0, late_turns=0, idle_no_energy_in_hand=0,
                 idle_active_cannot_attack=0)
    real_do_attack = SV.do_attack

    def spy(pl, opp, log):
        if pl.active and opp.active:
            stats["turns"] += 1
            hp_left = SV.effective_hp(opp, opp.active) - opp.active.damage
            chosen = SV.best_attack(pl, pl.active, opp=opp)
            chosen_dmg = (SV.attack_damage(pl, opp, pl.active, chosen, record=False)
                          if chosen else 0)
            late = pl.active.entered_turn >= 0 and len(pl.discard) + len(pl.hand) > 12
            if late:
                stats["late_turns"] += 1
            if chosen is None:
                stats["idle"] += 1
                if late:
                    stats["idle_late"] += 1
                # Why could it not attack? Separating "the deck did not
                # give it Energy" from "the AI put the Energy in the wrong
                # place" is the whole point -- 35% idle is meaningless
                # until you know which.
                if not any(k == "Energy" for k, _ in pl.hand):
                    stats["idle_no_energy_in_hand"] += 1
                info = pl.POKEMON[pl.active.name]
                castable = [a for a in info["attacks"]
                            if all(c == "Colorless" or c in pl.energy_types
                                   for c in a["cost"])]
                if not castable:
                    stats["idle_active_cannot_attack"] += 1
            elif chosen_dmg < hp_left:
                # Could anything on the Bench have finished it?
                for b in pl.bench:
                    a = SV.best_attack(pl, b, opp=opp)
                    if a and SV.attack_damage(pl, opp, b, a, record=False) >= hp_left:
                        stats["missed_lethal"] += 1
                        break
            elif chosen_dmg >= hp_left + 100:
                smaller = [a for a in pl.POKEMON[pl.active.name]["attacks"]
                           if a is not chosen
                           and SV.can_pay(SV.effective_cost(pl, pl.active,
                                                            a["cost"], opp),
                                          pl.active.energy)
                           and hp_left <= SV.attack_damage(pl, opp, pl.active,
                                                           a, record=False)
                           < chosen_dmg]
                if smaller:
                    stats["overkill"] += 1
        return real_do_attack(pl, opp, log)

    SV.do_attack = spy
    try:
        mA, _ = SV.load_model(deck_a, "a")
        mB, _ = SV.load_model(deck_b, "b")
        for _ in range(games):
            SV.run_game(mA, mB)
    finally:
        SV.do_attack = real_do_attack
    return stats


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    folder = args[0] if args else "decks"
    games = int(args[1]) if len(args) > 1 else 12
    decks = sorted(glob.glob(os.path.join(folder, "*.txt")))
    total = dict(turns=0, missed_lethal=0, overkill=0, idle=0,
                 idle_late=0, late_turns=0, idle_no_energy_in_hand=0,
                 idle_active_cannot_attack=0)
    pairs = 0
    for i in range(0, min(len(decks) - 1, 16), 2):
        try:
            s = probe(decks[i], decks[i + 1], games, 1)
        except Exception:
            continue
        for k in total:
            total[k] += s[k]
        pairs += 1
    t = max(total["turns"], 1)
    print(f"{pairs} matchups, {total['turns']} attacking turns\n")
    for k in ("missed_lethal", "overkill", "idle"):
        print(f"  {k:26} {total[k]:5}   {100 * total[k] / t:5.1f} per 100 turns")
    print("\n  of the idle turns:")
    i = max(total["idle"], 1)
    for k in ("idle_no_energy_in_hand", "idle_active_cannot_attack", "idle_late"):
        print(f"    {k:26} {total[k]:5}   {100 * total[k] / i:5.1f}% of idle")


if __name__ == "__main__":
    main()
