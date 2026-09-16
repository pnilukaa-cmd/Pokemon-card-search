# Pilot team — what a different driver is actually worth

`policies.py` gives the engine five pilots instead of one: **greedy**
(historical), **aggro**, **control**, **setup**, **prizewise**. Twelve
knobs, every one read at the decision point rather than baked into a
constant.

Re-measured 2026-09-16 on the post-Stadium-fix engine and the 45-deck
field. **This supersedes the 2026-09-15 pilot run**: that run predates
three engine fixes (20 inert Stadium passives, Stadiums a deck wanted
but did not name never being played, and blind discard costs pitching
unranked cards) and its numbers are not comparable with these.

## The result, stated the way it should be

**Overall, no pilot beats greedy.** All four alternatives are
statistically tied with it across the field:

| pilot | vs greedy | 95% CI | better on |
|---|---|---|---|
| aggro | -0.36 | [-1.73, +1.02] | 22/45 |
| prizewise | -0.66 | [-2.06, +0.75] | 16/45 |
| control | -0.71 | [-2.36, +0.94] | 21/45 |
| setup | -1.58 | [-3.60, +0.44] | 17/45 |

Every interval spans zero. This is the second independent field to say
so — the first said it about a 44-deck field on a materially different
engine, which makes it a property of the pilots rather than of one
measurement.

**And most of the per-deck gains are noise.** Picking each deck's best
pilot and re-measuring that same choice on seeds it was not chosen on:

| | mean gain | 95% CI |
|---|---|---|
| selection run (seed 12345) | **+3.88** | [+2.53, +5.22] |
| held-out run (seed 777) | **+0.84** | [-0.68, +2.37] |

**78% of the apparent gain evaporates.** max-of-4 is biased
upward by construction: pick the best of four noisy draws per deck and
you have measured the noise as much as the pilot. 19 decks flipped sign outright.

## What survives

8 decks gain at least 4 points on BOTH independent
runs. These are the credible ones:

| worst case | selection | held out | driver | deck |
|---|---|---|---|---|
| **+12.0** | +12.0 | +13.5 | `setup` | `heracross_sinistcha_tea` |
| **+9.0** | +9.0 | +10.5 | `prizewise` | `salazzle_ex_team_rockets_muk_condition_stack` |
| **+8.0** | +15.5 | +8.0 | `setup` | `eerie_inferno_ninetales_burn` |
| **+8.0** | +8.0 | +12.0 | `setup` | `team_rockets_koffing_weezing_bench_swarm` |
| **+7.5** | +7.5 | +12.0 | `prizewise` | `metal_metang_excadrill` |
| **+7.0** | +8.5 | +7.0 | `setup` | `kyurem_vanilluxe_blizzard` |
| **+7.0** | +7.0 | +8.0 | `control` | `meta_slowking` |
| **+4.0** | +10.0 | +4.0 | `control` | `stevens_carbink_damage_wall` |

8 of 45. Not the 34 the selection run suggested.

Which pilot survives, and how often: `setup` 4, `prizewise` 2, `control` 2.

## The strongest evidence here: what reproduced across engines

The 2026-09-15 run also found eight survivors. **Five are the same
deck with the same driver**, which means they held up across two seed
sets AND across an engine change that moved the field by a mean of
5.6 points per pairing. That is a far higher bar than either run
clears on its own:

| deck | driver | 09-15 worst case | 09-16 worst case |
|---|---|---|---|
| `heracross_sinistcha_tea` | `setup` | +10.0 | +12.0 |
| `salazzle_ex_team_rockets_muk_condition_stack` | `prizewise` | +9.2 | +9.0 |
| `team_rockets_koffing_weezing_bench_swarm` | `setup` | +8.3 | +8.0 |
| `eerie_inferno_ninetales_burn` | `setup` | +8.0 | +8.0 |
| `kyurem_vanilluxe_blizzard` | `setup` | +6.0 | +7.0 |

Three from the old list did not reproduce —
`tr_arbok_yveltal_snow_coating` (aggro),
`team_rockets_wobbuffet_orbeetle_damage_launder` (setup) and
`dhelmise_veluza_hide_n_sneak` (control). Three are new:
`meta_slowking` and `stevens_carbink_damage_wall` under `control`, and
`metal_metang_excadrill` under `prizewise` — that last one was not in
the old field at all.

`setup` is the interesting case. It is the WORST pilot overall at
-1.58, and it owns four of the eight survivors. That is not a
contradiction, it is the finding: `setup` is not a better driver, it
is a driver that is right for a specific kind of deck — one that has
to assemble something before it threatens anything — and badly wrong
for everything else. Its per-deck spread is the widest of the four.

