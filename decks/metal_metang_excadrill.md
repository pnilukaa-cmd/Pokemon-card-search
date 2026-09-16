# metal_metang_excadrill — Metal Maker / Mega Excadrill ex

<!-- field-results -->
> ### Field results — 2026-09-16
> **55.5% mean · 55.2% median · 27 of 44 winning matchups · rank 14 of 45**
>
> Best `meta_ns_zoroark` 90% · worst `scovillain_salazzle_spicy_rage` 28%.
>
> Full round robin, 200 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates the Stadium-passive fix and is not comparable**: 20 Stadiums had inert passives, Stadiums a deck wanted but did not name by text were never played at all, and blind discard costs pitched arbitrary cards instead of ranking them.
<!-- field-results -->


**Not my list.** Submitted by the user for review. Reproduced card-for-card
with three lines corrected (below); nothing else was changed, because
nothing else I tried made it better.

> ### Measured — 2026-09-15
> **56.1% mean · 54.5% median · 28 of 44 winning matchups · would rank 15 of 45**
>
> Best `meta_ns_zoroark` 90% · worst `scovillain_salazzle_spicy_rage` 28%.
>
> 200 games against each of the 44 decks in `FIELD_RESULTS.md`, own fixed
> seed per pairing. Measured as a challenger, so it is not itself in that
> field and the other decks' numbers there do not include it.

## Three lines did not resolve

| as submitted | problem | corrected to |
|---|---|---|
| `1 Boss's Orders RCL 189` | Rebel Clash is not Standard-legal | `1 Boss's Orders MEG 114` |
| `1 Judge DRI 222` | DRI is legal, but 222 is not a Judge | `1 Judge POR 76` |
| `16 Basic {M} Energy SUM 163` | Sun & Moon rotated out; Basic Energy carries no set code here | `16 Basic Metal Energy` |

The section headers also counted **lines, not cards** — "Pokémon: 8" is 8
lines holding 18 cards, "Trainer: 14" is 14 lines holding 26, "Energy: 1"
is one line holding 16. The 60 total is right, so it is a cosmetic export
bug, but a judge reading the headers would flag it.

## Decklist

```
Pokémon: 18
3 Drilbur PBL 46
1 Metagross CRI 61
1 Fezandipiti ex ASC 288
2 Mega Excadrill ex PBL 103
1 Mega Skarmory ex POR 106
2 Genesect ex BLK 169
4 Metang TEF 114
4 Beldum CRI 59

Trainer: 26
1 Kieran TWM 206
1 Boss's Orders MEG 114
2 Team Rocket's Watchtower DRI 180
1 Community Center TWM 146
1 Secret Box TWM 163
1 Air Balloon MEG 166
4 Buddy-Buddy Poffin MEG 167
1 Energy Recycler POR 108
3 Jumbo Ice Cream CRI 109
1 Judge POR 76
1 Special Red Card CRI 113
3 Brock's Scouting JTG 179
4 Team Rocket's Petrel DRI 226
2 Team Rocket's Transceiver ASC 263

Energy: 16
16 Basic Metal Energy

Total Cards: 60
```

## What it does

`Metang`'s **Metal Maker** is the engine — look at the top 4 and attach
every Basic Metal you find, anywhere you like. That is what justifies 16
Energy: the Ability is a four-card look, so density is the whole point.
It feeds `Mega Excadrill ex`'s **Maximum Drilling**, 200 base and **330**
with two Energy beyond the cost. `Genesect ex`'s **Metallic Signal**
fetches two Evolution Metal Pokémon, which is how Metang is found.

The Team Rocket package looks like a mistake and is not one. There are no
Team Rocket's Pokémon here and none are needed: `Transceiver` finds
`Petrel`, `Petrel` finds any Trainer, and `Team Rocket's Watchtower` turns
off **Colorless** Abilities — a type this deck does not play, so it is
pure anti-meta aimed at the Dunsparce / Fan Rotom engines.

## Four attempts to improve it, all measured, none kept

Each variant was run against the same 44 opponents on the same seeds and
compared pairwise.

