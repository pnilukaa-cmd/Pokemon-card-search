# Field results — every deck against every other deck

Full round robin over **44 decks**, **200 games** per pairing, 946 pairings, 189,200 games. Each pairing uses its own fixed seed, so a re-run of this field reproduces exactly.

Measured 2026-09-15. **These supersede every number recorded in the deck files before this date**, and are not comparable with any earlier run: the engine changed materially in between.

What changed since the 2026-09-13 field: every one of the 2198 card effects in the pool is now handled by some mechanism -- 282 abilities, 1641 attacks, 257 Trainers, 18 Energy, 100.000% on all four. The measure is ACCOUNTED FOR, not "compiles": damage scalers live in attack_damage rather than the IR, so a compile check understates coverage badly. Attacks began this session at 93.358%. The tail closed here was 109 attacks in 86 shapes plus 40 across abilities and Trainers -- condition-gated fizzles that had been dealing full damage unconditionally, hand disruption, Bench splash, defender locks, recall and bounce, Energy and counter movement, outright Knock Outs, the Berry cycle, and the last six orphan ops. Two card shapes are modelled as nothing DELIBERATELY and by name: hidden-information effects, and deckbuilding or setup-phase rules.

> **100% accounted for is not 100% exact.** Every card's text now reaches some mechanism; several tail effects are reasonable approximations rather than tournament-precise implementations. `audit_ops.py --cards` reports the op-level state, and now also flags a reader that nothing calls -- which caught five dead query functions the moment it was written.

> **Read the bottom of the table as a lower bound, not a verdict.** Both sides run the same greedy AI. A list whose edge is in sequencing — holding a Knock Out back, aiming spread damage at a Prize map, choosing when to take the turn off — is piloted by a policy that cannot do any of that, and six measured attempts to make the policy smarter all came out at no detectable difference. Where a deck's placement is known to be an artefact of that, its own file says so.