## The control is the self-test

greedy-vs-greedy, both seats, 90 deck-runs of 200 games:
**49.94%** to seat A, 95% CI [49.26, 50.62].

Two things follow. First, `greedy` reproduces the engine's historical
behaviour exactly, so a mirror that read anything other than an even
split plus seat bias would mean the policy plumbing had changed
behaviour on its own — it has not. Second, **the seat bias of 51.6%
this repo has been quoting is not reproduced on the current engine.**
The interval above contains 50.00, so on this evidence there is no
detectable first-player advantage. That does not change the method:
the control run is subtracted regardless, because it also cancels
most of the shared variance, which is the only reason a 1-point
effect is visible at this sample size.

## Usage

    python3 ai_selfplay.py <deck-folder> <games> <pilot-A> <pilot-B>

Both seats play the same deck, so the only difference is the driver. A
control run of B-vs-B is subtracted. Always validate a per-deck pick on
seeds it was not chosen on — the two tables above are the whole reason
that sentence is here.

## Per-deck detail

Every deck, its best alternative pilot on the selection seeds, and what
that same choice measured on the held-out seeds. Read the third column,
not the second.

| deck | driver | selection | held out |
|---|---|---|---|
| `heracross_sinistcha_tea` | `setup` | +12.0 | +13.5 |
| `salazzle_ex_team_rockets_muk_condition_stack` | `prizewise` | +9.0 | +10.5 |
| `eerie_inferno_ninetales_burn` | `setup` | +15.5 | +8.0 |
| `team_rockets_koffing_weezing_bench_swarm` | `setup` | +8.0 | +12.0 |
| `metal_metang_excadrill` | `prizewise` | +7.5 | +12.0 |
| `kyurem_vanilluxe_blizzard` | `setup` | +8.5 | +7.0 |
| `meta_slowking` | `control` | +7.0 | +8.0 |
| `stevens_carbink_damage_wall` | `control` | +10.0 | +4.0 |
| `dhelmise_veluza_hide_n_sneak` | `aggro` | +3.5 | +7.5 |
| `arbok_muk_trolley_darkbell` | `setup` | +5.5 | +1.5 |
| `mega_chandelure_ex_retreat_tax` | `aggro` | +1.5 | +6.0 |
| `selective_bloom_cradily` | `control` | +2.5 | +1.0 |
| `darkness_mill_hand_lock` | `aggro` | +7.0 | +0.0 |
| `feraligatr_munkidori_damage_transfer` | `prizewise` | +0.0 | +0.0 |
| `meta_festival_lead` | `prizewise` | +9.5 | +0.0 |
| `orthworm_ex_metal_retaliation` | `prizewise` | +0.0 | +2.5 |
| `team_rockets_wobbuffet_orbeetle_damage_launder` | `setup` | +8.5 | +0.0 |
| `arbok_muk_laser_darkbell` | `setup` | +2.5 | -0.5 |
| `hops_snorlax_stacked_buff` | `control` | +1.5 | -0.5 |
| `mega_lopunny_dusknoir_snipe_finisher` | `aggro` | -0.5 | +2.5 |
| `meta_raging_bolt` | `control` | -1.0 | -0.5 |
| `static_venom_drapion` | `setup` | +2.5 | -1.0 |
| `tr_crobat_absol_bench_snipe` | `prizewise` | +3.0 | -1.0 |
| `water_aggro` | `prizewise` | -1.0 | +0.5 |
| `krookodile_ex_relicanth_hand_disruption` | `aggro` | +1.5 | -1.5 |
| `scovillain_salazzle_spicy_rage` | `control` | +13.5 | -1.5 |
| `veluza_sinistcha_ex_tea_service` | `aggro` | +5.0 | -1.5 |
| `meta_ns_zoroark` | `control` | +3.5 | -2.0 |
| `toxic_slumber_vileplume_ex` | `setup` | +6.5 | -2.0 |
| `tr_arbok_yveltal_snow_coating` | `prizewise` | +4.5 | -2.0 |
| `kangaskhan_tyrantrum_flip_mill` | `prizewise` | -2.5 | +1.5 |
| `ns_zoroark_night_joker_toolbox` | `prizewise` | -2.5 | -2.0 |
| `panic_poison_paralysis` | `prizewise` | +3.0 | -2.5 |
| `crabominable_veluza_food_prep` | `control` | +1.5 | -3.0 |
| `meta_mega_excadrill` | `prizewise` | +4.0 | -3.0 |
| `meta_dragapult_blaziken` | `aggro` | -1.5 | -3.5 |
| `meta_dragapult_pure` | `setup` | -4.0 | +5.5 |
| `chandelure_centiskorch_deck_out` | `control` | +6.0 | -4.5 |
| `arbok_team_rockets_muk_condition_stack` | `prizewise` | -2.5 | -5.0 |
| `mega_scrafty_ex_darkness_tank` | `aggro` | -5.0 | +3.5 |
| `team_rockets_spidops_swarm` | `setup` | +2.5 | -5.0 |
| `meta_dragapult_dusknoir` | `prizewise` | +3.5 | -6.0 |
| `team_rockets_persian_ex_attack_theft` | `aggro` | +5.5 | -6.0 |
| `lurantis_heal_punish` | `setup` | +7.0 | -6.5 |
| `decidueye_ex_judge_sniper_lock` | `prizewise` | +2.5 | -8.0 |