| variant | mean | vs baseline | better on |
|---|---|---|---|
| **as submitted** | **56.1%** | — | — |
| +4 `Lillie's Determination`, cut `Community Center` + `Metagross` | 43.6% | **−12.55** [−15.29, −9.80] | 2/44 |
| +3 `Lillie's Determination`, keep `Community Center` | 49.6% | **−6.56** [−8.55, −4.57] | 6/44 |
| 2nd `Community Center` for a `Jumbo Ice Cream` | 54.0% | **−2.09** [−3.47, −0.71] | 14/44 |
| 3rd `Mega Excadrill ex` for an Energy | 56.0% | −0.16 [−1.69, +1.37] | 24/44 |

**Three things I was confident about were wrong.**

*"Six of eight Pokémon are Fire-weak, so Fire is a structural problem."*
Against the six field decks running 2+ Fire Pokémon it averages 51.4%,
against everyone else 56.9% — a gap of 5.4 points, with `meta_ns_zoroark`
(2 Fire cards) at 90% and `salazzle_ex_team_rockets_muk` (3 Fire cards) at
60.5%. Real, but not what holds the deck back.

*"Ten Supporters and one Judge is not a draw engine."* True as arithmetic
and wrong as a diagnosis. This deck's consistency is **search**, not draw
— Petrel, Brock's Scouting, Metallic Signal, Buddy-Buddy Poffin,
Transceiver, five separate tutors. When you know which card you need,
search beats draw, and every `Lillie's Determination` added competes for
the one Supporter slot per turn that Petrel needs. `Lillie's` also
**shuffles your hand away**, which costs a deck that is holding Energy for
Metal Maker and assembling two evolution lines.

*"`Community Center` heals 10, that is marginal."* It heals 10 from
**each** of your Pokémon, every turn you play a Supporter, and it is worth
roughly 6 points on its own — the difference between the two Lillie's
variants. It is the answer to precisely the spread decks this list
otherwise farms: cutting it took `meta_festival_lead` from 79% to 44.5%
and `team_rockets_spidops_swarm` from 71% to 43.5%. A **second** copy is
also worse than one, which is what a Stadium slot should do.

The `Metagross` at one copy still looks like the weakest card — Metang is
played for its Ability, not to evolve — but cutting it was part of the
worst variant, so that suspicion is untested on its own.

**Conclusion: the list is at a local optimum for everything tried.** Four
proposed changes, four failures. The only defensible edits are the three
resolution fixes above.

## And the pilot excuse does not hold either

I closed the first review by saying 56.1% was "a floor, not a ceiling",
on the grounds that this deck's search-toolbox structure is the kind a
human pilots better than a greedy AI. That was a hand-wave offered
immediately after being wrong three times about this same deck, so it got
measured too — the same list under all five pilots in `PILOT_RESULTS.md`:

| pilot | mean | vs greedy |
|---|---|---|
| aggro | 56.9% | **+0.77** |
| **greedy** | **56.1%** | — |
| prizewise | 55.5% | −0.64 |
| setup | 53.7% | −2.39 |
| control | 51.0% | −5.10 |

The best alternative driver is worth **+0.77 points**, which is inside
noise, and three of the four are worse. This deck is not being held back
by its pilot.

**Re-tested 2026-09-16 on the fixed engine, because one measurement said
otherwise.** The mirror test in `PILOT_RESULTS.md` — this deck driven by
`prizewise` against a copy of itself driven by greedy — read **+7.5 on the
selection seeds and +12.0 held out**, which would have reversed the
paragraph above. It does not survive contact with the field. Replaying all
44 pairings with the same CRN seeds and only this deck's pilot changed:

| | mean vs field |
|---|---|
| greedy | 55.5% |
| prizewise | 55.3% |

**−0.20, 95% CI [−1.69, +1.29].** The mirror gain does not convert. That
is not specific to this deck: across all eight decks that passed held-out
validation, mean mirror gain was +9.38 and mean field gain +2.66, with a
correlation of +0.27. This deck is one of the five where the field delta
is flatly zero.

So the original finding stands, now on better evidence than it had: **this
deck is not being held back by its pilot.**
