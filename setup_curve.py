"""Per-turn setup curve: what is actually in play by the END of turn N."""
import sys, collections
import simulate_baseline as B

def curve(path, n=2000, turns=6, watch=None):
    POKEMON, DECKLIST, _, _ = B.build_deck_model(open(path).read())
    watch = watch or list(POKEMON)
    hits = {w: collections.Counter() for w in watch}
    prized = collections.Counter()
    for _ in range(n):
        r = B.run_playthrough(POKEMON, DECKLIST, num_turns=turns)
        for w in watch:
            t = r["online_turn"].get(w)
            if t is not None:
                for k in range(t, turns + 1):
                    hits[w][k] += 1
    print(f"{path.split('/')[-1]}  ({n} trials, Prizes modeled)\n")
    print(f"{'':22}" + "".join(f"  T{k}" .rjust(7) for k in range(1, turns + 1)))
    for w in watch:
        row = "".join(f"{100*hits[w][k]/n:6.1f}%" .rjust(7) for k in range(1, turns + 1))
        print(f"  {w:20}{row}")

if __name__ == "__main__":
    curve(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 2000)
