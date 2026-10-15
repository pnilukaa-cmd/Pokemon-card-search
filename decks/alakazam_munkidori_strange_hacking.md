# Alakazam / Munkidori Strange Hacking

Built 2026-10-15 from a list submitted with the tag "taking 6 Prizes in
one turn": Froslass, Munkidori, both Alakazam lines and Uxie. The question
was how that turn works and what else supports it.

**This list: 68.51% against the 93-deck field at 1000 games per
opponent** (76 of 93 winning), re-measured 2026-10-15 after the Freezing
Shroud fix below. That is **+29.24 ± 1.41** over the submitted list
(39.27%), better on all 93. The best version that keeps Froslass measured
54.98%.

**Lines:** Abra → Kadabra → Alakazam, both printings:
- **Alakazam MEG 56** (Powerful Hand, and Psychic Draw on Kadabra MEG and
  Alakazam MEG).
- **Alakazam TWM 82** (Strange Hacking).

Plus Munkidori and Uxie.

## How six Prizes in one turn works

The finisher is **Alakazam TWM 82's Strange Hacking** (P): "You may move
any number of damage counters from your opponent's Pokémon to their other
Pokémon in any way you like." It also Confuses their Active.
- Every counter on their board is one pool, and you can rebuild their board
  however you like.
- If the pool is at least the HP of three of their Pokémon ex together,
  one attack Knocks Out all three. Knock Outs are checked once the attack
  is done, so that's 6 Prizes at once (or two Mega ex).

**Filling the pool** (all from the card text):

| Card | Puts on their board |
|---|---|
| **Alakazam MEG**'s **Powerful Hand** (P) | 2 counters on their Active per card in your hand. 8 cards is 160. |
| **Uxie**'s **Painful Memories** (P) | 2 on each of their Pokémon: 100-120 on a full board. |
| **Munkidori**'s **Adrena-Brain** (Ability, needs Darkness Energy) | Moves 3 counters from one of your Pokémon onto one of theirs, every turn, per Munkidori. |
| **Froslass**'s **Freezing Shroud** (Ability, in the submitted list) | 1 counter at every Pokémon Checkup on every Pokémon with an Ability, both sides. |

**A worked line** against three Pokémon ex of 210, 210 and 320 HP. That's
740 HP in total, so 74 counters:
1. **Turn 2:** Painful Memories, 2 on each of five Pokémon: **10**.
2. **Turn 3:** Powerful Hand with 8 cards on the 320 HP Active, which
   survives: **16**. Two Munkidori move 6: **22**.
3. **Turn 4:** Powerful Hand again (8 cards): 16. Munkidori: 6. **22**.
4. **Turn 5:** Munkidori moves 6 before the attack. The pool is now about
   60 plus whatever your attacks left. Strange Hacking puts 320 on the
   Active and 210 on each Benched ex: **6 Prizes**.

**The rules points:**
- **Powerful Hand must place every counter.** If they exceed the Active's
  HP it is Knocked Out and the excess is lost. Bank counters on something
  big.
- **Your own Knock Outs empty the pool.** Every 1-Prize Knock Out on the
  way spends counters you were saving.
- **Battle Cage** (their Stadium) stops counters going onto their Bench
  from your attacks and Abilities. That blocks Uxie, Munkidori onto the
  Bench, and Strange Hacking's moves onto the Bench. Replace it with a
  Stadium of your own.
- **Healing** removes counters from the pool.
- **Hand reset** cards shrink Powerful Hand.
- **Darkness** hits every Psychic Pokémon here for double.

### How often it actually happens

At every one of this list's attacks in 100 field games, I measured the most
Prizes a Strange Hacking could have taken with the counters on the board.
- A 4+ Prize Strange Hacking was available in 11 games, a 5-Prize one in 1,
  and a 6-Prize one in none.
- The submitted list: 6+ in 4 games of 100, measured with the broken
  Freezing Shroud. With it fixed: 4+ in 15, 6+ in 1. A working Froslass
  grows the pool a little, but it costs more on your own board (below).
- The Froslass build with Munkidori as its only Ability Pokémon: 4+ in 14,
  6+ in 2.
