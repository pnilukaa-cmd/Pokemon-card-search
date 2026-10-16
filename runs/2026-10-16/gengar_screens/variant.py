"""variant.py BASE OUT 'Card Name SET NUM:+1' ... -- change counts, keep 60, rewrite headers."""
import sys, re
base, out, changes = sys.argv[1], sys.argv[2], sys.argv[3:]
import json
_CARDS = json.load(open('/home/user/Pokemon-card-search/pokemon_standard_cards.json'))
def _supertype(card):
    """Section for 'Name SET NUM' from the card file, never a keyword guess."""
    name, code, num = card.rsplit(' ', 2)
    for c in _CARDS:
        if c['name'] == name and ([code, num] in (c.get('printings') or []) or
                                  (c['set']['ptcgoCode'], str(c['number'])) == (code, num)):
            return {'Pokémon': 'Pokémon', 'Trainer': 'Trainer', 'Energy': 'Energy'}[c['supertype']]
    raise SystemExit(f"not in the pool: {card}")
secs, order, cur = {}, [], None
for ln in open(base, encoding='utf-8').read().splitlines():
    m = re.match(r"^(Pokémon|Trainer|Energy): \d+", ln)
    if m: cur = m.group(1); secs[cur] = []; order.append(cur); continue
    m = re.match(r"^(\d+) (.+)$", ln)
    if m and cur: secs[cur].append([int(m.group(1)), m.group(2)])
for ch in changes:
    card, d = ch.rsplit(':', 1); d = int(d)
    for sec in order:
        hit = next((x for x in secs[sec] if x[1] == card), None)
        if hit: hit[0] += d; break
    else:
        sec = 'Energy' if card.startswith('Basic ') else _supertype(card)
        secs.setdefault(sec, []); secs[sec].append([d, card])
        if sec not in order: order.append(sec)
lines = []
for sec in ('Pokémon', 'Trainer', 'Energy'):
    xs = [x for x in secs.get(sec, []) if x[0] > 0]
    assert all(x[0] <= 4 or x[1].startswith('Basic ') for x in xs), xs
    lines.append(f"{sec}: {sum(x[0] for x in xs)}")
    lines += [f"{n} {c}" for n, c in xs] + [""]
tot = sum(x[0] for s in secs.values() for x in s if x[0] > 0)
assert tot == 60, tot
lines.append("Total Cards: 60")
open(out, 'w', encoding='utf-8').write("\n".join(lines) + "\n")
