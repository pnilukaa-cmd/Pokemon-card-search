"""mkvar.py base.txt out.txt "+1 Rare Candy MEG 125" "-1 Psyduck ASC 39" ..."""
import sys, re
base, out, *edits = sys.argv[1:]
lines = open(base).read().splitlines()
def key(l):
    m = re.match(r"(\d+) (.+)$", l.strip()); return (int(m.group(1)), m.group(2)) if m else None
for e in edits:
    sign, n, card = e[0], int(e[1:].split()[0]), e[1:].split(" ", 1)[1]
    for i, l in enumerate(lines):
        k = key(l)
        if k and k[1] == card:
            c = k[0] + (n if sign == "+" else -n)
            assert c >= 0, e
            lines[i] = f"{c} {card}" if c else None
            lines = [x for x in lines if x is not None]
            break
    else:
        assert sign == "+", f"missing {card}"
        # insert before the Energy header
        j = next(i for i, l in enumerate(lines) if l.startswith("Energy"))
        lines.insert(j - 1, f"{n} {card}")
tot = sum(key(l)[0] for l in lines if key(l))
assert tot == 60, tot
open(out, "w").write("\n".join(lines) + "\n")