- Every variant tested: 0-4 in 100.

Their own Knock Outs and yours keep clearing the board. The pool's peak
was 180 damage in the median game and 350 at the 90th percentile.

**The six-Prize turn is real but rare.** What wins games is Strange
Hacking cashing in 1-3 Prizes most turns, behind Powerful Hand.
- This list used Strange Hacking in 57 of 100 games. The submitted list
  used it in 22.
- Its biggest single turn was 3 Prizes in 15 games.
- Its per-game win rate went from 33 to 69 of 100.

## What the measurements changed

**Froslass costs this list more than it gives**, even with Munkidori
moving its counters. Freezing Shroud was broken when the rounds below were
run. It put one counter on one Pokémon, usually its owner's Munkidori, and
never touched the opponent. So these numbers are from the fixed engine (200
games against the 93 decks, paired).

Counter flow per game, submitted list (60 games):
- Freezing Shroud put **18.3 counters on your board and 16.0 on theirs.**
  The list has six Pokémon with Abilities: 3 Munkidori, Kadabra MEG,
  Alakazam MEG, Shaymin.
- Adrena-Brain moved **4.9**: 1.8 uses a game, out of 1.9 chances with a
  Darkness-Energy Munkidori and counters to move.
- 0.9 of your own Pokémon a game were Knocked Out at checkup, each a Prize
  for them.

Why Munkidori can't absorb it:
- **It moves at most 3 counters a turn**, and only while it has Darkness
  Energy.
- **It never lacks fuel without Froslass.** Their attacks put 100+ on your
  Active every turn. So Froslass's counters on your side don't add Adrena-
  Brain uses; they are damage you keep.

With 7 Darkness Energy instead of 3, Adrena-Brain fired 3.1 times and moved
8.7 a game. Freezing Shroud still put 22.7 on your board against 16.3 on
theirs.

| Change | Paired |
|---|---|
| Submitted list, 3-3 → 2-2 Froslass (+2 Energy) | +8.73 ± 0.69 |
| Submitted list, no Froslass (+6 Energy) | **+21.44 ± 1.33** |
| Submitted list with 7 Darkness, then no Froslass | +16.52 ± 1.33 |
| This list + 2-2 / 3-3 Froslass | −13.00 / −21.21 |
| This list with 5 Darkness + 2-2 Froslass (and a 4th Munkidori) | −13.54 (−14.09) |
| Froslass build where Munkidori is your only Ability Pokémon (TWM Kadabra / Alakazam, 4-4 Froslass) | 46.71%, +7.31 over the submitted list |