| # | deck | mean | median | winning | best matchup | worst |
|---|---|---|---|---|---|---|
| 1 | `lurantis_heal_punish` | **72.3%** | 71.0% | 42/43 | feraligatr_munkidori_damage_transfer (95%) | scovillain_salazzle_spicy_rage (46%) |
| 2 | `panic_poison_paralysis` | **71.3%** | 71.0% | 40/43 | feraligatr_munkidori_damage_transfer (96%) | krookodile_ex_relicanth_hand_disruption (46%) |
| 3 | `team_rockets_persian_ex_attack_theft` | **70.5%** | 70.0% | 41/43 | feraligatr_munkidori_damage_transfer (94%) | panic_poison_paralysis (44%) |
| 4 | `scovillain_salazzle_spicy_rage` | **63.9%** | 64.5% | 35/43 | meta_ns_zoroark (94%) | team_rockets_persian_ex_attack_theft (38%) |
| 5 | `krookodile_ex_relicanth_hand_disruption` | **63.7%** | 63.0% | 37/43 | meta_ns_zoroark (92%) | lurantis_heal_punish (28%) |
| 6 | `meta_raging_bolt` | **62.8%** | 63.5% | 36/43 | meta_ns_zoroark (93%) | arbok_muk_laser_darkbell (36%) |
| 7 | `meta_mega_excadrill` | **61.3%** | 61.5% | 35/43 | meta_ns_zoroark (89%) | scovillain_salazzle_spicy_rage (36%) |
| 8 | `heracross_sinistcha_tea` | **60.2%** | 60.0% | 33/43 | meta_ns_zoroark (92%) | scovillain_salazzle_spicy_rage (27%) |
| 9 | `toxic_slumber_vileplume_ex` | **60.1%** | 62.0% | 35/43 | feraligatr_munkidori_damage_transfer (94%) | lurantis_heal_punish (32%) |
| 10 | `arbok_muk_laser_darkbell` | **59.1%** | 59.0% | 30/43 | feraligatr_munkidori_damage_transfer (96%) | panic_poison_paralysis (28%) |
| 11 | `arbok_muk_trolley_darkbell` | **57.1%** | 57.0% | 29/43 | meta_ns_zoroark (94%) | lurantis_heal_punish (24%) |
| 12 | `dhelmise_veluza_hide_n_sneak` | **57.0%** | 56.5% | 28/43 | meta_ns_zoroark (92%) | meta_mega_excadrill (34%) |
| 13 | `kyurem_vanilluxe_blizzard` | **56.8%** | 56.0% | 27/43 | team_rockets_wobbuffet_orbeetle_damage_launder (89%) | team_rockets_persian_ex_attack_theft (29%) |
| 14 | `mega_chandelure_ex_retreat_tax` | **56.2%** | 58.5% | 30/43 | feraligatr_munkidori_damage_transfer (88%) | panic_poison_paralysis (28%) |
| 15 | `arbok_team_rockets_muk_condition_stack` | **55.2%** | 54.0% | 27/43 | feraligatr_munkidori_damage_transfer (94%) | lurantis_heal_punish (24%) |
| 16 | `team_rockets_koffing_weezing_bench_swarm` | **55.2%** | 53.5% | 27/43 | feraligatr_munkidori_damage_transfer (91%) | lurantis_heal_punish (19%) |
| 17 | `meta_dragapult_pure` | **54.7%** | 52.0% | 26/43 | meta_ns_zoroark (90%) | team_rockets_persian_ex_attack_theft (28%) |
| 18 | `water_aggro` | **53.6%** | 50.5% | 22/43 | feraligatr_munkidori_damage_transfer (95%) | panic_poison_paralysis (27%) |
| 19 | `mega_lopunny_dusknoir_snipe_finisher` | **53.6%** | 53.0% | 23/43 | feraligatr_munkidori_damage_transfer (85%) | meta_mega_excadrill (33%) |
| 20 | `tr_crobat_absol_bench_snipe` | **53.0%** | 51.0% | 25/43 | meta_ns_zoroark (90%) | lurantis_heal_punish (14%) |
| 21 | `orthworm_ex_metal_retaliation` | **52.2%** | 50.0% | 19/43 | meta_festival_lead (90%) | scovillain_salazzle_spicy_rage (12%) |
| 22 | `selective_bloom_cradily` | **51.9%** | 49.0% | 21/43 | feraligatr_munkidori_damage_transfer (86%) | meta_mega_excadrill (15%) |
| 23 | `stevens_carbink_damage_wall` | **51.4%** | 48.0% | 19/43 | meta_ns_zoroark (93%) | scovillain_salazzle_spicy_rage (26%) |
| 24 | `meta_dragapult_blaziken` | **51.1%** | 47.5% | 19/43 | meta_ns_zoroark (86%) | meta_raging_bolt (34%) |
| 25 | `kangaskhan_tyrantrum_flip_mill` | **50.6%** | 50.0% | 21/43 | meta_ns_zoroark (90%) | team_rockets_persian_ex_attack_theft (26%) |
| 26 | `ns_zoroark_night_joker_toolbox` | **50.3%** | 48.0% | 17/43 | static_venom_drapion (76%) | arbok_muk_trolley_darkbell (34%) |
| 27 | `mega_scrafty_ex_darkness_tank` | **49.9%** | 50.0% | 21/43 | meta_ns_zoroark (93%) | lurantis_heal_punish (13%) |
| 28 | `eerie_inferno_ninetales_burn` | **49.0%** | 48.0% | 20/43 | meta_ns_zoroark (90%) | panic_poison_paralysis (20%) |
| 29 | `meta_dragapult_dusknoir` | **48.9%** | 45.5% | 14/43 | meta_ns_zoroark (86%) | team_rockets_persian_ex_attack_theft (24%) |
| 30 | `veluza_sinistcha_ex_tea_service` | **48.7%** | 48.0% | 20/43 | meta_ns_zoroark (92%) | panic_poison_paralysis (20%) |
| 31 | `decidueye_ex_judge_sniper_lock` | **48.0%** | 44.5% | 16/43 | feraligatr_munkidori_damage_transfer (94%) | panic_poison_paralysis (16%) |
| 32 | `hops_snorlax_stacked_buff` | **44.4%** | 42.5% | 13/43 | feraligatr_munkidori_damage_transfer (94%) | panic_poison_paralysis (13%) |
| 33 | `meta_slowking` | **44.2%** | 44.0% | 12/43 | meta_ns_zoroark (80%) | team_rockets_persian_ex_attack_theft (17%) |
| 34 | `team_rockets_spidops_swarm` | **44.1%** | 41.0% | 13/43 | meta_ns_zoroark (93%) | lurantis_heal_punish (16%) |
| 35 | `crabominable_veluza_food_prep` | **43.8%** | 41.0% | 10/43 | meta_ns_zoroark (94%) | team_rockets_persian_ex_attack_theft (21%) |
| 36 | `tr_arbok_yveltal_snow_coating` | **41.2%** | 40.0% | 10/43 | feraligatr_munkidori_damage_transfer (90%) | panic_poison_paralysis (12%) |
| 37 | `chandelure_centiskorch_deck_out` | **39.6%** | 38.0% | 11/43 | meta_ns_zoroark (87%) | water_aggro (13%) |
| 38 | `darkness_mill_hand_lock` | **37.5%** | 33.5% | 8/43 | feraligatr_munkidori_damage_transfer (86%) | lurantis_heal_punish (6%) |
| 39 | `meta_festival_lead` | **35.4%** | 36.5% | 4/43 | meta_ns_zoroark (83%) | orthworm_ex_metal_retaliation (10%) |
| 40 | `salazzle_ex_team_rockets_muk_condition_stack` | **34.3%** | 32.0% | 4/43 | meta_ns_zoroark (87%) | panic_poison_paralysis (13%) |
| 41 | `static_venom_drapion` | **29.3%** | 25.5% | 5/43 | team_rockets_wobbuffet_orbeetle_damage_launder (65%) | panic_poison_paralysis (9%) |
| 42 | `team_rockets_wobbuffet_orbeetle_damage_launder` | **25.1%** | 21.5% | 4/43 | meta_ns_zoroark (82%) | lurantis_heal_punish (5%) |
| 43 | `feraligatr_munkidori_damage_transfer` | **18.4%** | 15.0% | 1/43 | meta_ns_zoroark (80%) | arbok_muk_laser_darkbell (4%) |
| 44 | `meta_ns_zoroark` | **13.2%** | 10.5% | 0/43 | static_venom_drapion (41%) | arbok_muk_trolley_darkbell (6%) |

