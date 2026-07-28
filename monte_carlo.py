"""Monte Carlo runner: simulate many matches of simulate_match.py and report
probabilities/averages over the first 3 rounds.

Usage: python3 monte_carlo.py [num_trials]
"""

import sys
from collections import Counter

from simulate_match import run_match, NUM_ROUNDS


def pct(count, total):
    return f"{100 * count / total:.1f}%"


def round_distribution(rounds_list, total):
    counter = Counter(rounds_list)
    never = counter.get(None, 0)
    parts = [f"R{r}={pct(counter.get(r, 0), total)}" for r in range(1, NUM_ROUNDS + 1)]
    parts.append(f"never={pct(never, total)}")
    return ", ".join(parts)


def by_round_or_earlier(rounds_list, total, upto_round):
    hits = sum(1 for r in rounds_list if r is not None and r <= upto_round)
    return pct(hits, total)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    print(f"Running {n} simulated matches...\n")

    results = [run_match(verbose=False) for _ in range(n)]

    jellicent = [r["jellicent_ex_round"] for r in results]
    espeon = [r["espeon_ex_round"] for r in results]
    either = [r["either_ex_round"] for r in results]
    dragapult = [r["dragapult_ex_round"] for r in results]
    us_first_atk = [r["us_first_attack_round"] for r in results]
    opp_first_atk = [r["opp_first_attack_round"] for r in results]

    print("=== Board development timing (first round the card is in play) ===")
    print(f"Jellicent ex online:       {round_distribution(jellicent, n)}")
    print(f"Espeon ex online:          {round_distribution(espeon, n)}")
    print(f"Either ex online:          {round_distribution(either, n)}")
    print(f"Opponent's Dragapult ex:   {round_distribution(dragapult, n)}")
    print()

    print("=== Cumulative: online by round N or earlier ===")
    for label, data in [("Jellicent ex", jellicent), ("Espeon ex", espeon),
                        ("Either ex", either), ("Dragapult ex (opp)", dragapult)]:
        line = ", ".join(f"by R{r}={by_round_or_earlier(data, n, r)}"
                         for r in range(1, NUM_ROUNDS + 1))
        print(f"{label:22s} {line}")
    print()

    print("=== Attacking ===")
    print(f"US first attack round:       {round_distribution(us_first_atk, n)}")
    print(f"OPPONENT first attack round: {round_distribution(opp_first_atk, n)}")
    print()

    us_dmg = [r["us_total_damage"] for r in results]
    opp_dmg = [r["opp_total_damage"] for r in results]
    print("=== Damage dealt over rounds 1-3 ===")
    print(f"US average total damage:       {sum(us_dmg)/n:.1f}")
    print(f"OPPONENT average total damage: {sum(opp_dmg)/n:.1f}")
    print()

    us_hand = [r["us_final_hand"] for r in results]
    opp_hand = [r["opp_final_hand"] for r in results]
    print("=== Hand size after round 3 ===")
    print(f"US average final hand:       {sum(us_hand)/n:.2f}")
    print(f"OPPONENT average final hand: {sum(opp_hand)/n:.2f}")


if __name__ == "__main__":
    main()
