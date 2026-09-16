# Pilot team — what a different driver is actually worth

`policies.py` gives the engine five pilots instead of one: **greedy**
(historical), **aggro**, **control**, **setup**, **prizewise**. Twelve
knobs, every one read at the decision point rather than baked into a
constant.

## The result, stated the way it should be

**Overall, no pilot beats greedy.** All four alternatives are
statistically tied with it across the field:

| pilot | vs greedy | 95% CI | better on |
|---|---|---|---|
| control | −0.08 | [−1.64, +1.49] | 23/44 |
| setup | −0.38 | [−2.88, +2.12] | 21/44 |
| aggro | −0.72 | [−2.68, +1.24] | 20/44 |
| prizewise | −0.76 | [−2.57, +1.05] | 16/44 |

**And most of the per-deck gains were noise.** Picking each deck's best
pilot and re-measuring that choice on fresh seeds:

| | mean gain |
|---|---|
| selection run (seed 12345) | **+6.64** [+5.34, +7.95] |
| held-out run (seed 777) | **+1.57** [−0.54, +3.68] |

**76% of the apparent gain evaporated, and the held-out interval spans
zero.** Six decks flipped sign outright — `team_rockets_persian_ex` looked
like +15.0 and measured −4.7; `meta_dragapult_blaziken` +12.5 became
−10.7. Reporting the selection numbers as findings would have been
straightforwardly wrong, which is the entire reason the held-out run
exists.

## What survives

Eight decks gain at least 4 points on BOTH independent runs. These are the
credible ones:

| worst case | selection | held out | driver | deck |
|---|---|---|---|---|
| **+10.0** | +10.0 | +11.3 | `setup` | `heracross_sinistcha_tea` |
| **+9.2** | +9.2 | +12.0 | `prizewise` | `salazzle_ex_team_rockets_muk_condition_stack` |
| **+8.3** | +8.3 | +10.0 | `setup` | `team_rockets_koffing_weezing_bench_swarm` |
| **+8.0** | +15.8 | +8.0 | `setup` | `eerie_inferno_ninetales_burn` |
| **+6.7** | +8.3 | +6.7 | `aggro` | `tr_arbok_yveltal_snow_coating` |
| **+6.0** | +6.7 | +6.0 | `setup` | `kyurem_vanilluxe_blizzard` |
| **+4.7** | +10.0 | +4.7 | `setup` | `team_rockets_wobbuffet_orbeetle_damage_launder` |
| **+4.7** | +6.7 | +4.7 | `control` | `dhelmise_veluza_hide_n_sneak` |

Eight of forty-four. Not the twenty-one the first pass suggested.

`setup` accounts for five of the eight, and the shape is consistent: decks
that have to assemble something before they threaten anything. `heracross_sinistcha_tea` and
`kyurem_vanilluxe_blizzard` both want a board built before they start
attacking, and the greedy pilot spends those turns swinging for small
numbers instead.

## Two null tests guard the baseline

A policy layer that silently moved the default would invalidate every
number in this repo, so:

1. `greedy` vs `greedy` reads **+0.00 with a zero-width interval**.
   Identical policies on identical seeds produce identical games.
2. Stronger: eight committed field pairings re-run with the layer in place
   return **byte-identical win counts** (98/98, 101/101, 146/146 ...).
   Test 1 only proves self-consistency; test 2 proves the baseline behind
   every earlier field run did not move.

## One pilot was broken rather than bad

`setup` first measured **−12.58, losing on 43 of 44 decks**. No coherent
strategy is that uniformly bad, and it wasn't one: with
`energy_to_active` off, `attach_energy` fell through to a branch scanning
`pl.bench` only, so setup's Active **never received Energy at all**. It
starved every game. Fixed, it measures −0.38.

The tell was the shape of the loss, not its size. A style that is wrong
for the field loses to greedy on sixty or seventy percent of decks; one
that loses on 43 of 44 is broken.

## Usage

    python3 ai_selfplay.py <deck-folder> <games> <pilot-A> <pilot-B>

Both seats play the same deck, so the only difference is the driver. A
control run of B-vs-B is subtracted to cancel the seat bias (seat A wins
51.6% of mirrors). Always validate a per-deck pick on seeds it was not
chosen on.
