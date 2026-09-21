# Team Rocket's Arbok / Yveltal / N's Vanilluxe — the Snow Coating deck

<!-- field-results -->
> ### Field results — 2026-09-21
> **42.6% mean · 39.2% median · 12 of 44 winning matchups · rank 37 of 45**
>
> Best `selective_bloom_cradily` 100% · worst `lurantis_heal_punish` 14%.
>
> Full round robin, 200 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates the Fossil-setup fix**: a Fossil is an Item and cannot be your opening Pokemon, so it no longer counts as a Basic for the opening hand.
<!-- field-results -->














**50.8% mean · 50.5% median · 18 of 35 winning matchups**, and 50.7% on an
independent seed.

This is the ninth shell built around `Snow Coating`, and the first in which
the card does not cost its deck points. The reason is not cleverness — it
is that **the attack that feeds it did not previously exist in the
simulator.**

## What changed

`Team Rocket's Arbok` **DRI 113** — Stage 1, 130 HP, Darkness.

> `Darkness``Darkness``Darkness` **Spinning Tail** — This attack does **30
> damage to each of your opponent's Pokémon.** (Don't apply Weakness and
> Resistance for Benched Pokémon.)

That is 180 damage spread across a full opposing board, every turn,
repeatable. It is exactly the input `Snow Coating` consumes — and it was
one of **15 free-target spread attacks in the pool that compiled to
nothing at all**. Spinning Tail placed zero damage in every game this
project ever simulated, so every previous Snow Coating shell was tested
without the one card that makes the doubler work.

`Yveltal` **SFA 35** is the second half:

> `Darkness` **Corrosive Winds** — Put 2 damage counters on each of your
> opponent's Pokémon **that has any damage counters on it.**

Twenty more damage to everything already hit, for **one** Energy. It only
works *after* Spinning Tail has touched the board, which is precisely the
sequence this deck wants.

Then `N's Vanilluxe` **ASC 51** doubles the lot: `Colorless``Colorless`,
so mono-Darkness pays for it.

## The turn sequence

- **Your turn N**: Spinning Tail. 30 on all six.
- **N+1**: Corrosive Winds for one Energy. 50 on all six.
- **N+2**: Spinning Tail. 80 on all six.
- **N+3**: switch in Vanilluxe, Snow Coating. **160 on all six** — which
  Knocks Out every Basic and most Stage 1s on their board at once.

Measured over 210 games: Snow Coating fired 99 times for a **mean of +185
damage** (max **+560**), and Knocked Out a mean of **0.65 Pokémon per use**,
up to **5 at once**.

`N's PP Up` **ASC 195** is what makes the switch turn possible: it attaches
a Basic Energy from the discard to a **Benched N's Pokémon**, and
`N's Vanilluxe` is one. Snow Coating's oldest problem is that a freshly
Rare-Candied Vanilluxe arrives with no Energy on it; PP Up charges it on
the Bench so it can attack the turn it comes forward.

## Honest accounting

**Snow Coating is worth about a point, not five.** In an earlier, weaker
version of this shell it measured **+5.4 / +5.5** — but that was the
doubler papering over a deck that could not attack on 29% of its turns.
Once `Yveltal` fixed the shell (34.2% → 50.8%), the same A/B against a
matched control gives:

| seed | with Vanilluxe | control | delta |
| --- | --- | --- | --- |
| van3 | 50.8% (18/35) | 50.0% (19/35) | **+0.8** |
| van5 | 50.7% (18/35) | 49.1% (16/35) | **+1.6** |

So the verdict flips from "costs its slots" to "roughly pays for itself,"
not to "build around it." The control — the same deck with four more
Arbok/Yveltal pieces instead of the Vanilluxe line — is the same deck
within noise. **The spread engine is what is good here.** The doubler is a
reasonable six slots on top of it, and that is a genuine change from the
eight shells before this one, where it was never anything but a cost.

At 50.8% this would sit around 22nd of the 35 decks in
[FIELD_RESULTS.md](FIELD_RESULTS.md). A real deck, not a strong one.

## Decklist

```
Pokémon: 16
4 Team Rocket's Ekans DRI 112
3 Team Rocket's Arbok DRI 113
4 N's Vanillite ASC 49
2 N's Vanilluxe ASC 51
3 Yveltal SFA 35

Trainer: 28
4 Rare Candy MEG 125
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
3 N's PP Up ASC 195
3 Boss's Orders MEG 114
3 Switch MEG 130
2 Lillie's Determination MEG 119
2 Night Stretcher MEG 173
1 Poké Pad ASC 198
1 Air Balloon ASC 181
1 Hero's Cape TEF 152

Energy: 16
4 Team Rocket's Energy DRI 182
12 Basic Darkness Energy

Total Cards: 60
```

- **`Team Rocket's Energy` DRI 182 provides TWO Energy** (any combination
  of Psychic and Darkness) on a Team Rocket's Pokémon. That is what makes
  a three-Energy attack on a Stage 1 castable at all — two cards fully pay
  Spinning Tail. It cannot attach to Vanilluxe, which is why the twelve
  Basic Darkness are still there.
- **Mono-Darkness pays for everything.** Snow Coating is `Colorless`
  `Colorless` and Corrosive Winds is a single `Darkness`. `Blizzard` and
  `Icy Snow` report as uncastable and that is intended — this deck runs the
  Vanilluxe line purely for the doubler.
- **`Rare Candy` bridges `N's Vanillite` straight to `N's Vanilluxe`**;
  the deck runs no `N's Vanillish` at all.
- 60 cards, 11 Basics, mulligan **22.2%**, legal.

## Development curve

1000 openings: Team Rocket's Ekans 95.9% by turn 6, N's Vanillite 94.2%,
Yveltal 76.7% (avg turn 1.9), Team Rocket's Arbok 66.7% (avg turn 3.2),
**N's Vanilluxe 18.9% (avg turn 3.9)**. First attack lands by turn 6 in
91.8% of games.

That 18.9% is the honest ceiling on how often the doubler shows up, and it
matches what the match simulator sees. It is also why the card is worth a
point rather than five: most games it never arrives.
