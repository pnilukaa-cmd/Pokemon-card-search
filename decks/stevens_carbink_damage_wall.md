# Steven's Carbink Damage Wall

The mirror image of the Hop's Snorlax stacked-buff deck: instead of
stacking +30 damage-dealt bonuses onto your own attacks, this stacks a
flat -30 damage-*taken* reduction across your whole team. Found while
researching whether a "Steven's"-named family existed with a similar
shape to Hop's — it does, structurally, but with one real difference
worth knowing before building around it (see below).

## Centerpieces

1. **Steven's Carbink** (DRI 86, 80 HP Psychic, standalone Basic) —
   Ability `Stone Palace`: *"As long as this Pokémon is on your Bench,
   all of your Steven's Pokémon take 30 less damage from attacks from
   your opponent's Pokémon. Doesn't stack."* Same passive, works-from-
   anywhere-in-play shape as Hop's Snorlax's Extra Helpings, with one
   critical difference: **the text says "on your Bench," not just "in
   play."** Lead with Carbink as your Active and the effect turns off
   entirely — this deck needs it Benched, on purpose, from turn 1.
2. **Steven's Beldum -> Metang -> Metagross ex** (DRI 143/144, ASC 289,
   340 HP) — the payoff attacker. `Metal Stomp` (Metal+C+C): flat 200,
   no drawback. Ability `X-Boot`: once per turn, search your deck for a
   Basic Metal Energy, a Basic Psychic Energy, or one of each, and
   attach them to your Metal and Psychic Pokémon in any combination —
   this is what makes running two real Energy types workable (see
   below).
3. **Steven's Baltoy -> Claydol** (DRI 83/84) — Baltoy's `Summoning
   Sign` is **free** (no Energy cost) and searches up to 2 Basic
   Steven's Pokémon onto the Bench, same shape as Hop's Bag but built
   into a Pokémon's own attack instead of a Trainer card. Claydol's
   `Clay Blast` (Psychic+Psychic+Colorless) hits for 220 but discards
   all its own Energy — a real one-shot, not a repeatable attacker.
4. **Steven's Skarmory** (DRI 142, 120 HP Metal, standalone Basic) —
   `Sonic Double` (Metal+Metal+Colorless): 50 damage to 2 different
   opponent Pokémon at once, Bench included.

## The honest structural difference from the Hop's deck

Hop's Snorlax's damage bonus stacks with **three independent sources**
(Snorlax, Postwick, Hop's Choice Band) for up to +90 total. Steven's
Carbink is the **only** source of its effect in this family — no
Steven's-named Stadium or Tool exists in the current pool (checked
directly, not assumed) — and it explicitly doesn't stack with itself, so
running more Carbink copies buys redundancy (in case one gets Prized or
KO'd), not a bigger number. A flat, permanent -30 to every hit is still
real and strong on its own — it turns a lot of the format's common
70-100 damage pokes into 40-70 — but it's a single fixed number, not a
stackable combo the way Hop's is.

## Design notes

- **Real Metal/Psychic Energy split, not optional.** Unlike Hop's
  (nearly pure Colorless cost, mono-type-friendly), both types are
  load-bearing here: Metagross ex/Skarmory/Beldum/Metang need Metal,
  Claydol/Carbink/Baltoy need Psychic. 7/7 Basic Energy split, and
  Metagross ex's own Ability (X-Boot) is the built-in answer to keeping
  both sides fed once it's down.
- **Precious Trolley** (ACE SPEC) is an excellent fit — every one of the
  4 lines starts as a Basic (Beldum, Skarmory, Baltoy, Carbink), so one
  card can seed a real chunk of the board.
- **Boss's Orders is safe here** — nothing about this deck's plan cares
  what the opponent's board looks like, unlike the Arbok/Muk deck's
  anti-synergy with it.
- Verified with `check_energy_support.py`: 60 cards, no card over 4
  copies, one ACE SPEC, no shortfalls across either Energy type.
- Mulligan math: 12 effective Basics (Beldum, Skarmory, Baltoy, Carbink)
  -> 19.1%.

## Baseline simulation (1000 trials, `simulate_baseline.py`)

| Pokémon | In play by turn 6 | Avg turn |
|---|---|---|
| Steven's Beldum | 96.9% | 1.49 |
| Steven's Metang | 67.4% | 3.09 |
| Steven's Metagross ex | 36.4% | 3.63 |
| Steven's Skarmory | 76.5% | 1.92 |
| Steven's Baltoy | 90.8% | 1.61 |
| Steven's Claydol | 48.6% | 3.26 |
| Steven's Carbink | 72.4% | 1.78 |

First attack landed by turn 6 in 80.4% of trials (avg turn 3.04) — slower
than most decks this session, consistent with a defensive, dual-type
build rather than an aggressive one. Average final hand size: 4.18.
Carbink itself — the card the whole plan depends on — is online by turn
6 in 72.4% of games, a solid rate for the deck's defining piece. As
always: no retreating or opponent modeled, so this can't show whether
Stone Palace's -30 actually saves a game, only that Carbink shows up.

## Pokémon TCG Live Import

```
Pokémon: 19
4 Steven's Beldum DRI 143
3 Steven's Metang DRI 144
2 Steven's Metagross ex ASC 289
2 Steven's Skarmory DRI 142
3 Steven's Baltoy DRI 83
2 Steven's Claydol DRI 84
3 Steven's Carbink DRI 86

Trainer: 27
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
1 Precious Trolley SSP 185
4 Lillie's Determination MEG 119
2 Boss's Orders MEG 114
2 Night Stretcher MEG 173
2 Rare Candy MEG 125
2 Air Balloon BLK 79
2 Rescue Board TEF 159
2 Switch MEG 130
2 Poké Pad ASC 198

Energy: 14
7 Basic Metal Energy
7 Basic Psychic Energy

Total Cards: 60
```