## Does a mirror gain convert into a FIELD gain? Mostly not.

Everything above is a **mirror** measurement: driven by pilot P, does a
deck beat a copy of itself driven by greedy? That is sensitive and
well-paired, and it is not the question anyone cares about, which is
whether the deck wins more **against the field**.

So it was measured directly. Every one of the eight survivors replayed
against all 44 opponents, same CRN seeds as the recorded round robin,
with only that deck's pilot changed and the opponent left on greedy.
Subtracting the recorded greedy result is an exactly-paired field delta.

| deck | pilot | greedy | with pilot | **field delta** | 95% CI | mirror (sel/held) |
|---|---|---|---|---|---|---|
| `heracross_sinistcha_tea` | `setup` | 59.6% | 68.1% | **+8.42** | [+6.81, +10.03] | +12.0/+13.5 |
| `eerie_inferno_ninetales_burn` | `setup` | 48.9% | 55.8% | **+6.89** | [+5.59, +8.19] | +15.5/+8.0 |
| `kyurem_vanilluxe_blizzard` | `setup` | 55.8% | 58.9% | **+3.06** | [+1.48, +4.63] | +8.5/+7.0 |
| `team_rockets_koffing_weezing_bench_swarm` | `setup` | 54.7% | 56.1% | +1.45 | [-0.05, +2.96] | +8.0/+12.0 |
| `salazzle_ex_team_rockets_muk_condition_stack` | `prizewise` | 33.8% | 34.9% | +1.17 | [-0.37, +2.71] | +9.0/+10.5 |
| `stevens_carbink_damage_wall` | `control` | 51.0% | 51.5% | +0.53 | [-0.91, +1.98] | +10.0/+4.0 |
| `meta_slowking` | `control` | 43.6% | 43.6% | +0.00 | [-1.53, +1.53] | +7.0/+8.0 |
| `metal_metang_excadrill` | `prizewise` | 55.5% | 55.3% | -0.20 | [-1.69, +1.29] | +7.5/+12.0 |

**Mean mirror gain +9.38. Mean field gain +2.66. Correlation +0.27.**
The mirror test overstates by roughly a factor of three and barely ranks
the decks in the right order. Five of the eight survivors — including two
that reproduced across both earlier runs — show **no field gain at all**.

Three convert, and all three run `setup`:

| deck | rank under greedy | rank under `setup` |
|---|---|---|
| `heracross_sinistcha_tea` | 59.6% (9) | 68.1% (4) |
| `eerie_inferno_ninetales_burn` | 48.9% (30) | 55.8% (14) |
| `kyurem_vanilluxe_blizzard` | 55.8% (13) | 58.9% (10) |

That is the whole harvest of the pilot programme: **three decks, one
pilot.** `setup` is the worst driver in the field on average and the only
one whose per-deck wins survive all the way to a field measurement. The
decks it helps are the ones that must assemble a board before they
threaten anything, and greedy spends those turns swinging for small
numbers.

### What this retracts

The eight-survivor table above, and the equivalent table in the
2026-09-15 run, were both presented as *the credible ones*. Held-out
validation had already cut 21 candidates to 8; it turns out that was not
enough, because held-out validation of a mirror test only removes
selection bias — it cannot tell you the mirror was the wrong question.
**Read the field-delta column, not the mirror columns.** The mirror test
stays useful for one thing: it is cheap enough to screen 45 decks x 4
pilots, and everything it rejected can be trusted as rejected. What it
accepts has to be confirmed against the field.

