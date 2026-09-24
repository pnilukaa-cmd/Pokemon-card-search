# Field results — every deck against every other deck

Full round robin over **54 decks**, **1000 games** per pairing, 1431 pairings, 1,431,000 games. Each pairing uses its own fixed seed, so a re-run of this field reproduces exactly.

Measured 2026-09-23. **These supersede every number in the deck files before this date.**

## What changed since the 45-deck table

**The field.** 54 decks, up from 45. Added: `wugtrio_paralysis_pin`,
`tauros_risky_ruins`, both Cradily condition builds, and the five mill
study lists. Removed: `selective_bloom_cradily` (no Basic Pokémon, cannot
start a game) and `paralysis_ctl` (a measurement control, not a deck).
30th Celebration (`30C`) is treated as legal; two Maushold lists use it.

**The engine.** Four commits landed after the 45-deck table: the
copy-attack depth guard, the three loose searches (Cyrano, the Ascension
family, Crispin's "different types"), Binding Mochi and Hop's Choice Band
in `DAMAGE_TOOLS`, and Repel / Iron Defender / the when-damaged Tools.

**Same seeds.** Every pairing reuses the `rr1` seed of the previous run,
so a deck present in both runs faces the same dice against the same
opponent.

## How far the old decks moved

Dropping `selective_bloom_cradily` removes a near-certain win from every
deck, which lowers a mean of *m* by about (99.7 − *m*) / 43: −0.6 at the
top of the table, −2.0 at the bottom. After removing that, and scoring
only against the opponents both runs share, the residual moves have a
standard deviation of 0.77. Three decks stand out:

| deck | residual | cause |
|---|---:|---|
| `water_aggro` | −3.51 | **Crispin fix, measured.** Paired A/B across commit `3ec19f3`, `water_aggro` vs all 53 opponents at 400 games: **−4.18 ± 0.50**. The deck is mono-Water with 4 Crispin; Crispin had been fetching 2 Energy where the printed "of different types" allows 1. Neither of the commit's other two fixes is in its list. |
| `hops_snorlax_stacked_buff` | +2.07 | Consistent with Hop's Choice Band now applying its damage. Not isolated by A/B. |
| `meta_slowking` | −1.85 | Consistent with the copy-attack depth guard and Lucky Helmet. Not isolated by A/B. |

No other deck moved by more than 1.4 after the correction.

| # | deck | mean | median | winning | best matchup | worst |
|---|---|---|---|---|---|---|
| 1 | `lurantis_heal_punish` | **73.2%** | 72.9% | 51/53 | study_centiskorch_bastiodon_mill (98%) | scovillain_salazzle_spicy_rage (43%) |
| 2 | `team_rockets_persian_ex_attack_theft` | **70.6%** | 69.6% | 52/53 | study_centiskorch_bastiodon_mill (97%) | tauros_risky_ruins (43%) |
| 3 | `wugtrio_paralysis_pin` | **69.5%** | 72.3% | 48/53 | study_centiskorch_bastiodon_mill (97%) | study_mega_excadrill_drill_mill (38%) |
| 4 | `panic_poison_paralysis` | **68.3%** | 68.2% | 46/53 | study_centiskorch_bastiodon_mill (97%) | lurantis_heal_punish (40%) |
| 5 | `scovillain_salazzle_spicy_rage` | **65.3%** | 65.5% | 45/53 | meta_ns_zoroark (94%) | kyurem_vanilluxe_blizzard (36%) |
| 6 | `cradily_accelgor_conditions` | **64.1%** | 61.7% | 45/53 | feraligatr_munkidori_damage_transfer (97%) | wugtrio_paralysis_pin (38%) |
| 7 | `cradily_amoonguss_conditions` | **63.8%** | 61.1% | 43/53 | meta_ns_zoroark (96%) | wugtrio_paralysis_pin (37%) |
| 8 | `krookodile_ex_relicanth_hand_disruption` | **62.8%** | 64.8% | 43/53 | meta_ns_zoroark (93%) | lurantis_heal_punish (21%) |
| 9 | `tauros_risky_ruins` | **61.6%** | 58.5% | 37/53 | study_centiskorch_bastiodon_mill (94%) | meta_raging_bolt (31%) |
| 10 | `meta_raging_bolt` | **61.2%** | 61.8% | 43/53 | meta_ns_zoroark (90%) | maushold_gnaw_together_mill (30%) |
| 11 | `toxic_slumber_vileplume_ex` | **60.2%** | 58.8% | 38/53 | study_flygon_sandy_flapping_mill (92%) | scovillain_salazzle_spicy_rage (31%) |
| 12 | `heracross_sinistcha_tea` | **59.8%** | 57.8% | 38/53 | study_flygon_sandy_flapping_mill (95%) | scovillain_salazzle_spicy_rage (28%) |
| 13 | `study_mega_excadrill_drill_mill` | **59.1%** | 58.8% | 42/53 | meta_ns_zoroark (96%) | mega_chandelure_ex_retreat_tax (33%) |
| 14 | `meta_mega_excadrill` | **58.8%** | 58.0% | 40/53 | meta_ns_zoroark (91%) | scovillain_salazzle_spicy_rage (35%) |
| 15 | `arbok_muk_laser_darkbell` | **58.1%** | 58.9% | 36/53 | study_centiskorch_bastiodon_mill (93%) | lurantis_heal_punish (26%) |
| 16 | `maushold_gnaw_together_mill` | **58.1%** | 58.0% | 37/53 | meta_ns_zoroark (92%) | lurantis_heal_punish (28%) |
| 17 | `mega_chandelure_ex_retreat_tax` | **56.7%** | 58.1% | 36/53 | study_centiskorch_bastiodon_mill (96%) | panic_poison_paralysis (28%) |
| 18 | `arbok_muk_trolley_darkbell` | **56.2%** | 55.7% | 34/53 | meta_ns_zoroark (94%) | wugtrio_paralysis_pin (26%) |
| 19 | `kyurem_vanilluxe_blizzard` | **55.4%** | 52.6% | 30/53 | study_centiskorch_bastiodon_mill (95%) | meta_mega_excadrill (29%) |
| 20 | `decidueye_ex_judge_sniper_lock` | **54.7%** | 54.4% | 31/53 | study_centiskorch_bastiodon_mill (93%) | lurantis_heal_punish (19%) |
| 21 | `meta_dragapult_pure` | **54.2%** | 51.4% | 33/53 | meta_ns_zoroark (90%) | team_rockets_persian_ex_attack_theft (35%) |
| 22 | `metal_metang_excadrill` | **54.1%** | 51.4% | 29/53 | meta_ns_zoroark (89%) | scovillain_salazzle_spicy_rage (31%) |
| 23 | `dhelmise_veluza_hide_n_sneak` | **54.0%** | 50.0% | 25/53 | meta_ns_zoroark (94%) | lurantis_heal_punish (23%) |
| 24 | `mega_lopunny_dusknoir_snipe_finisher` | **54.0%** | 50.9% | 30/53 | study_centiskorch_bastiodon_mill (89%) | lurantis_heal_punish (34%) |
| 25 | `arbok_team_rockets_muk_condition_stack` | **53.6%** | 52.6% | 33/53 | meta_ns_zoroark (93%) | tauros_risky_ruins (22%) |
| 26 | `team_rockets_koffing_weezing_bench_swarm` | **53.0%** | 51.8% | 32/53 | study_centiskorch_bastiodon_mill (96%) | lurantis_heal_punish (20%) |
| 27 | `orthworm_ex_metal_retaliation` | **52.4%** | 48.4% | 25/53 | study_centiskorch_bastiodon_mill (93%) | scovillain_salazzle_spicy_rage (14%) |
| 28 | `tr_crobat_absol_bench_snipe` | **52.1%** | 51.5% | 31/53 | meta_ns_zoroark (91%) | lurantis_heal_punish (18%) |
| 29 | `stevens_carbink_damage_wall` | **51.8%** | 49.6% | 25/53 | meta_ns_zoroark (95%) | scovillain_salazzle_spicy_rage (24%) |
| 30 | `mega_scrafty_ex_darkness_tank` | **51.7%** | 50.8% | 29/53 | meta_ns_zoroark (90%) | lurantis_heal_punish (15%) |
| 31 | `kangaskhan_tyrantrum_flip_mill` | **51.6%** | 51.6% | 27/53 | meta_ns_zoroark (92%) | team_rockets_persian_ex_attack_theft (27%) |
| 32 | `meta_dragapult_blaziken` | **50.8%** | 48.6% | 24/53 | meta_ns_zoroark (83%) | team_rockets_persian_ex_attack_theft (34%) |
| 33 | `water_aggro` | **50.5%** | 46.4% | 22/53 | study_centiskorch_bastiodon_mill (98%) | lurantis_heal_punish (22%) |
| 34 | `meta_dragapult_dusknoir` | **49.3%** | 45.0% | 19/53 | study_centiskorch_bastiodon_mill (85%) | lurantis_heal_punish (29%) |
| 35 | `eerie_inferno_ninetales_burn` | **49.2%** | 47.7% | 23/53 | study_centiskorch_bastiodon_mill (94%) | wugtrio_paralysis_pin (13%) |
| 36 | `veluza_sinistcha_ex_tea_service` | **48.6%** | 45.5% | 21/53 | meta_ns_zoroark (94%) | wugtrio_paralysis_pin (23%) |
| 37 | `hops_snorlax_stacked_buff` | **47.7%** | 42.1% | 20/53 | study_centiskorch_bastiodon_mill (97%) | lurantis_heal_punish (20%) |
| 38 | `ns_zoroark_night_joker_toolbox` | **47.5%** | 46.2% | 19/53 | static_venom_drapion (81%) | study_mega_excadrill_drill_mill (25%) |
| 39 | `chandelure_centiskorch_deck_out` | **46.2%** | 44.4% | 18/53 | study_centiskorch_bastiodon_mill (91%) | lurantis_heal_punish (14%) |
| 40 | `tr_arbok_yveltal_snow_coating` | **44.2%** | 43.7% | 17/53 | study_centiskorch_bastiodon_mill (95%) | lurantis_heal_punish (11%) |
| 41 | `team_rockets_spidops_swarm` | **43.9%** | 39.4% | 15/53 | study_centiskorch_bastiodon_mill (92%) | wugtrio_paralysis_pin (16%) |
| 42 | `crabominable_veluza_food_prep` | **43.3%** | 39.9% | 12/53 | meta_ns_zoroark (94%) | team_rockets_persian_ex_attack_theft (22%) |
| 43 | `study_hydreigon_zweilous_mill` | **42.1%** | 41.1% | 15/53 | meta_ns_zoroark (88%) | lurantis_heal_punish (14%) |
| 44 | `meta_slowking` | **41.8%** | 42.2% | 13/53 | meta_ns_zoroark (82%) | maushold_gnaw_together_mill (20%) |
| 45 | `darkness_mill_hand_lock` | **39.5%** | 35.7% | 11/53 | study_centiskorch_bastiodon_mill (92%) | lurantis_heal_punish (7%) |
| 46 | `study_maushold_gnaw_latias` | **38.5%** | 37.3% | 12/53 | study_centiskorch_bastiodon_mill (91%) | lurantis_heal_punish (7%) |
| 47 | `meta_festival_lead` | **37.0%** | 35.0% | 8/53 | meta_ns_zoroark (82%) | orthworm_ex_metal_retaliation (16%) |
| 48 | `salazzle_ex_team_rockets_muk_condition_stack` | **33.5%** | 28.4% | 8/53 | meta_ns_zoroark (90%) | wugtrio_paralysis_pin (11%) |
| 49 | `static_venom_drapion` | **30.4%** | 26.1% | 7/53 | study_centiskorch_bastiodon_mill (85%) | tauros_risky_ruins (7%) |
| 50 | `team_rockets_wobbuffet_orbeetle_damage_launder` | **27.0%** | 23.2% | 4/53 | study_centiskorch_bastiodon_mill (88%) | wugtrio_paralysis_pin (5%) |
| 51 | `study_flygon_sandy_flapping_mill` | **21.8%** | 17.2% | 3/53 | meta_ns_zoroark (88%) | lurantis_heal_punish (2%) |
| 52 | `feraligatr_munkidori_damage_transfer` | **21.6%** | 16.6% | 3/53 | study_centiskorch_bastiodon_mill (87%) | cradily_accelgor_conditions (3%) |
| 53 | `study_centiskorch_bastiodon_mill` | **13.3%** | 10.6% | 1/53 | meta_ns_zoroark (62%) | lurantis_heal_punish (2%) |
| 54 | `meta_ns_zoroark` | **12.5%** | 10.1% | 0/53 | static_venom_drapion (41%) | cradily_accelgor_conditions (4%) |

## Full matrix

Row's win rate against column.

| |lurantis_heal_|team_rockets_p|wugtrio_paraly|panic_poison_p|scovillain_sal|cradily_accelg|cradily_amoong|krookodile_ex_|tauros_risky_r|meta_raging_bo|toxic_slumber_|heracross_sini|study_mega_exc|meta_mega_exca|arbok_muk_lase|maushold_gnaw_|mega_chandelur|arbok_muk_trol|kyurem_vanillu|decidueye_ex_j|meta_dragapult|metal_metang_e|dhelmise_veluz|mega_lopunny_d|arbok_team_roc|team_rockets_k|orthworm_ex_me|tr_crobat_abso|stevens_carbin|mega_scrafty_e|kangaskhan_tyr|meta_dragapult|water_aggro|meta_dragapult|eerie_inferno_|veluza_sinistc|hops_snorlax_s|ns_zoroark_nig|chandelure_cen|tr_arbok_yvelt|team_rockets_s|crabominable_v|study_hydreigo|meta_slowking|darkness_mill_|study_maushold|meta_festival_|salazzle_ex_te|static_venom_d|team_rockets_w|study_flygon_s|feraligatr_mun|study_centisko|meta_ns_zoroar|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **lurantis_heal_** |—|47|61|60|43|60|62|79|65|53|68|62|51|51|74|72|59|74|64|81|63|59|77|66|75|80|68|82|66|85|62|64|78|71|71|72|80|70|86|89|81|73|86|74|93|93|82|82|87|94|98|94|98|92|
| **team_rockets_p** |53|—|55|53|58|59|56|63|43|56|66|64|59|60|59|63|58|60|68|77|65|62|71|64|63|70|78|69|68|76|73|66|73|70|75|72|76|66|86|83|80|78|81|77|89|76|81|83|84|91|86|93|97|95|
| **wugtrio_paraly** |39|45|—|57|47|62|63|53|41|54|52|55|38|52|73|60|53|74|63|74|60|54|71|63|74|77|72|74|61|71|60|64|74|66|87|77|78|67|81|82|84|75|73|76|83|88|79|89|91|95|90|96|97|96|
| **panic_poison_p** |40|47|43|—|51|52|44|50|42|56|48|64|64|54|67|69|72|73|62|68|63|64|68|58|69|70|76|66|71|62|64|63|72|64|75|72|79|63|72|81|76|76|78|75|85|88|59|87|87|94|91|92|97|92|
| **scovillain_sal** |57|42|53|49|—|59|60|52|57|54|69|72|64|65|66|48|44|67|36|58|59|69|57|63|71|71|86|70|76|68|58|64|46|67|62|63|72|64|48|76|75|48|70|72|67|72|67|84|82|91|87|79|92|94|
| **cradily_accelg** |40|41|38|48|41|—|46|53|50|52|55|51|49|51|62|58|62|63|56|61|55|50|56|60|65|68|52|73|57|72|64|55|71|60|66|66|70|72|59|68|70|71|78|75|82|83|68|80|87|88|96|97|94|96|
| **cradily_amoong** |38|44|37|56|40|54|—|55|58|49|50|50|39|42|66|53|61|65|57|56|57|47|56|56|70|67|52|78|48|73|59|60|71|61|61|65|71|71|56|68|75|73|77|77|85|82|69|79|84|90|91|94|93|96|
| **krookodile_ex_** |21|37|47|50|48|47|45|—|51|41|44|42|62|54|67|65|67|68|60|43|56|56|64|59|68|69|68|66|72|65|60|61|69|61|70|60|71|57|67|70|62|73|66|62|68|80|68|85|71|90|88|90|88|93|
| **tauros_risky_r** |35|57|59|58|43|50|42|49|—|31|53|50|48|48|73|56|49|74|58|49|56|53|53|63|78|80|54|50|52|54|43|50|65|62|71|61|62|35|77|86|74|72|65|43|84|69|64|83|93|86|91|85|94|72|
| **meta_raging_bo** |47|44|46|44|46|48|51|59|69|—|63|56|45|56|37|30|61|40|64|55|61|62|57|62|50|54|65|61|56|66|58|65|66|67|62|64|71|57|60|70|70|69|65|68|74|63|75|72|79|77|81|79|85|90|
| **toxic_slumber_** |32|34|48|52|31|45|50|56|47|37|—|54|49|46|69|51|41|70|59|46|56|49|65|46|69|76|65|65|66|74|54|51|62|58|43|66|67|58|55|72|61|64|70|58|77|71|66|75|72|85|92|92|86|87|
| **heracross_sini** |38|36|45|36|28|49|50|58|50|44|46|—|36|39|52|54|41|56|60|51|50|44|58|61|57|66|55|69|60|73|58|46|68|59|50|65|67|57|56|68|73|65|71|62|82|82|76|73|82|87|95|85|89|91|
| **study_mega_exc** |49|41|62|36|36|51|61|38|52|55|51|64|—|60|51|47|33|55|70|50|64|61|71|57|57|55|53|61|57|49|60|59|55|65|41|76|61|75|34|58|70|73|60|75|47|52|80|72|69|76|77|71|83|96|
| **meta_mega_exca** |49|40|48|46|35|49|58|46|52|44|54|61|40|—|55|41|39|54|71|52|58|57|50|60|62|59|63|58|53|60|51|57|66|63|53|66|64|57|44|73|67|71|56|65|70|63|79|64|81|77|72|79|75|91|
| **arbok_muk_lase** |26|41|27|33|34|38|34|33|27|63|31|48|49|45|—|60|66|55|49|60|53|53|52|50|53|48|61|52|59|44|64|59|62|59|59|63|67|72|63|60|73|63|70|75|72|80|58|77|79|91|88|92|93|92|
| **maushold_gnaw_** |28|37|40|31|52|42|47|35|44|70|49|46|53|59|40|—|37|44|58|54|53|67|50|50|49|48|70|63|56|60|66|59|53|60|50|64|63|56|66|56|60|65|70|80|60|62|72|79|75|78|79|84|91|92|
| **mega_chandelur** |41|42|47|28|56|38|39|33|51|39|59|59|67|61|34|63|—|36|58|73|51|60|56|48|39|44|56|40|62|49|66|54|62|55|56|63|63|42|68|61|64|69|50|54|60|62|64|73|63|80|86|88|96|76|
| **arbok_muk_trol** |26|40|26|27|33|37|35|32|26|60|30|44|45|46|45|56|64|—|49|56|53|52|53|53|49|47|60|48|54|40|62|58|58|58|57|64|66|69|59|54|72|62|70|73|67|80|54|74|77|93|86|91|91|94|
| **kyurem_vanillu** |36|32|37|38|64|44|43|40|42|36|41|40|30|29|51|42|42|51|—|45|50|32|49|52|59|61|41|54|46|53|43|56|57|57|70|56|62|49|69|73|69|68|58|59|66|73|76|80|78|82|87|86|95|90|
| **decidueye_ex_j** |19|23|26|32|42|39|44|57|51|45|54|49|50|48|40|46|27|44|55|—|40|51|51|46|43|50|61|61|55|69|64|34|55|44|51|59|58|62|58|47|57|71|70|58|74|68|62|73|77|83|89|90|93|89|
| **meta_dragapult** |37|35|40|37|41|45|43|44|44|39|44|50|36|42|47|47|49|47|50|60|—|51|50|54|50|54|53|52|46|51|46|51|59|57|59|52|52|51|59|64|63|60|52|56|64|65|73|63|77|76|75|81|87|90|
| **metal_metang_e** |41|38|46|36|31|50|53|44|47|38|51|56|39|43|47|33|40|48|68|49|49|—|50|52|53|50|62|48|48|56|46|49|61|58|47|61|59|52|38|71|67|66|50|55|64|58|76|60|76|75|67|78|76|89|
| **dhelmise_veluz** |23|29|29|32|43|44|44|36|47|43|35|42|29|50|48|50|44|47|51|49|50|50|—|49|56|41|50|48|50|49|50|56|50|56|64|67|50|58|55|52|61|67|62|77|57|70|80|73|78|78|76|86|86|94|
| **mega_lopunny_d** |34|36|37|42|37|40|44|41|37|38|54|39|43|40|50|50|52|47|48|54|46|48|51|—|49|50|58|49|51|54|47|46|58|51|59|52|60|37|76|68|65|55|55|52|71|64|70|70|70|80|84|86|89|76|
| **arbok_team_roc** |25|37|26|31|29|35|30|32|22|50|31|43|43|38|47|51|61|51|41|57|50|47|44|51|—|48|57|53|51|41|56|56|53|55|53|54|61|66|53|56|66|57|70|70|70|74|52|72|78|88|84|92|89|93|
| **team_rockets_k** |20|30|23|30|29|32|33|31|20|46|24|34|45|41|52|52|56|53|39|50|46|50|59|50|52|—|44|52|50|42|52|52|54|49|52|68|59|55|63|61|62|67|66|65|66|76|63|73|78|85|85|91|96|89|
| **orthworm_ex_me** |32|22|28|24|14|48|48|32|46|35|35|45|47|37|39|30|44|40|59|39|47|38|50|42|43|56|—|50|57|44|38|52|49|52|47|60|70|48|63|82|69|60|54|51|67|78|84|67|74|89|91|81|93|86|
| **tr_crobat_abso** |18|31|26|34|30|27|22|34|50|39|35|31|39|42|48|37|60|52|46|39|48|52|52|51|47|48|50|—|52|46|53|58|54|51|54|50|55|56|54|57|60|59|64|66|66|71|56|71|78|86|87|84|91|91|
| **stevens_carbin** |34|32|39|29|24|43|52|28|48|44|34|40|43|47|41|44|38|46|54|45|54|52|50|49|49|50|43|48|—|40|48|58|51|60|38|61|53|58|37|50|62|62|62|64|53|62|81|67|69|71|79|80|87|95|
| **mega_scrafty_e** |15|24|29|38|32|28|27|35|46|34|26|27|51|40|56|40|51|60|47|31|49|44|51|46|59|58|56|54|60|—|48|49|54|50|64|44|60|43|58|55|53|60|59|55|61|72|64|80|67|87|87|81|90|90|
| **kangaskhan_tyr** |38|27|40|36|42|36|41|40|57|42|46|42|40|49|36|34|34|38|57|36|54|54|50|53|44|48|62|47|52|52|—|57|58|57|52|59|59|49|32|49|59|66|57|58|53|46|68|67|76|69|69|77|74|92|
| **meta_dragapult** |36|34|36|37|36|45|40|39|50|35|49|54|41|43|41|41|46|42|44|66|49|51|44|54|44|48|48|42|42|51|43|—|54|57|53|48|50|45|55|60|62|56|50|50|65|55|65|53|74|69|66|69|82|83|
| **water_aggro** |22|27|26|28|54|29|29|31|35|34|38|32|45|34|38|47|38|42|43|45|41|39|50|42|47|46|51|46|49|46|42|46|—|44|68|54|52|40|83|61|53|59|62|54|66|75|65|76|69|75|89|90|98|85|
| **meta_dragapult** |29|30|34|36|33|40|39|39|38|33|42|41|35|37|41|40|45|42|43|56|43|42|44|49|45|51|48|49|40|50|43|43|56|—|53|43|48|39|58|62|58|53|48|49|62|60|70|58|77|77|75|79|85|82|
| **eerie_inferno_** |29|25|13|25|38|34|39|30|29|38|57|50|59|47|41|50|44|43|30|49|41|53|36|41|47|48|53|46|62|36|48|47|32|47|—|38|51|50|52|56|53|42|66|55|59|62|56|75|69|71|83|84|94|89|
| **veluza_sinistc** |28|28|23|28|37|34|35|40|39|36|34|35|24|34|37|36|37|36|44|41|48|39|33|48|46|32|40|50|39|56|41|52|46|57|62|—|48|54|53|54|56|52|59|60|72|62|79|56|74|79|76|85|86|94|
| **hops_snorlax_s** |20|24|22|21|28|30|29|29|38|29|33|33|39|36|33|37|37|34|38|42|48|41|50|40|39|41|30|45|47|40|41|50|48|52|49|52|—|55|61|56|54|60|59|56|58|62|70|74|72|75|92|91|97|93|
| **ns_zoroark_nig** |30|34|33|37|36|28|29|43|65|43|42|43|25|43|28|44|58|31|51|38|49|48|42|63|34|45|52|44|42|57|51|55|60|61|50|46|45|—|42|47|53|56|42|67|61|49|46|44|81|58|48|60|62|77|
| **chandelure_cen** |14|14|19|28|52|41|44|33|23|40|45|44|66|56|37|34|32|41|31|42|41|62|45|24|47|37|37|46|63|42|68|45|17|42|48|47|39|58|—|32|36|51|59|67|22|49|58|78|54|66|82|72|91|88|
| **tr_arbok_yvelt** |11|17|18|19|24|32|32|30|14|30|28|32|42|27|40|44|39|46|27|53|36|29|48|32|44|39|18|43|50|45|51|40|39|38|44|46|44|53|68|—|47|56|54|48|52|68|61|62|60|68|86|90|95|88|
| **team_rockets_s** |19|20|16|24|25|30|25|38|26|30|39|27|30|33|27|40|36|28|31|43|37|33|39|35|34|38|31|40|38|47|41|38|47|42|47|44|46|47|64|53|—|52|59|55|72|59|57|59|69|74|80|83|92|87|
| **crabominable_v** |27|22|25|24|52|29|27|27|28|31|36|35|27|29|37|35|31|38|32|29|40|34|33|45|43|33|40|41|38|40|34|44|41|47|58|48|40|44|49|44|48|—|46|45|55|54|74|62|68|67|65|79|79|94|
| **study_hydreigo** |14|19|27|22|30|22|23|34|35|35|30|29|40|44|30|30|50|30|42|30|48|50|38|45|30|34|46|36|38|41|43|50|38|52|34|41|41|58|41|46|41|54|—|59|48|47|51|54|66|64|55|62|76|88|
| **meta_slowking** |26|23|24|25|28|25|23|38|57|32|42|38|25|35|25|20|46|27|41|42|44|45|23|48|30|35|49|34|36|45|42|50|46|51|45|40|44|33|33|52|45|55|41|—|56|42|57|49|70|58|60|65|62|82|
| **darkness_mill_** |7|11|17|15|33|18|15|32|16|26|23|18|53|30|28|40|40|33|34|26|36|36|43|29|30|34|33|34|47|39|47|35|34|38|41|28|42|39|78|48|28|45|52|44|—|62|39|66|54|67|82|82|92|74|
| **study_maushold** |7|24|12|12|28|17|18|20|31|37|29|18|48|37|20|38|38|20|27|32|35|42|30|36|26|24|22|29|38|28|54|45|25|40|38|38|38|51|51|32|41|46|53|58|38|—|69|67|49|55|81|66|91|91|
| **meta_festival_** |18|19|21|41|33|32|31|32|36|25|34|24|20|21|42|28|36|46|24|38|27|24|20|30|48|37|16|44|19|36|32|35|35|30|44|21|30|54|42|39|43|26|49|43|61|31|—|48|64|52|65|60|76|82|
| **salazzle_ex_te** |18|17|11|13|16|20|21|15|17|28|25|27|28|36|23|21|27|26|20|27|37|40|27|30|28|27|33|29|33|20|33|47|24|42|25|44|26|56|22|38|41|38|46|51|34|33|52|—|48|51|58|60|77|90|
| **static_venom_d** |13|16|9|13|18|13|16|29|7|21|28|18|31|19|21|25|37|23|22|23|23|24|22|30|22|22|26|22|31|33|24|26|31|23|31|26|28|19|46|40|31|32|34|30|46|51|36|52|—|67|70|65|85|59|
| **team_rockets_w** |6|9|5|6|9|12|10|10|14|23|15|13|24|23|9|22|20|7|18|17|24|25|22|20|12|15|11|14|29|13|31|31|25|23|29|21|25|42|34|32|26|33|36|42|33|45|48|49|33|—|83|79|88|80|
| **study_flygon_s** |2|14|10|9|13|4|9|12|9|19|8|5|23|28|12|21|14|14|13|11|25|33|24|16|16|15|9|13|21|13|31|34|11|25|17|24|8|52|18|14|20|35|45|40|18|19|35|42|30|17|—|25|76|88|
| **feraligatr_mun** |6|7|4|8|21|3|6|10|15|21|8|15|29|21|8|16|12|9|14|10|19|22|14|14|8|9|19|16|20|19|23|31|10|21|16|15|9|40|28|10|17|21|38|35|18|34|40|40|35|21|75|—|87|80|
| **study_centisko** |2|3|3|3|8|6|7|12|6|15|14|11|17|25|7|9|4|9|5|7|13|24|14|11|11|4|7|9|13|10|26|18|2|15|6|14|3|38|9|5|8|21|24|38|8|9|24|23|15|12|24|13|—|62|
| **meta_ns_zoroar** |8|5|4|8|6|4|4|7|28|10|13|9|4|9|8|8|24|6|10|11|10|11|6|24|7|11|14|9|5|10|8|17|15|18|11|6|7|23|12|12|13|6|12|18|26|9|18|10|41|20|12|20|38|—|