## Full matrix

Row's win rate against column.

| |lurantis_heal_|panic_poison_p|team_rockets_p|scovillain_sal|krookodile_ex_|meta_raging_bo|meta_mega_exca|heracross_sini|toxic_slumber_|arbok_muk_lase|arbok_muk_trol|dhelmise_veluz|kyurem_vanillu|mega_chandelur|arbok_team_roc|team_rockets_k|meta_dragapult|water_aggro|mega_lopunny_d|tr_crobat_abso|orthworm_ex_me|selective_bloo|stevens_carbin|meta_dragapult|kangaskhan_tyr|ns_zoroark_nig|mega_scrafty_e|eerie_inferno_|meta_dragapult|veluza_sinistc|decidueye_ex_j|hops_snorlax_s|meta_slowking|team_rockets_s|crabominable_v|tr_arbok_yvelt|chandelure_cen|darkness_mill_|meta_festival_|salazzle_ex_te|static_venom_d|team_rockets_w|feraligatr_mun|meta_ns_zoroar|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **lurantis_heal_** |—|54|50|46|72|54|53|58|68|69|76|58|64|60|76|81|64|69|60|86|71|78|64|60|69|65|87|71|70|68|83|82|70|84|74|86|86|94|80|78|89|95|95|91|
| **panic_poison_p** |46|—|56|58|46|56|60|68|50|72|67|60|68|72|70|71|59|73|64|68|78|64|69|61|74|62|73|80|64|80|84|87|80|74|76|88|82|86|63|87|91|93|96|90|
| **team_rockets_p** |50|44|—|62|60|56|56|60|66|64|56|64|71|58|58|68|72|67|61|62|77|62|66|64|74|64|70|74|76|73|80|80|83|80|79|74|84|87|78|86|84|94|94|92|
| **scovillain_sal** |54|42|38|—|49|53|64|73|66|59|61|49|43|41|64|66|57|46|60|66|88|75|74|64|54|64|70|58|68|64|66|69|64|76|54|73|48|72|72|80|82|88|78|94|
| **krookodile_ex_** |28|54|40|51|—|39|56|44|47|68|69|62|68|65|69|69|66|60|60|63|72|40|72|61|63|58|63|72|62|59|54|74|59|62|71|74|78|76|66|84|76|87|88|92|
| **meta_raging_bo** |46|44|44|47|61|—|60|56|64|36|44|60|58|60|50|53|60|60|66|61|67|80|56|66|64|56|72|58|64|64|60|70|64|74|68|75|64|70|78|72|86|75|77|93|
| **meta_mega_exca** |47|40|44|36|44|40|—|59|62|54|54|66|65|38|59|54|59|72|67|54|61|85|53|62|54|64|62|56|62|70|62|68|70|68|73|80|44|70|74|64|77|78|78|89|
| **heracross_sini** |42|32|40|27|56|44|41|—|36|58|60|50|46|48|59|61|58|68|60|66|57|68|54|47|62|59|74|51|55|64|56|68|62|73|67|64|62|84|80|76|81|87|90|92|
| **toxic_slumber_** |32|50|34|34|53|36|38|64|—|68|66|56|57|38|72|76|55|62|52|64|66|52|63|52|55|62|71|42|58|62|56|72|55|56|66|76|58|78|63|75|75|87|94|83|
| **arbok_muk_lase** |31|28|36|41|32|64|46|42|32|—|49|54|50|70|50|57|52|57|58|50|65|44|65|61|64|64|50|59|59|68|62|71|68|73|66|59|73|71|60|76|80|92|96|92|
| **arbok_muk_trol** |24|33|44|39|31|56|46|40|34|51|—|48|56|61|56|45|48|52|57|48|64|42|63|60|57|66|42|64|56|62|59|66|80|71|62|54|69|62|62|68|79|94|92|94|
| **dhelmise_veluz** |42|40|36|51|38|40|34|50|44|46|52|—|50|43|58|40|56|58|61|50|52|58|45|54|47|50|57|68|58|63|62|56|68|68|70|66|70|68|78|59|80|83|88|92|
| **kyurem_vanillu** |36|32|29|57|32|42|35|54|43|50|44|50|—|37|55|49|52|60|56|56|43|64|45|58|55|50|55|70|64|56|50|69|56|69|68|76|70|62|68|83|78|89|88|86|
| **mega_chandelur** |40|28|42|59|35|40|62|52|62|30|39|57|63|—|38|48|52|60|46|38|62|52|57|56|64|40|48|59|60|64|70|64|57|58|72|64|58|62|70|76|62|78|88|82|
| **arbok_team_roc** |24|30|42|36|31|50|41|41|28|50|44|42|45|62|—|46|52|54|56|48|54|42|54|56|51|62|52|55|52|63|58|71|68|66|59|54|70|78|60|70|80|90|94|93|
| **team_rockets_k** |19|29|32|34|31|47|46|39|24|43|55|60|51|52|54|—|49|56|46|45|46|42|58|50|64|52|46|52|54|70|68|63|64|70|62|68|78|64|64|73|84|86|91|90|
| **meta_dragapult** |36|41|28|43|34|40|41|42|45|48|52|44|48|48|48|51|—|52|60|52|50|58|51|54|62|53|58|58|60|46|66|46|57|64|61|65|61|70|72|62|78|79|82|90|
| **water_aggro** |31|27|33|54|40|40|28|32|38|43|48|42|40|40|46|44|48|—|45|47|50|51|53|48|43|42|57|76|60|52|60|57|52|62|62|70|87|66|76|77|74|80|95|88|
| **mega_lopunny_d** |40|36|39|40|40|34|33|40|48|42|43|39|44|54|44|54|40|55|—|50|62|56|54|46|50|38|53|60|50|50|60|58|54|60|58|76|80|68|75|72|76|79|85|72|
| **tr_crobat_abso** |14|32|38|34|37|39|46|34|36|50|52|50|44|62|52|55|48|53|50|—|50|45|52|53|62|52|49|49|48|48|50|56|70|58|58|51|67|64|61|75|76|83|86|90|
| **orthworm_ex_me** |29|22|23|12|28|33|39|43|34|35|36|48|57|38|46|54|50|50|38|50|—|64|55|48|36|40|45|48|59|64|56|74|50|70|58|84|72|67|90|66|72|88|84|86|
| **selective_bloo** |22|36|38|25|60|20|15|32|48|56|58|42|36|48|58|58|42|49|44|55|36|—|36|40|44|34|70|56|48|44|52|72|45|59|56|75|76|81|74|69|77|86|86|73|
| **stevens_carbin** |36|31|34|26|28|44|47|46|37|35|37|55|55|43|46|42|49|47|46|48|45|64|—|64|40|62|43|34|60|59|52|56|68|70|62|50|43|52|82|68|65|73|77|93|
| **meta_dragapult** |40|39|36|36|39|34|38|53|48|39|40|46|42|44|44|50|46|52|54|47|52|60|36|—|46|40|52|44|60|45|62|58|46|66|49|69|56|64|64|53|78|74|71|86|
| **kangaskhan_tyr** |31|26|26|46|37|36|46|38|45|36|43|53|45|36|49|36|38|57|50|38|64|56|60|54|—|50|51|44|50|54|46|66|61|60|66|55|38|50|63|68|72|68|80|90|
| **ns_zoroark_nig** |35|38|36|36|42|44|36|41|38|36|34|50|50|60|38|48|47|58|62|48|60|66|38|60|50|—|60|53|52|48|48|46|70|47|59|45|46|66|51|50|76|60|62|75|
| **mega_scrafty_e** |13|27|30|30|37|28|38|26|29|50|58|43|45|52|48|54|42|43|47|51|55|30|57|48|49|40|—|58|51|40|38|71|56|50|64|60|64|52|64|78|70|86|80|93|
| **eerie_inferno_** |29|20|26|42|28|42|44|49|58|41|36|32|30|41|45|48|42|24|40|51|52|44|66|56|56|47|42|—|46|38|60|51|58|54|52|57|62|67|52|74|66|68|85|90|
| **meta_dragapult** |30|36|24|32|38|36|38|45|42|41|44|42|36|40|48|46|40|40|50|52|41|52|40|40|50|48|49|54|—|42|60|45|50|58|49|64|52|63|70|63|74|75|76|86|
| **veluza_sinistc** |32|20|27|36|41|36|30|36|38|32|38|37|44|36|37|30|54|48|50|52|36|56|41|55|46|52|60|62|58|—|34|41|51|50|51|54|58|73|79|56|72|75|86|92|
| **decidueye_ex_j** |17|16|20|34|46|40|38|44|44|38|41|38|50|30|42|32|34|40|40|50|44|48|48|38|54|52|62|40|40|66|—|62|44|50|68|39|54|73|60|70|64|76|94|84|
| **hops_snorlax_s** |18|13|20|31|26|30|32|32|28|29|34|44|31|36|29|37|54|43|42|44|26|28|44|42|34|54|29|49|55|59|38|—|48|50|56|64|58|50|69|74|68|75|94|94|
| **meta_slowking** |30|20|17|36|41|36|30|38|45|32|20|32|44|43|32|36|43|48|46|30|50|55|32|54|39|30|44|42|50|49|56|52|—|46|53|60|42|58|61|48|74|64|62|80|
| **team_rockets_s** |16|26|20|24|38|26|32|27|44|27|29|32|31|42|34|30|36|38|40|42|30|41|30|34|40|53|50|46|42|50|50|50|54|—|57|58|73|72|60|57|68|74|84|93|
| **crabominable_v** |26|24|21|46|29|32|27|33|34|34|38|30|32|28|41|38|39|38|42|42|42|44|38|51|34|41|36|48|51|49|32|44|47|43|—|46|56|60|78|58|72|64|78|94|
| **tr_arbok_yvelt** |14|12|26|27|26|25|20|36|24|41|46|34|24|36|46|32|35|30|24|49|16|25|50|31|45|55|40|43|36|46|61|36|40|42|54|—|68|48|62|62|59|76|90|84|
| **chandelure_cen** |14|18|16|52|22|36|56|38|42|27|31|30|30|42|30|22|39|13|20|33|28|24|57|44|62|54|36|38|48|42|46|42|58|27|44|32|—|16|58|62|48|64|74|87|
| **darkness_mill_** |6|14|13|28|24|30|30|16|22|29|38|32|38|38|22|36|30|34|32|36|33|19|48|36|50|34|48|33|37|27|27|50|42|28|40|52|84|—|40|64|51|60|86|74|
| **meta_festival_** |20|37|22|28|34|22|26|20|37|40|38|22|32|30|40|36|28|24|25|39|10|26|18|36|37|49|36|48|30|21|40|31|39|40|22|38|42|60|—|41|61|49|63|83|
| **salazzle_ex_te** |22|13|14|20|16|28|36|24|25|24|32|41|17|24|30|27|38|23|28|25|34|31|32|47|32|50|22|26|37|44|30|26|52|43|42|38|38|36|59|—|48|47|62|87|
| **static_venom_d** |11|9|16|18|24|14|23|19|25|20|21|20|22|38|20|16|22|26|24|24|28|23|35|22|28|24|30|34|26|28|36|32|26|32|28|41|52|49|39|52|—|65|64|59|
| **team_rockets_w** |5|7|6|12|13|25|22|13|13|8|6|17|11|22|10|14|21|20|21|17|12|14|27|26|32|40|14|32|25|25|24|25|36|26|36|24|36|40|51|53|35|—|80|82|
| **feraligatr_mun** |5|4|6|22|12|23|22|10|6|4|8|12|12|12|6|9|18|5|15|14|16|14|23|29|20|38|20|15|24|14|6|6|38|16|22|10|26|14|37|38|36|20|—|80|
| **meta_ns_zoroar** |9|10|8|6|8|7|11|8|17|8|6|8|14|18|7|10|10|12|28|10|14|27|7|14|10|25|7|10|14|8|16|6|20|7|6|16|13|26|17|13|41|18|20|—|
