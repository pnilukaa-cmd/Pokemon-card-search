# Scovillain ex / Salazzle ex — Spicy Rage

<!-- field-results -->
> ### Field results — 2026-09-11
> **61.2% mean · 61.0% median · 34 of 43 winning matchups · rank 6 of 44**
>
> Best `meta_ns_zoroark` 95% · worst `water_aggro` 34%.
>
> Full round robin, 200 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box was measured on an older engine and is not comparable** — not with this number and not with each other.
<!-- field-results -->










`Scovillain ex` **SSP 216**, Stage 1 from Capsakid, **260 HP**, Fire.
`F``F` **Spicy Rage 10+ — 70 more damage for each damage counter on this
Pokémon.**

## First, the right printing

**There are two different Scovillain ex and only one of them does this.**

| | | |
| --- | --- | --- |
| `Scovillain ex` **TEF 22** | Grass, 260 HP | Chili Snapper Bind (Burn + retreat lock), Two-Headed Crushing 140 |
| **`Scovillain ex` SSP 216** | **Fire**, 260 HP | `Double Type` (it is Grass *and* Fire in play), **Spicy Rage** |

The list below is SSP 216. If `check_energy_support` flags
*"Two-Headed Crushing needs 2x Grass"*, that is the **other** printing's
attack being pooled in by name — a false positive, not a deck error.

## The trap in "damage it, then heal it"

**Healing removes the counters, and the counters are the damage.**

| | |
| --- | --- |
| Scovillain at 130 damage (13 counters) | Spicy Rage hits for **920** |
| heal 60 | now hits for **500** |
| heal 120 | now hits for **80** |

Healing is a direct, roughly 7:1 downgrade of your own attack. **Swap is
the right instinct; heal is not.** Damage counters stay on a Pokémon when
it moves to the Bench, so switching Scovillain out **preserves the whole
charge** — you park a loaded gun and bring it back when you need it.

The full curve:

| damage taken | counters | Spicy Rage |
| --- | --- | --- |
| 0 | 0 | 10 |
| 30 | 3 | **220** |
| 60 | 6 | **430** |
| 100 | 10 | **710** |
| 130 | 13 | **920** |
| 180 | 18 | **1270** |

Nothing in the format has more than 350 HP, so **anything past 6 counters
is already lethal to everything.** Measured over 20 games: Spicy Rage
fired 17 times, mean **1072**, median **1130**, max **1760**, with **76%
of swings at 200 or more**. The overkill is enormous and it does not
matter — what matters is that it reliably one-shots anything.

## Who damages Scovillain?

**Nothing in Standard can put damage counters on another of your own
Pokémon.** I checked: `Feraligatr`'s Torrential Heart and `Walking Wake`'s
Undulating Slice both damage *themselves*, and there is no card that
damages a chosen friendly Pokémon. So the deck cannot self-charge.

**The opponent charges it, and that is the whole design.** Scovillain ex
has 260 HP. Almost nothing one-shots it, so the standard sequence is:
they hit it, it survives, and it swings back for five to ten times what
they dealt. It is a counter-puncher, not a combo.

`Hero's Cape` TEF 152 (+100 HP → **360**) is the ACE SPEC for exactly this
reason: more HP is more turns absorbing hits, and every hit absorbed is
70 more damage on the swing back. It beat `Master Ball` for the slot.

## Why Salazzle ex is the right partner

`Salazzle ex` POR 101 — Fire, Stage 1 from Salandit, **260 HP**, retreat 1.

- **`F` Nasty Plot: search your deck for up to 2 cards.** A two-card tutor
  on an attack, for one Energy.
- **`F``F` Dire Nails 100** — Burns and Poisons them, **and switches this
  Pokémon with 1 of your Benched Pokémon.**

That second clause is the swap you were after, built into an attack.
Salazzle hits, Burns and Poisons, and **pulls itself out**, promoting
Scovillain — which then eats the opponent's next attack and gets paid for
it. Same type, same stage, same HP, one Energy line.

## The turn sequence, honestly

- **Your turn N:** Salazzle ex uses Dire Nails. 100 damage, they are
  Burned and Poisoned, Salazzle swaps to the Bench, **Scovillain ex is now
  Active** with 0 counters.
- **Their turn:** they attack Scovillain. Say 130. *This is the point of
  the deck.* **Their out here is not attacking it** — dragging up a
  Dunsparce with a gust card instead, or Knocking Out Scovillain outright
  if they can reach 260.
- **Your turn N+1:** Spicy Rage for **920**. Anything dies.
- **Their turn:** Scovillain is at 130/260 and will not survive twice.
- **Your turn N+2:** `Switch` it out — **counters and all** — and bring it
  back later fully charged, or let it trade.

The soft spot is real and worth naming: **a patient opponent simply does
not attack Scovillain.** Burn and Poison from Dire Nails are the answer —
checkup damage they cannot decline.

## Decklist

```
Pokémon: 20
4 Capsakid SSP 12
4 Salandit ASC 34
4 Dunsparce JTG 120
3 Scovillain ex SSP 216
3 Salazzle ex POR 101
2 Dudunsparce TEF 129

Trainer: 28
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
4 Switch MEG 130
3 Cyrano SSP 170
3 Boss's Orders MEG 114
3 Lillie's Determination MEG 119
2 Air Balloon ASC 181
2 Night Stretcher MEG 173
2 Judge POR 76
1 Hero's Cape TEF 152

Energy: 12
12 Basic Fire Energy

Total Cards: 60
```

- **`Cyrano` SSP 170 searches three Pokémon ex at once** — and both of
  this deck's payoffs are ex, so it finds either half of the pair.
  `Poké Pad` is deliberately absent: it cannot fetch a Pokémon with a Rule
  Box, so it would miss both.
- **`Buddy-Buddy Poffin` reaches every Basic in the deck** — Capsakid,
  Salandit and Dunsparce are all exactly 70 HP or under.
- **Four `Switch` plus two `Air Balloon`** is the swap package. It is not
  a luxury: it is how a charged Scovillain survives to swing twice.
- `Dunsparce` → `Dudunsparce`'s Run Away Draw is the consistency engine
  and the reason the mulligan is 19.1% rather than 34.6%.

## Numbers

60 cards, no card over 4, one ACE SPEC, mulligan **19.1%** (12 Basics).

1200-opening curve, Prizes set aside: Capsakid 80.6% by T2, Salandit
77.2%, **Scovillain ex 25.4% by T2 and 61.3% by T6**, Salazzle ex 56.4%
by T6.

Full field, 32 decks, 200 games each — mean **56.3%**, median **57.0%**,
**23/32** winning. Independent seed: **57.3% / 55.5% / 24-32**.

Best: T.R. Wobbuffet 81.5%, Orthworm ex 76.0%, T.R. Spidops 74.0%.

## Where it loses, and it is one word

**Water.** Both Scovillain ex and Salazzle ex are Fire, and both are
**Weak to Water ×2**. Every attacker in the deck folds to the same type.

`water_aggro` is the worst matchup in the field at **21.0%** — less than
half the deck's average — followed by Panic Poison 30.0% and the
Chandelure deck-out at 35.0%.

Note the shape of that Water loss: Weakness means they double their
damage, which *also* charges Scovillain twice as fast — but it dies before
it swings. `Passho Berry` (60 less from Water) would help it survive and
**hurt** it at the same time by removing the counters it wants. There is
no clean tech answer inside a mono-Fire shell; the real fix is a
non-Fire attacker, which is a different deck.
