# Snow Coating: seven shells, one engine bug, and a verdict

`N's Vanilluxe` **ASC 51** — Stage 2, 150 HP.

> `Colorless``Colorless` **Snow Coating** — Double the number of damage
> counters on each of your opponent's Pokémon.

The attack cost is **two Colorless**, so any deck of any type can pay it.
That premise was worth testing and has now been tested. This file is the
record so the same shell does not get built an eighth time.

## First, an engine bug that made the earlier tests unfair

`effect_rare_candy` in `simulate_versus.py` decided whether Rare Candy
could bridge a Basic to a Stage 2 by looking the intervening Stage 1 up in
`pl.POKEMON` — **which is built from the decklist.**

Rare Candy's own text says "skipping the Stage 1." The middle card only
has to exist in the *card pool*. But almost nobody runs it: the normal
construction is four Basics, three Stage 2s, zero Stage 1s. In exactly
that construction the lookup returned `None` and **Rare Candy silently did
nothing, every game, for the whole life of the deck.**

Measured: a deck running 4 Rare Candy and 2 `N's Vanilluxe` put
`N's Vanillite` into play at 82% of Checkups and `N's Vanilluxe` into play
**0 times in 408 games**.

This is the same shape as every other bug this engine has had — the code
existed, the card compiled, a unit test passed, and no path in the field
ever reached it. `test_rare_candy_bridges_a_line_the_deck_does_not_own`
now covers it, and fails without the fix.

**Scope of the damage: none of the existing decks in `decks/`.** All 11
Rare Candy decks in the folder happen to run their Stage 1 as well, so
their numbers stand. The bug only bit decks built the normal way, which is
why it survived this long.

## The attack is good. The card is not.

With the bug fixed, Snow Coating fires and it hits hard:

| | |
| --- | --- |
| uses across 510 games | 56 |
| **mean damage added per use** | **133** |
| max | **640** |

640 damage from one `Colorless``Colorless` attack is real. So the failure
is not the attack's value — it is how rarely all of its preconditions line
up. Instrumented over 510 games of the Dragapult shell:

| | |
| --- | --- |
| Vanilluxe in play (per Checkup) | 18% |
| Vanilluxe **in the Active Spot** (per attack turn) | **5.7%** |
| of those Active turns, **no payable attack** | **49%** |
| opponent's board damage when it was Active | **median 0** |

Four conditions have to hold at once, and two of them fight each other:

1. Assemble a **Stage 2** — three cards, or Rare Candy.
2. Get it **into the Active Spot** — displacing your real attacker.
3. Have **two Energy on it** — invested in a Pokémon that deals 0 damage.
   A freshly Rare-Candied Vanillite has none, which is why half its Active
   turns are spent doing nothing at all.
4. Have a **dirty board** — which requires your real attacker to have been
   Active, not Vanilluxe.

**3 and 4 are in direct tension.** The turns when the board is dirtiest are
precisely the turns when something else was in the Active Spot.

## Seven shells

| shell | type | with | without | delta |
| --- | --- | --- | --- | --- |
| N's Zoroark toolbox | Dark | 17.5% | — | archetype was 36% |
| Palossand ex | Water | 35.4% | 35.3% | **0.0** |
| Kyurem ex / Blizzard | Water | 46.4% | 40.5% | **+5.9** * |
| Froslass | Water | 48.6% | 51.4% | −2.8 |
| Heracross / Sinistcha | Grass | 57.3% | 60.4% | −3.1 |
| **Dusknoir + Uxie** | Psychic | 24.6% | 29.9% | **−5.3** |
| **Dragapult ex** | Psychic/Fire | 50.5% | 55.1% | **−4.6** |
| **max-Vanilluxe combo** | Psychic | 22.2% | 37.7% | **−15.5** |

\* the Kyurem shell is the one gain, and it earns it as a **`Blizzard`**
attacker — a Water deck paying `Water``Colorless``Colorless` for 120 plus
10 to the Bench. That is the line doing ordinary work, not doubling.

Second seed, same field, 200 games each: Dragapult −4.1, combo −16.2.
Both deltas reproduce.

**Re-measured after the ex audit**, which changed damage on a large number
of cards (typed Energy scalers, discard scalers, attack gates): Dragapult
51.6% vs 55.0% (**−3.4**), combo 22.8% vs 39.1% (**−16.3**). The verdict
is unchanged on the corrected engine, and the monotonic relationship —
more Snow Coating, worse deck — survives it.

