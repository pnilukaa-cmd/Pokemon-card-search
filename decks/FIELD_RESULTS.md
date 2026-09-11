# Field results — every deck against every other deck

Full round robin over **44 decks**, **200 games** per pairing, 946 pairings, 189,200 games. Each pairing uses its own fixed seed, so a re-run of this field reproduces exactly.

Measured 2026-09-11. **These supersede every number recorded in the deck files before this date**, and are not comparable with any earlier run: the engine changed materially in between.

What changed since the 2026-09-11 field. Paying a hand cost used to take whatever sat at the front of the hand -- in `pay_costs`, in `Ultra Ball` (in all 44 decks here) and in `Kofu` -- so decks pitched their own Energy and their own attackers to pay for a search. Measured against the unfixed engine on identical seeds it is field-NEUTRAL (mean -0.03) but not small: 43 of 44 decks moved, mean absolute change 2.07 points, range -6.50 to +6.25. Separately, nine conditional damage bonuses that `attack_damage` could already pay had no condition kind to gate on and were silently dropped -- including +130 on `Mega Excadrill ex`'s Maximum Drilling and +100 on `Team Rocket's Kangaskhan ex`'s Wicked Impact. Every Trainer in every deck here now compiles, and a crash that killed two shards of the previous run is fixed.

> **Read the bottom of the table as a lower bound, not a verdict.** Both sides run the same greedy AI. A list whose edge is in sequencing — holding a Knock Out back, aiming spread damage at a Prize map, choosing when to take the turn off — is piloted by a policy that cannot do any of that, and six measured attempts to make the policy smarter all came out at no detectable difference. Where a deck's placement is known to be an artefact of that, its own file says so.

| # | deck | mean | median | winning | best matchup | worst |
|---|---|---|---|---|---|---|
| 1 | `lurantis_heal_punish` | **72.9%** | 71.0% | 41/43 | team_rockets_wobbuffet_orbeetle_damage_launder (97%) | meta_raging_bolt (44%) |
| 2 | `panic_poison_paralysis` | **72.4%** | 72.5% | 41/43 | team_rockets_wobbuffet_orbeetle_damage_launder (97%) | lurantis_heal_punish (40%) |
| 3 | `team_rockets_persian_ex_attack_theft` | **71.0%** | 72.0% | 42/43 | meta_ns_zoroark (94%) | lurantis_heal_punish (49%) |
| 4 | `meta_raging_bolt` | **62.8%** | 64.0% | 37/43 | meta_ns_zoroark (85%) | arbok_muk_trolley_darkbell (38%) |
| 5 | `meta_mega_excadrill` | **62.5%** | 61.5% | 35/43 | meta_ns_zoroark (92%) | panic_poison_paralysis (38%) |
| 6 | `scovillain_salazzle_spicy_rage` | **61.2%** | 61.0% | 34/43 | meta_ns_zoroark (95%) | water_aggro (34%) |
| 7 | `toxic_slumber_vileplume_ex` | **60.6%** | 62.0% | 35/43 | feraligatr_munkidori_damage_transfer (90%) | team_rockets_persian_ex_attack_theft (28%) |
| 8 | `arbok_muk_laser_darkbell` | **59.5%** | 58.5% | 33/43 | team_rockets_wobbuffet_orbeetle_damage_launder (95%) | panic_poison_paralysis (28%) |
| 9 | `tr_crobat_absol_bench_snipe` | **58.3%** | 56.5% | 31/43 | team_rockets_wobbuffet_orbeetle_damage_launder (95%) | lurantis_heal_punish (20%) |
| 10 | `water_aggro` | **58.2%** | 53.5% | 28/43 | feraligatr_munkidori_damage_transfer (94%) | panic_poison_paralysis (30%) |
| 11 | `arbok_muk_trolley_darkbell` | **58.2%** | 61.0% | 30/43 | meta_ns_zoroark (94%) | lurantis_heal_punish (24%) |
| 12 | `krookodile_ex_relicanth_hand_disruption` | **58.1%** | 60.0% | 32/43 | meta_ns_zoroark (93%) | lurantis_heal_punish (20%) |
| 13 | `kyurem_vanilluxe_blizzard` | **56.2%** | 55.0% | 30/43 | team_rockets_wobbuffet_orbeetle_damage_launder (89%) | meta_mega_excadrill (28%) |
| 14 | `team_rockets_koffing_weezing_bench_swarm` | **55.8%** | 52.5% | 25/43 | feraligatr_munkidori_damage_transfer (93%) | lurantis_heal_punish (19%) |
| 15 | `dhelmise_veluza_hide_n_sneak` | **55.6%** | 54.5% | 27/43 | meta_ns_zoroark (86%) | panic_poison_paralysis (33%) |
| 16 | `arbok_team_rockets_muk_condition_stack` | **55.5%** | 54.5% | 27/43 | team_rockets_wobbuffet_orbeetle_damage_launder (95%) | lurantis_heal_punish (24%) |
| 17 | `mega_chandelure_ex_retreat_tax` | **55.5%** | 57.0% | 29/43 | feraligatr_munkidori_damage_transfer (89%) | panic_poison_paralysis (27%) |
| 18 | `meta_dragapult_pure` | **55.1%** | 53.5% | 29/43 | meta_ns_zoroark (90%) | lurantis_heal_punish (32%) |
| 19 | `heracross_sinistcha_tea` | **54.2%** | 54.5% | 27/43 | meta_ns_zoroark (92%) | panic_poison_paralysis (26%) |
| 20 | `mega_lopunny_dusknoir_snipe_finisher` | **53.7%** | 49.5% | 21/43 | feraligatr_munkidori_damage_transfer (84%) | scovillain_salazzle_spicy_rage (34%) |
| 21 | `orthworm_ex_metal_retaliation` | **52.7%** | 49.0% | 21/43 | meta_festival_lead (90%) | scovillain_salazzle_spicy_rage (18%) |
| 22 | `stevens_carbink_damage_wall` | **52.2%** | 49.5% | 19/43 | meta_ns_zoroark (92%) | scovillain_salazzle_spicy_rage (24%) |
| 23 | `kangaskhan_tyrantrum_flip_mill` | **52.0%** | 51.5% | 24/43 | meta_ns_zoroark (91%) | team_rockets_persian_ex_attack_theft (25%) |
| 24 | `selective_bloom_cradily` | **52.0%** | 48.5% | 21/43 | feraligatr_munkidori_damage_transfer (86%) | meta_mega_excadrill (22%) |
| 25 | `meta_dragapult_blaziken` | **50.2%** | 47.0% | 19/43 | meta_ns_zoroark (83%) | team_rockets_persian_ex_attack_theft (28%) |
| 26 | `meta_dragapult_dusknoir` | **49.7%** | 46.5% | 17/43 | meta_ns_zoroark (84%) | team_rockets_persian_ex_attack_theft (28%) |
| 27 | `ns_zoroark_night_joker_toolbox` | **49.3%** | 47.5% | 17/43 | meta_ns_zoroark (78%) | arbok_muk_trolley_darkbell (34%) |
| 28 | `eerie_inferno_ninetales_burn` | **49.1%** | 46.5% | 19/43 | meta_ns_zoroark (93%) | panic_poison_paralysis (24%) |
| 29 | `mega_scrafty_ex_darkness_tank` | **48.8%** | 48.5% | 20/43 | meta_ns_zoroark (94%) | lurantis_heal_punish (14%) |
| 30 | `decidueye_ex_judge_sniper_lock` | **47.7%** | 44.5% | 15/43 | feraligatr_munkidori_damage_transfer (89%) | panic_poison_paralysis (16%) |
| 31 | `meta_slowking` | **45.2%** | 46.0% | 18/43 | meta_ns_zoroark (82%) | tr_crobat_absol_bench_snipe (22%) |
| 32 | `veluza_sinistcha_ex_tea_service` | **44.7%** | 41.0% | 13/43 | meta_ns_zoroark (92%) | team_rockets_koffing_weezing_bench_swarm (18%) |
| 33 | `hops_snorlax_stacked_buff` | **44.5%** | 41.5% | 12/43 | meta_ns_zoroark (93%) | panic_poison_paralysis (15%) |
| 34 | `team_rockets_spidops_swarm` | **43.3%** | 39.5% | 13/43 | meta_ns_zoroark (86%) | team_rockets_persian_ex_attack_theft (20%) |
| 35 | `tr_arbok_yveltal_snow_coating` | **42.2%** | 41.0% | 11/43 | feraligatr_munkidori_damage_transfer (88%) | lurantis_heal_punish (14%) |
| 36 | `darkness_mill_hand_lock` | **42.0%** | 41.0% | 9/43 | feraligatr_munkidori_damage_transfer (84%) | lurantis_heal_punish (10%) |
| 37 | `chandelure_centiskorch_deck_out` | **41.4%** | 39.5% | 12/43 | meta_ns_zoroark (86%) | team_rockets_persian_ex_attack_theft (14%) |
| 38 | `crabominable_veluza_food_prep` | **39.3%** | 36.5% | 9/43 | meta_ns_zoroark (91%) | team_rockets_persian_ex_attack_theft (20%) |
| 39 | `meta_festival_lead` | **35.4%** | 34.5% | 6/43 | meta_ns_zoroark (82%) | orthworm_ex_metal_retaliation (10%) |
| 40 | `salazzle_ex_team_rockets_muk_condition_stack` | **33.8%** | 31.5% | 5/43 | meta_ns_zoroark (89%) | panic_poison_paralysis (12%) |
| 41 | `static_venom_drapion` | **30.2%** | 28.0% | 4/43 | team_rockets_wobbuffet_orbeetle_damage_launder (66%) | team_rockets_persian_ex_attack_theft (10%) |
| 42 | `team_rockets_wobbuffet_orbeetle_damage_launder` | **23.3%** | 19.5% | 3/43 | feraligatr_munkidori_damage_transfer (78%) | panic_poison_paralysis (3%) |
| 43 | `feraligatr_munkidori_damage_transfer` | **20.0%** | 16.5% | 1/43 | meta_ns_zoroark (80%) | panic_poison_paralysis (4%) |
| 44 | `meta_ns_zoroark` | **13.8%** | 13.0% | 0/43 | static_venom_drapion (40%) | scovillain_salazzle_spicy_rage (5%) |

## Full matrix

Row's win rate against column.

| |lurantis_heal_|panic_poison_p|team_rockets_p|meta_raging_bo|meta_mega_exca|scovillain_sal|toxic_slumber_|arbok_muk_lase|tr_crobat_abso|water_aggro|arbok_muk_trol|krookodile_ex_|kyurem_vanillu|team_rockets_k|dhelmise_veluz|arbok_team_roc|mega_chandelur|meta_dragapult|heracross_sini|mega_lopunny_d|orthworm_ex_me|stevens_carbin|kangaskhan_tyr|selective_bloo|meta_dragapult|meta_dragapult|ns_zoroark_nig|eerie_inferno_|mega_scrafty_e|decidueye_ex_j|meta_slowking|veluza_sinistc|hops_snorlax_s|team_rockets_s|tr_arbok_yvelt|darkness_mill_|chandelure_cen|crabominable_v|meta_festival_|salazzle_ex_te|static_venom_d|team_rockets_w|feraligatr_mun|meta_ns_zoroar|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **lurantis_heal_** |—|60|51|44|52|50|68|69|80|66|76|80|60|81|61|76|60|68|71|60|71|64|64|78|66|68|65|71|86|83|69|74|82|80|86|90|84|78|80|86|89|97|94|94|
| **panic_poison_p** |40|—|47|62|62|62|52|72|69|70|72|62|71|72|67|68|73|54|74|66|81|72|71|68|67|66|60|76|72|84|78|80|85|80|85|84|84|80|66|88|88|97|96|90|
| **team_rockets_p** |49|53|—|55|59|58|72|62|60|68|52|65|68|61|60|66|58|66|64|61|74|65|75|72|72|72|64|74|76|76|73|75|80|80|86|85|86|80|80|84|90|92|92|94|
| **meta_raging_bo** |56|38|45|—|44|51|64|41|52|60|38|69|56|52|62|44|64|61|66|64|60|54|64|76|66|67|61|64|68|56|70|71|66|74|74|68|70|75|80|69|80|76|78|85|
| **meta_mega_exca** |48|38|41|56|—|38|56|54|52|62|60|56|72|50|60|62|42|56|65|59|68|51|54|78|61|70|60|46|70|64|66|78|66|76|78|64|46|78|84|68|78|84|84|92|
| **scovillain_sal** |50|38|42|49|62|—|65|50|55|34|56|48|44|58|54|58|44|61|72|66|82|76|56|78|58|66|66|57|61|65|68|59|64|76|70|57|38|54|69|78|74|84|74|95|
| **toxic_slumber_** |32|48|28|36|44|35|—|68|51|53|66|64|54|76|61|72|38|56|56|52|66|63|54|52|62|56|62|42|75|56|54|63|72|60|76|72|70|73|63|80|75|89|90|86|
| **arbok_muk_lase** |31|28|38|59|46|50|32|—|46|52|49|39|56|57|55|50|70|55|48|58|65|65|64|44|56|58|64|59|55|62|77|67|71|74|59|58|75|68|60|78|80|95|93|90|
| **tr_crobat_abso** |20|31|40|48|48|45|49|54|—|52|56|44|50|55|56|51|69|52|46|58|54|58|65|43|64|50|64|56|46|60|78|61|62|64|64|64|68|68|65|80|78|95|84|92|
| **water_aggro** |34|30|32|40|38|66|47|48|48|—|44|52|46|56|51|49|54|49|49|53|60|50|49|60|54|54|46|72|56|61|62|62|73|69|71|67|80|74|72|84|76|84|94|85|
| **arbok_muk_trol** |24|28|48|62|40|44|34|51|44|56|—|38|50|45|48|56|61|52|44|57|64|63|64|42|66|61|66|64|53|59|71|68|66|70|54|63|67|66|62|74|79|93|90|94|
| **krookodile_ex_** |20|38|35|31|44|52|36|61|56|48|62|—|67|67|58|65|52|50|41|54|64|60|54|37|54|63|60|63|55|44|59|60|68|60|66|65|68|74|65|78|70|91|88|93|
| **kyurem_vanillu** |40|29|32|44|28|56|46|44|50|54|50|33|—|52|48|53|42|51|56|55|48|44|51|54|56|60|57|71|56|54|61|66|65|61|76|56|61|64|78|78|73|89|86|87|
| **team_rockets_k** |19|28|39|48|50|42|24|43|45|44|55|33|48|—|62|54|52|50|48|46|46|58|62|42|48|53|52|52|46|68|68|82|63|66|68|59|67|79|64|71|84|89|93|89|
| **dhelmise_veluz** |39|33|40|38|40|46|39|45|44|49|52|42|52|38|—|54|44|45|55|59|52|41|49|55|54|60|57|66|57|64|64|62|54|70|60|62|58|68|81|68|80|82|86|86|
| **arbok_team_roc** |24|32|34|56|38|42|28|50|49|51|44|35|47|46|46|—|62|54|48|56|54|54|51|42|47|61|62|55|52|58|67|64|71|68|54|62|66|68|60|70|80|95|91|89|
| **mega_chandelur** |40|27|42|36|58|56|62|30|31|46|39|48|58|48|56|38|—|55|56|46|62|57|64|52|62|57|40|59|48|70|54|68|64|60|64|56|60|70|70|72|62|82|89|74|
| **meta_dragapult** |32|46|34|39|44|39|44|45|48|51|48|50|49|50|55|46|45|—|58|56|52|52|54|60|55|53|58|60|60|62|51|52|54|67|70|62|54|59|74|68|70|80|76|90|
| **heracross_sini** |29|26|36|34|35|28|44|52|54|51|56|59|44|52|45|52|44|42|—|52|36|46|48|66|42|58|56|48|72|55|60|66|58|62|60|77|54|61|72|62|73|90|82|92|
| **mega_lopunny_d** |40|34|39|36|41|34|48|42|42|47|43|46|45|54|41|44|54|44|48|—|62|54|46|56|48|50|38|60|52|60|46|54|58|70|76|65|76|56|75|72|76|82|84|76|
| **orthworm_ex_me** |29|19|26|40|32|18|34|35|46|40|36|36|52|54|48|46|38|48|64|38|—|55|40|64|52|54|40|48|49|56|48|70|74|68|84|58|74|64|90|68|72|88|84|86|
| **stevens_carbin** |36|28|35|46|49|24|37|35|42|50|37|40|56|42|59|46|43|48|54|46|45|—|46|64|53|54|62|34|48|52|70|72|56|64|50|50|40|72|82|68|65|74|78|92|
| **kangaskhan_tyr** |36|29|25|36|46|44|46|36|35|51|36|46|49|38|51|49|36|46|52|54|60|54|—|62|58|60|52|41|54|45|56|66|64|58|56|52|38|72|66|72|72|72|79|91|
| **selective_bloo** |22|32|28|24|22|22|48|56|57|40|58|63|46|58|45|58|48|40|34|44|36|36|38|—|41|48|34|56|65|52|46|48|72|64|75|84|78|60|74|70|77|86|86|66|
| **meta_dragapult** |34|33|28|34|39|42|38|44|36|46|34|46|44|52|46|53|38|45|58|52|48|47|42|59|—|52|44|47|46|63|46|50|54|64|54|62|53|61|67|51|78|69|74|83|
| **meta_dragapult** |32|34|28|33|30|34|44|42|50|46|39|37|40|47|40|39|43|47|42|50|46|46|40|52|48|—|44|54|57|55|45|44|56|58|68|60|62|58|68|58|76|80|76|84|
| **ns_zoroark_nig** |35|40|36|39|40|34|38|36|36|54|34|40|43|48|43|38|60|42|44|62|60|38|48|66|56|56|—|53|58|48|65|47|46|46|45|56|48|61|51|48|76|66|64|78|
| **eerie_inferno_** |29|24|26|36|54|43|58|41|44|28|36|37|29|48|34|45|41|40|52|40|52|66|59|44|53|46|47|—|46|60|61|35|51|46|57|58|62|46|52|69|66|74|84|93|
| **mega_scrafty_e** |14|28|24|32|30|39|25|45|54|44|47|45|44|54|43|48|52|40|28|48|51|52|46|35|54|43|42|54|—|34|49|52|60|52|54|54|54|59|66|74|70|88|79|94|
| **decidueye_ex_j** |17|16|24|44|36|35|44|38|40|39|41|56|46|32|36|42|30|38|45|40|44|48|55|48|37|45|52|40|66|—|44|56|62|45|39|70|51|64|60|68|64|78|89|87|
| **meta_slowking** |31|22|27|30|34|32|46|23|22|38|29|41|39|32|36|33|46|49|40|54|52|30|44|54|54|55|35|39|51|56|—|54|52|52|54|58|38|64|64|50|70|60|70|82|
| **veluza_sinistc** |26|20|25|29|22|41|37|33|39|38|32|40|34|18|38|36|32|48|34|46|30|28|34|52|50|56|53|65|48|44|46|—|40|48|45|62|50|57|79|52|72|74|76|92|
| **hops_snorlax_s** |18|15|20|34|34|36|28|29|38|27|34|32|35|37|46|29|36|46|42|42|26|44|36|28|46|44|54|49|40|38|48|60|—|52|64|45|60|70|69|68|68|70|88|93|
| **team_rockets_s** |20|20|20|26|24|24|40|26|36|31|30|40|39|34|30|32|40|33|38|30|32|36|42|36|36|42|54|54|48|55|48|52|48|—|53|70|68|49|52|64|64|79|82|86|
| **tr_arbok_yvelt** |14|15|14|26|22|30|24|41|36|29|46|34|24|32|40|46|36|30|40|24|16|50|44|25|46|32|55|43|46|61|46|55|36|47|—|50|70|59|62|65|59|69|88|87|
| **darkness_mill_** |10|16|15|32|36|43|28|42|36|33|37|35|44|41|38|38|44|38|23|35|42|50|48|16|38|40|44|42|46|30|42|38|55|30|50|—|80|47|44|61|62|78|84|72|
| **chandelure_cen** |16|16|14|30|54|62|30|25|32|20|33|32|39|33|42|34|40|46|46|24|26|60|62|22|47|38|52|38|46|49|62|50|40|32|30|20|—|56|47|66|52|62|70|86|
| **crabominable_v** |22|20|20|25|22|46|27|32|32|26|34|26|36|21|32|32|30|41|39|44|36|28|28|40|39|42|39|54|41|36|36|43|30|51|41|53|44|—|65|56|64|56|74|91|
| **meta_festival_** |20|34|20|20|16|31|37|40|35|28|38|35|22|36|19|40|30|26|28|25|10|18|34|26|33|32|49|48|34|40|36|21|31|48|38|56|53|35|—|46|61|54|58|82|
| **salazzle_ex_te** |14|12|16|31|32|22|20|22|20|16|26|22|22|29|32|30|28|32|38|28|32|32|28|30|49|42|52|31|26|32|50|48|32|36|35|39|34|44|54|—|41|48|58|89|
| **static_venom_d** |11|12|10|20|22|26|25|20|22|24|21|30|27|16|20|20|38|30|27|24|28|35|28|23|22|24|24|34|30|36|30|28|32|36|41|38|48|36|39|59|—|66|58|60|
| **team_rockets_w** |3|3|8|24|16|16|11|5|5|16|7|9|11|11|18|5|18|20|10|18|12|26|28|14|31|20|34|26|12|22|40|26|30|21|31|22|38|44|46|52|34|—|78|76|
| **feraligatr_mun** |6|4|8|22|16|26|10|7|16|6|10|12|14|7|14|9|11|24|18|16|16|22|21|14|26|24|36|16|21|11|30|24|12|18|12|16|30|26|42|42|42|22|—|80|
| **meta_ns_zoroar** |6|10|6|15|8|5|14|10|8|15|6|7|13|11|14|11|26|10|8|24|14|8|9|34|17|16|22|7|6|13|18|8|7|14|13|28|14|9|18|11|40|24|20|—|