**Froslass pays when the opponent has more Pokémon with Abilities than you
do.** That's why the real Froslass / Munkidori archetype keeps Munkidori as
its only one. [Dittobase](https://www.dittobase.com/tcg/decks/meta/pbl/froslass-munkidori)
tracks it at 0.24% of the meta with a 41.6% win rate, close to the 46.71%
above. Built that way it gives up Powerful Hand and Psychic Draw, which
are worth more here.

**Energy.** The submitted list had 9, three of them Darkness for
Munkidori. Every round's top changes traded a situational card for an
Energy:
- Nighttime Mine (+2.77)
- Budew
- Shaymin, for a second Strange Hacking Alakazam
- Special Red Card, Hassel, Air Balloon

**Rare Candy** (+2.16) gets both Alakazam lines down on time.

**Supporting cards tried, all measured worse than an Energy in the
slot** (200 games against the 92 decks, paired against the submitted list):

| Card | Why it looked good | Win rate | Paired |
|---|---|---|---|
| Mimikyu ex (for Nighttime Mine, +1 Energy) | 3 counters on 2 Pokémon | 38.64% | +2.34 (the Energy; −0.43 alone) |
| 2 Rare Candy (for Nighttime Mine) | faster Alakazam | 36.24% | −0.06 (+2.16 later) |
| 1 / 2 Azelf | +10 per counter on their whole board | 35.0% / 33.1% | −1.30 / −3.20 |
| 2-2 Trevenant CRI (for Mine, Budew) | the same payoff; Phantump damages itself for Munkidori | 33.30% | −2.99 |
| 2-2-2 N's Vanilluxe | Snow Coating doubles every counter on their board | 33.16% | −3.14 |
| 2 Swirlix | 2 counters on any Pokémon | 32.55% | −3.75 |
| Azelf + Mesprit | the Lake trio | 30.94% | −5.36 |
| 2-2 Dusclops / 2-1-1 Dusknoir | Cursed Blast drops 5 / 13 counters | 30.6% | −5.7 |
| Bloodmoon Ursaluna ex | the real Froslass list's big hitter | | −2.82 in the final shell |

None of them made a six-Prize turn measurably more often (0-4 in 100
games each).

## What the simulator found

**Two engine fixes** (2026-10-15), each with a regression test that fails
on the previous commit:
- **Freezing Shroud put one counter on one Pokémon**, in practice its
  owner's Munkidori, instead of one on every Pokémon with an Ability on both
  sides. Every "10 damage to each of your opponent's Benched Pokémon" rider
  hit one Benched Pokémon too: Blizzard, Ground Crasher, Blizzard Burst.
  The tuning rounds below ran before this fix, so their Froslass rows are
  from the broken card. The table above re-measures them.
- **Strange Hacking took every counter off the single most-damaged
  Pokémon and put them all on one target.** The AI also priced the attack
  at a flat 20, so the turn this deck is built for never happened.
- The executor now treats their whole board as one pool and spends it on
  the set of Knock Outs worth the most Prizes. Counters come off the
  survivors that matter least.
- A probe board with 720 damage on four Pokémon lost 7 Prizes to one
  Strange Hacking.
- Sableye's Damage Collection (their Bench to their Active) gathers from
  the whole Bench the same way.
- Worth **+1.34 ± 0.45** to the submitted list.

## How it was tuned

200 games against each of the 92 field decks, paired on the same seeds.
**These rounds ran before the Freezing Shroud fix**, so every row with
Froslass in it measured a Froslass that only damaged its owner. The
re-measured Froslass comparisons are under "What the measurements changed".
Each round is paired against the best list of the round before. Lists and
results are in `runs/2026-10-15/strange_hacking_screens/`.

| Round | Change | Win rate | Paired |
|---|---|---|---|
| 0 | Submitted list | 36.30% | |
| 1 | Support cards (table above) | 30.6-38.6% | −5.75 to +2.34 |
| 1 | **−2 Nighttime Mine, +2 Psychic Energy** | **39.07%** | **+2.77 ± 0.68** |
| 2 | Mimikyu ex / +1 Darkness | 38.6% / 40.3% | −0.43 / +1.25 |
| 2 | −1 Uxie / −Special Red Card / −Air Balloon / −Hassel, +Energy | 41.2-41.7% | +2.13 to +2.66 |
| 2 | Shaymin → 2nd Alakazam TWM 82 | 41.77% | +2.70 ± 0.55 |
| 2 | −2 Budew, +2 Energy | 42.79% | +3.73 ± 0.53 |
| 2 | **Froslass 3-3 → 2-2, +2 Energy** | **46.74%** | **+7.68 ± 0.47** |
| 3 | −Air Balloon / Bloodmoon Ursaluna ex / −SRC / −Hassel | 48.2-48.7% | +1.42 to +1.92 |
| 3 | 2nd Alakazam TWM / no Budew | 49.9% / 50.9% | +3.11 / +4.19 |
| 3 | Froslass 1-1 / no Budew + 2nd Alakazam TWM | 53.7% / 54.1% | +6.90 / +7.33 |
| 3 | **No Froslass, +4 Energy** | **60.58%** | **+13.84 ± 0.62** |
| 4 | Froslass-focused build (no Abilities of its own) | 39.07% | −21.51 |
| 4 | −1 Uxie / −Hassel / −SRC / Bloodmoon Ursaluna ex | 60.9-62.3% | +0.33 to +1.68 |
| 4 | 2nd Alakazam TWM / no Budew | 63.7% / 64.6% | +3.15 / +4.00 |
| 4 | **No Budew, Shaymin → 2nd Alakazam TWM, +2 Energy** | **66.81%** | **+6.23 ± 0.51** |
| 5 | Shaymin back / Bloodmoon Ursaluna ex / +Abra +Uxie / 3rd Uxie / 3rd Kadabra MEG | 63.1-65.7% | −3.69 to −1.07 |
| 5 | 4th Abra / 4th Munkidori / 3rd Alakazam MEG | 66.3-67.2% | −0.47 to +0.42 |
| 5 | **2 Rare Candy for 2 Energy (this list)** | **68.97%** | **+2.16 ± 0.47** |
| 1000 games | Submitted / Froslass kept / **this list** | 36.29% / 53.87% / **68.69%** | **+32.40 ± 1.04** |
| 1000 games, fixed engine (93 decks) | Submitted / Froslass kept / **this list** | 39.27% / 54.98% / **68.51%** | **+29.24 ± 1.41** |

**Matchups (1000 games):**
- **Worst:** Mega Zygarde ex / Cinderace 14.0%, Mega Zeraora ex /
  Cinderace 15.7%, Arboliva / Ogerpon 22.6%, Munkidori ex / Pecharunt ex
  24.6% (Darkness).
- **Best:** Mew / Hypno 97.5%, Team Rocket's Wobbuffet 97.1%, Arbok /
  Yveltal 95.3%, Mew baby box 94.9%.
- Against the field's Alakazam / Dudunsparce list: 74.5%.

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Abra | 92.6% | 1.55 |
| Kadabra MEG 55 / TWM 81 | 47.3% / 40.6% | 3.37 / 3.30 |
| Alakazam MEG 56 | 26.2% | 3.90 |
| Alakazam TWM 82 | 21.6% | 3.75 |
| Munkidori | 86.8% | 1.88 |
| Uxie | 84.1% | 1.78 |

First attack by turn 6 in 98.7% of games (average turn 2.38). The baseline
doesn't model Gwynn, Hassel or Lana's Aid, so Alakazam lands sooner in
real games. In the submitted list Alakazam TWM 82 was in play by turn 6 in
3.3%.

**Checks:**
- 60 cards, no card over 4 copies, one ACE SPEC (Legacy Energy).
- Every attack is payable: Psychic, plus Darkness for Munkidori's
  Adrena-Brain.
- 8 Basics, 34.6% mulligan. A 4th Abra or another Uxie measured −0.47 /
  −1.30, so the mulligan rate stays.

## PTCGL import

```
Pokémon: 15
3 Munkidori SFA 72
3 Abra MEG 54
2 Kadabra MEG 55
1 Kadabra TWM 81
2 Alakazam MEG 56
2 Alakazam TWM 82
2 Uxie SSP 78

Trainer: 28
4 Lillie's Determination MEG 169
3 Gwynn PBL 119
2 Hilda WHT 171
1 Boss's Orders MEG 114
1 Lana's Aid TWM 207
1 Hassel TWM 205
4 Buddy-Buddy Poffin MEG 167
4 Poké Pad POR 113
3 Night Stretcher MEG 173
2 Rare Candy MEG 125
1 Pokégear 3.0 BLK 84
1 Air Balloon MEG 166
1 Special Red Card CRI 113

Energy: 17
1 Legacy Energy TWM 167
2 Telepathic Psychic Energy POR 88
3 Basic Darkness Energy
11 Basic Psychic Energy

Total Cards: 60
```

**The best version that keeps Froslass** (54.98% at 1000 games on the
fixed engine):
Froslass 2-2, no Budew, Shaymin swapped for a second Alakazam TWM 82, and
Nighttime Mine for Energy. It is `s3_bh` in the run archive.

Sources for the real Froslass / Munkidori lists:
- [Pokémon.com: Froslass and Munkidori strategy](https://www.pokemon.com/us/strategy/froslass-and-munkidori-strategy-iteration-and-improvement)
- [Dittobase meta page](https://www.dittobase.com/tcg/decks/meta/pbl/froslass-munkidori)
- [PokemonCard.io Froslass & Munkidori](https://pokemoncard.io/deck/froslass-amp-munkidori-bb-amp-wf-133030)