The last row is the informative one. **The more Snow Coating a deck runs,
the worse it does** — 4 Vanillite / 3 Vanilluxe is a 15-point hole, where
3/2 in a better shell is a 5-point hole. The relationship is monotonic,
which is what a card that costs tempo looks like, not what noise looks
like.

## What was checked and ruled out

The "any colour" premise was the point of this round, and it is genuinely
dead: three of the seven shells were built off-type specifically to test
it. `Blizzard` reports as `IMPOSSIBLE` in a Psychic deck and that is fine
— Snow Coating and `Call for Family` are both Colorless and both work.
Type was never the constraint. The Active Spot is.

Everything that puts counters on the opponent without spending an attack
was searched (`direct_damage_no_attack`, `bench_damage_spread`,
`damage_on_bench_placement`, `damage_on_opponent_evolve`,
`damage_on_opponent_retreat`, `damage_on_opponent_energy_attach`,
`damage_move_opponent_side`, `status_checkup_damage_multiplier`,
`status_checkup_damage_amp`) — 35 producers. The three biggest:

- **`Dusknoir` SFA 20 `Cursed Blast`** — 13 counters (130) for no Energy,
  as an Ability, self-KO. Doubles to 260 *on the same turn*. Built as
  shell C; the tightest version of the combo available, and the worst
  result of the seven.
- **`Team Rocket's Tyranitar` DRI 96 `Sand Stream`** — 2 counters on each
  of the opponent's **Basic** Pokémon at every Checkup, free. Wide, which
  is what a doubler wants — but it requires Tyranitar **in the Active
  Spot**, competing with Vanilluxe for the one slot that matters.
- **`Dragapult ex` TWM 130 `Phantom Dive`** — 200 plus 6 counters spread
  across the Bench, the best spread attack in the format. Built as shell
  B. Still −4.6.

Poison was checked and is the wrong shape: `Mega Dragalge ex`'s
`Pernicious Poison` places **16 counters per Checkup** and
`Team Rocket's Nidoking ex`'s `Tainted Horn` places 8, but poison only
ever touches the Active Pokémon — a doubler that reads "each of your
opponent's Pokémon" gains nothing from a single-target stack that is
already lethal on its own.

## UPDATE — the verdict changed, and here is why

Everything above was measured on an engine in which **15 free-target
spread attacks compiled to nothing at all.** One of them is
`Team Rocket's Arbok`'s **`Spinning Tail`**: `D``D``D` for **30 damage to
each of your opponent's Pokémon** — 180 across a full board, every turn,
repeatable. It placed zero damage in every game any of the eight shells
above ever played.

That is not an incidental card. It is the single best input Snow Coating
has in the format, and the doubler was being judged without it.

Rebuilt around it (see
[tr_arbok_yveltal_snow_coating.md](tr_arbok_yveltal_snow_coating.md)),
with `Yveltal` SFA 35's one-Energy `Corrosive Winds` as the follow-up and
`N's PP Up` charging Vanilluxe on the Bench so it can attack the turn it
switches in:

| shell | with | control | delta |
| --- | --- | --- | --- |
| Arbok, before Yveltal fixed it | 32.4% | 27.0% | **+5.4** |
| *second seed* | 32.3% | 26.8% | **+5.5** |
| **Arbok / Yveltal (the good version)** | **50.8%** | 50.0% | **+0.8** |
| *second seed* | 50.7% | 49.1% | **+1.6** |

Read those four rows together, because they say two different things. In
the weak shell the doubler is worth five points — but that is Snow Coating
compensating for a deck that could not attack on 29% of its turns. Once
the shell actually works, the same A/B collapses to about a point.

Snow Coating fires 99 times per 210 games in that deck for a **mean of
+185 damage, max +560**, Knocking Out a mean of 0.65 Pokémon per use and
as many as **5 at once**. It is a real effect. It is just that the deck
built to enable it is roughly as good without it.

**So: it is no longer a trap, and it is still not a build-around.** Nine
shells, and the honest summary is that Snow Coating now pays for its six
slots instead of costing three to sixteen points. The `win-more` reading
below is still the right one — the difference is that the board it wants
can now actually be built.

## Verdict (as measured before the spread fix)

Snow Coating is a **win-more** attack. It is worth exactly what is already
on the board, and the decks that put a lot on the board are decks that
were already winning and did not need to spend a turn, two Energy and a
Stage 2 slot to convert it.

The one thing that would change this is a card that lets the doubling
happen **without occupying the Active Spot** — an Ability that multiplies
counters, or a way to use an attack from the Bench. Neither exists in this
pool. Until one prints, the line's real home is the Kyurem shell, as a
`Blizzard` attacker.
