# Team Rocket's Koffing/Weezing Bench Swarm

Built from a real deck the user played against — described as "the weezing hit
hard and the bench was filled fast." Confirmed both halves against the actual
card text rather than assumed from the name.

## Centerpieces

1. **Team Rocket's Koffing** (Destined Rivals, Basic, 70 HP) — Ability
   `Smog Signals`: *"If this Pokémon is in the Active Spot and is damaged by
   an attack from your opponent's Pokémon (even if this Pokémon is Knocked
   Out), search your deck for up to 2 Pokémon that have 'Koffing' in their
   name and put them onto your Bench."* Every hit it takes, lethal or not,
   refills the bench with 2 more Koffing-family Basics for free — this is
   "the bench filled fast."

2. **Team Rocket's Weezing** (Destined Rivals, Stage 1, 130 HP) —
   `Explode Together Now` (Darkness + Colorless): *"40 damage for each
   Pokémon in play that has 'Koffing' or 'Weezing' in its name (both yours
   and your opponent's)."* Not restricted to Team Rocket's-prefixed cards —
   counts **any** Koffing or Weezing on the board. Only 4 such cards exist
   in the whole pool (Team Rocket's Koffing/Weezing and plain
   Koffing/Weezing), and running all 4 together maximizes both Smog
   Signals' search pool and this attack's damage — genuinely stronger
   combined than either family alone.

3. **Koffing / Weezing** (plain, Journey Together) — count toward Explode
   Together Now the same as the Team Rocket's versions, and Weezing has its
   own real attack, `Crazy Blast` (Darkness + Colorless, 50+120 if this
   Pokémon used `Pervasive Gas` last turn) — see `combo_patterns.md`
   Pattern 14 for why that bonus has no retreat-escape counter, unlike most
   Special-Condition combos in this project.

## Design notes

- **This deck wants Team Rocket's Koffing to sit Active and eat hits,
  including lethal ones** — backwards from how most decks protect their
  Active Pokémon. Don't retreat it away defensively; let it trade.
- A Koffing that Smog Signals just searched onto the bench still can't
  evolve the same turn it entered play — that rule applies regardless of
  how a Pokémon entered play, not just when played from hand. It needs to
  survive to the start of your next turn before evolving into Weezing.
- Verified with `check_energy_support.py`: mono-Darkness supply (13
  Darkness Energy) covers every attack with no shortfalls; no
  attack-gating Ability text found; 60 cards, no card over 4 copies.
- Mulligan math: 8 effective Basics (Team Rocket's Koffing + plain
  Koffing) → 34.6%, elevated. Smog Signals partially self-corrects
  mid-game once the first Koffing takes a hit, but that's a different
  thing from the actual opening-hand odds, worth knowing as a real
  distinction rather than treating it as a fix for the mulligan rate.

## Pokémon TCG Live Import

```
Pokémon: 16
4 Team Rocket's Koffing DRI 125
4 Team Rocket's Weezing DRI 126
4 Koffing JTG 91
4 Weezing JTG 92

Trainer: 31
4 Ultra Ball MEG 131
4 Buddy-Buddy Poffin MEG 167
4 Boss's Orders MEG 114
4 Lillie's Determination MEG 119
4 Switch MEG 130
4 Air Balloon BLK 79
3 Rescue Board TEF 159
4 Night Stretcher MEG 173

Energy: 13
13 Basic Darkness Energy

Total Cards: 60
```
