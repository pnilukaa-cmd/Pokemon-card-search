# Field results — every deck against every other deck

Full round robin over **45 decks**, **200 games** per pairing, 990 pairings, 198,000 games. Each pairing uses its own fixed seed, so a re-run of this field reproduces exactly.

Measured 2026-09-21, after the Fossil-setup fix. **These supersede every number in the deck files before this date.**

What changed, and what did NOT.

- **A Fossil is an Item, so it cannot be your opening Pokemon.** Its text says to play it *as if it were* a Basic Pokemon, and Items are played during your turn -- setup is not your turn. Fossils had been counted as Basics everywhere, including for the opening hand. This is the only change that moved the field, and it moved one deck: `selective_bloom_cradily` runs 4 Lileep, 4 Cradily and 4 Antique Root Fossil, has **zero Basic Pokemon**, and cannot start a game at all. It goes from 51.1% at rank 25 to **0.3% at rank 45**. Its old placement was never real. The deck file is kept rather than deleted, because dropping a deck changes every other deck's mean.
- **"100 damage for each Special Condition" now scales** (Cradily's Miasma Wind, Team Rocket's Muk's Hazardous Venom); it had been a flat 100.
- **Asleep, Confused and Paralyzed are now mutually exclusive**, so the real ceiling is three conditions at once rather than five.

Those last two were expected to shake the top of the table -- five decks run Team Rocket's Muk, including `panic_poison_paralysis` at rank 2. **They did not.** Excluding the collapsed deck, whose free win inflates everyone by about a point, the five Muk decks move between -0.87 and +0.40, all inside a 1.5-point noise floor. The scaler makes the attack hit harder and the exclusivity cap means fewer conditions to count; the two cancel. The only decks clearing the floor are `kyurem_vanilluxe_blizzard` (+1.66) and `meta_dragapult_pure` (+1.55), and both match the Blizzard Burst and Risky Ruins deltas already measured against this same stale baseline -- they are not today's work.

| # | deck | mean | median | winning | best matchup | worst |
|---|---|---|---|---|---|---|
| 1 | `lurantis_heal_punish` | **73.1%** | 71.5% | 43/44 | selective_bloom_cradily (100%) | scovillain_salazzle_spicy_rage (46%) |
| 2 | `panic_poison_paralysis` | **71.6%** | 70.2% | 42/44 | selective_bloom_cradily (100%) | lurantis_heal_punish (49%) |
| 3 | `team_rockets_persian_ex_attack_theft` | **71.6%** | 69.2% | 43/44 | selective_bloom_cradily (100%) | lurantis_heal_punish (50%) |
| 4 | `krookodile_ex_relicanth_hand_disruption` | **64.4%** | 63.8% | 37/44 | selective_bloom_cradily (100%) | lurantis_heal_punish (28%) |
| 5 | `scovillain_salazzle_spicy_rage` | **63.8%** | 64.5% | 37/44 | selective_bloom_cradily (100%) | kyurem_vanilluxe_blizzard (37%) |
| 6 | `meta_raging_bolt` | **62.5%** | 61.5% | 37/44 | selective_bloom_cradily (100%) | arbok_muk_laser_darkbell (38%) |
| 7 | `meta_mega_excadrill` | **61.4%** | 61.2% | 34/44 | selective_bloom_cradily (100%) | scovillain_salazzle_spicy_rage (36%) |
| 8 | `toxic_slumber_vileplume_ex` | **60.4%** | 62.0% | 33/44 | selective_bloom_cradily (100%) | lurantis_heal_punish (32%) |
| 9 | `arbok_muk_laser_darkbell` | **60.3%** | 60.0% | 35/44 | selective_bloom_cradily (100%) | lurantis_heal_punish (26%) |
| 10 | `heracross_sinistcha_tea` | **59.7%** | 59.8% | 33/44 | selective_bloom_cradily (100%) | scovillain_salazzle_spicy_rage (27%) |
| 11 | `kyurem_vanilluxe_blizzard` | **58.2%** | 57.5% | 28/44 | selective_bloom_cradily (100%) | meta_mega_excadrill (25%) |
| 12 | `arbok_muk_trolley_darkbell` | **57.8%** | 56.0% | 30/44 | selective_bloom_cradily (100%) | lurantis_heal_punish (23%) |
| 13 | `mega_chandelure_ex_retreat_tax` | **56.8%** | 58.8% | 29/44 | selective_bloom_cradily (100%) | panic_poison_paralysis (27%) |
| 14 | `meta_dragapult_pure` | **56.5%** | 53.2% | 29/44 | selective_bloom_cradily (100%) | team_rockets_persian_ex_attack_theft (32%) |
| 15 | `metal_metang_excadrill` | **55.7%** | 53.2% | 25/44 | selective_bloom_cradily (100%) | scovillain_salazzle_spicy_rage (28%) |
| 16 | `team_rockets_koffing_weezing_bench_swarm` | **55.3%** | 53.8% | 27/44 | selective_bloom_cradily (100%) | lurantis_heal_punish (19%) |
| 17 | `arbok_team_rockets_muk_condition_stack` | **55.0%** | 52.8% | 25/44 | selective_bloom_cradily (100%) | lurantis_heal_punish (20%) |
| 18 | `mega_lopunny_dusknoir_snipe_finisher` | **54.5%** | 53.0% | 24/44 | selective_bloom_cradily (100%) | meta_mega_excadrill (33%) |
| 19 | `dhelmise_veluza_hide_n_sneak` | **54.4%** | 51.2% | 25/44 | selective_bloom_cradily (100%) | lurantis_heal_punish (22%) |
| 20 | `water_aggro` | **54.2%** | 51.0% | 23/44 | selective_bloom_cradily (100%) | meta_mega_excadrill (28%) |
| 21 | `tr_crobat_absol_bench_snipe` | **54.1%** | 51.8% | 25/44 | selective_bloom_cradily (100%) | lurantis_heal_punish (14%) |
| 22 | `decidueye_ex_judge_sniper_lock` | **53.6%** | 51.8% | 24/44 | selective_bloom_cradily (98%) | team_rockets_persian_ex_attack_theft (16%) |
| 23 | `kangaskhan_tyrantrum_flip_mill` | **52.5%** | 52.8% | 25/44 | selective_bloom_cradily (100%) | team_rockets_persian_ex_attack_theft (24%) |
| 24 | `orthworm_ex_metal_retaliation` | **52.4%** | 49.5% | 19/44 | selective_bloom_cradily (100%) | scovillain_salazzle_spicy_rage (12%) |
| 25 | `meta_dragapult_blaziken` | **52.2%** | 50.5% | 24/44 | selective_bloom_cradily (100%) | scovillain_salazzle_spicy_rage (34%) |
| 26 | `mega_scrafty_ex_darkness_tank` | **52.0%** | 50.5% | 22/44 | selective_bloom_cradily (100%) | lurantis_heal_punish (13%) |
| 27 | `stevens_carbink_damage_wall` | **51.8%** | 47.8% | 18/44 | selective_bloom_cradily (100%) | scovillain_salazzle_spicy_rage (26%) |
| 28 | `ns_zoroark_night_joker_toolbox` | **50.8%** | 47.2% | 19/44 | selective_bloom_cradily (100%) | arbok_muk_trolley_darkbell (34%) |
| 29 | `meta_dragapult_dusknoir` | **50.2%** | 46.0% | 15/44 | selective_bloom_cradily (100%) | team_rockets_persian_ex_attack_theft (28%) |
| 30 | `eerie_inferno_ninetales_burn` | **49.9%** | 48.0% | 20/44 | selective_bloom_cradily (100%) | water_aggro (24%) |
| 31 | `veluza_sinistcha_ex_tea_service` | **49.1%** | 44.0% | 19/44 | selective_bloom_cradily (100%) | panic_poison_paralysis (23%) |
| 32 | `hops_snorlax_stacked_buff` | **46.2%** | 43.5% | 13/44 | selective_bloom_cradily (100%) | panic_poison_paralysis (16%) |
| 33 | `chandelure_centiskorch_deck_out` | **45.1%** | 45.0% | 15/44 | selective_bloom_cradily (98%) | team_rockets_persian_ex_attack_theft (14%) |
| 34 | `team_rockets_spidops_swarm` | **44.8%** | 40.8% | 14/44 | selective_bloom_cradily (100%) | lurantis_heal_punish (16%) |
| 35 | `meta_slowking` | **44.6%** | 43.5% | 11/44 | selective_bloom_cradily (100%) | team_rockets_persian_ex_attack_theft (17%) |
| 36 | `crabominable_veluza_food_prep` | **44.6%** | 41.2% | 9/44 | selective_bloom_cradily (100%) | team_rockets_persian_ex_attack_theft (21%) |
| 37 | `tr_arbok_yveltal_snow_coating` | **42.6%** | 39.2% | 12/44 | selective_bloom_cradily (100%) | lurantis_heal_punish (14%) |
| 38 | `darkness_mill_hand_lock` | **39.6%** | 36.0% | 9/44 | selective_bloom_cradily (100%) | lurantis_heal_punish (6%) |
| 39 | `meta_festival_lead` | **37.8%** | 35.5% | 7/44 | selective_bloom_cradily (100%) | orthworm_ex_metal_retaliation (14%) |
| 40 | `salazzle_ex_team_rockets_muk_condition_stack` | **35.7%** | 34.0% | 6/44 | selective_bloom_cradily (99%) | team_rockets_persian_ex_attack_theft (15%) |
| 41 | `static_venom_drapion` | **31.0%** | 25.5% | 5/44 | selective_bloom_cradily (99%) | lurantis_heal_punish (11%) |
| 42 | `team_rockets_wobbuffet_orbeetle_damage_launder` | **27.1%** | 22.8% | 4/44 | selective_bloom_cradily (100%) | lurantis_heal_punish (5%) |
| 43 | `feraligatr_munkidori_damage_transfer` | **20.3%** | 15.2% | 2/44 | selective_bloom_cradily (98%) | panic_poison_paralysis (5%) |
| 44 | `meta_ns_zoroark` | **14.8%** | 10.2% | 1/44 | selective_bloom_cradily (100%) | dhelmise_veluza_hide_n_sneak (4%) |
| 45 | `selective_bloom_cradily` | **0.3%** | 0.0% | 0/44 | chandelure_centiskorch_deck_out (2%) | arbok_muk_laser_darkbell (0%) |

## Full matrix

Row's win rate against column.

| |lurantis_heal_|panic_poison_p|team_rockets_p|krookodile_ex_|scovillain_sal|meta_raging_bo|meta_mega_exca|toxic_slumber_|arbok_muk_lase|heracross_sini|kyurem_vanillu|arbok_muk_trol|mega_chandelur|meta_dragapult|metal_metang_e|team_rockets_k|arbok_team_roc|mega_lopunny_d|dhelmise_veluz|water_aggro|tr_crobat_abso|decidueye_ex_j|kangaskhan_tyr|orthworm_ex_me|meta_dragapult|mega_scrafty_e|stevens_carbin|ns_zoroark_nig|meta_dragapult|eerie_inferno_|veluza_sinistc|hops_snorlax_s|chandelure_cen|team_rockets_s|meta_slowking|crabominable_v|tr_arbok_yvelt|darkness_mill_|meta_festival_|salazzle_ex_te|static_venom_d|team_rockets_w|feraligatr_mun|meta_ns_zoroar|selective_bloo|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **lurantis_heal_** |—|51|50|72|46|54|53|68|74|58|62|77|60|62|57|81|80|60|78|69|86|81|65|71|64|87|64|65|69|71|68|82|86|84|70|74|86|94|84|81|89|95|95|91|100|
| **panic_poison_p** |49|—|49|54|58|60|62|58|70|71|64|72|73|56|69|78|68|66|66|66|67|76|69|74|64|66|72|62|70|73|77|84|73|80|82|74|86|88|60|84|86|90|95|91|100|
| **team_rockets_p** |50|51|—|60|62|56|56|66|58|60|69|62|58|68|64|68|64|61|70|67|62|84|76|77|62|70|66|64|72|74|73|80|86|80|83|79|74|87|79|85|84|94|94|92|100|
| **krookodile_ex_** |28|46|40|—|51|39|56|47|66|44|64|68|65|59|62|69|66|60|73|60|63|38|63|72|64|63|72|58|63|72|59|74|74|62|59|71|74|76|66|82|76|87|88|92|100|
| **scovillain_sal** |54|42|38|49|—|53|64|66|58|73|37|58|41|58|72|66|66|60|58|46|66|58|52|88|66|70|74|64|64|58|64|69|39|76|64|54|73|72|58|76|82|88|78|94|100|
| **meta_raging_bo** |46|40|44|61|47|—|60|64|38|56|58|40|60|56|62|53|44|66|62|60|61|55|60|67|65|72|56|56|64|58|64|70|64|74|64|68|75|70|78|65|86|75|77|93|100|
| **meta_mega_exca** |47|38|44|44|36|40|—|62|48|59|75|50|38|58|60|54|62|67|52|72|54|60|55|61|54|62|53|64|66|56|70|68|46|68|70|73|80|70|79|62|77|78|78|89|100|
| **toxic_slumber_** |32|42|34|53|34|36|38|—|67|64|56|68|38|54|46|76|68|52|70|62|64|48|48|66|54|71|63|62|57|42|62|72|55|56|55|66|76|78|60|72|75|87|94|83|100|
| **arbok_muk_lase** |26|30|42|34|42|62|52|33|—|52|41|58|68|52|61|45|53|59|56|56|56|58|70|64|56|48|62|61|58|62|64|68|66|73|74|63|69|70|54|79|75|91|94|95|100|
| **heracross_sini** |42|29|40|56|27|44|41|36|48|—|53|52|48|51|47|61|60|60|56|68|66|53|61|57|44|74|54|59|61|51|64|68|50|73|62|67|64|84|72|72|81|87|90|92|100|
| **kyurem_vanillu** |38|36|31|36|63|42|25|44|59|47|—|56|44|46|26|57|61|50|54|58|54|45|44|49|61|55|46|54|59|69|63|66|70|70|62|71|77|70|76|82|76|88|93|88|100|
| **arbok_muk_trol** |23|28|38|32|42|60|50|32|42|48|44|—|62|52|50|48|50|54|46|60|52|55|66|62|57|41|60|66|55|64|61|66|51|74|72|65|62|69|54|79|74|92|94|92|100|
| **mega_chandelur** |40|27|42|35|59|40|62|62|32|52|56|38|—|47|62|48|34|46|58|60|38|74|62|62|54|48|57|40|50|59|64|64|68|58|57|72|64|62|64|70|62|78|88|82|100|
| **meta_dragapult** |38|44|32|41|42|44|42|46|48|49|54|48|53|—|49|55|52|52|46|52|50|58|45|52|59|51|52|58|56|62|58|54|64|66|54|66|70|60|72|66|84|76|78|90|100|
| **metal_metang_e** |43|31|36|38|28|38|40|54|39|53|74|50|38|51|—|41|49|58|52|62|56|49|46|58|46|57|48|44|62|47|60|64|42|70|55|68|72|62|78|62|83|78|78|90|100|
| **team_rockets_k** |19|22|32|31|34|47|46|24|55|39|43|52|52|45|59|—|50|46|60|56|45|56|55|46|50|46|58|52|48|52|70|63|64|70|64|62|68|64|64|71|84|86|91|90|100|
| **arbok_team_roc** |20|32|36|34|34|56|38|32|47|40|39|50|66|48|51|50|—|56|43|47|43|62|57|54|48|51|52|65|50|56|60|59|55|66|64|58|55|68|48|78|77|91|94|92|100|
| **mega_lopunny_d** |40|34|39|40|40|34|33|48|41|40|50|46|54|48|42|54|44|—|58|55|50|52|46|62|45|53|54|38|53|60|50|58|77|60|54|58|76|68|73|63|76|79|85|72|100|
| **dhelmise_veluz** |22|34|30|27|42|38|48|30|44|44|46|54|42|54|48|40|57|42|—|47|48|52|53|45|52|50|50|60|50|58|68|52|62|62|71|68|50|56|80|74|74|79|86|96|100|
| **water_aggro** |31|34|33|40|54|40|28|38|44|32|42|40|40|48|38|44|53|45|53|—|47|50|44|50|50|57|53|42|52|76|52|57|84|62|52|62|70|66|71|75|74|80|95|88|100|
| **tr_crobat_abso** |14|33|38|37|34|39|46|36|44|34|46|48|62|50|44|55|57|50|52|53|—|42|60|50|61|49|52|52|52|49|48|56|64|58|70|58|51|64|61|74|76|83|86|90|100|
| **decidueye_ex_j** |19|24|16|62|42|45|40|52|42|47|55|45|26|42|51|44|38|48|48|50|58|—|69|57|38|69|54|58|42|46|54|67|54|52|60|67|44|72|60|71|74|82|90|90|98|
| **kangaskhan_tyr** |35|31|24|37|48|40|45|52|30|39|56|34|38|55|54|45|43|54|47|56|40|31|—|64|54|52|56|46|59|48|58|66|38|54|58|70|56|52|66|62|76|68|80|91|100|
| **orthworm_ex_me** |29|26|23|28|12|33|39|34|36|43|51|38|38|48|42|54|46|38|55|50|50|43|36|—|50|45|55|40|59|48|64|74|68|70|50|58|84|67|86|62|72|88|84|86|100|
| **meta_dragapult** |36|36|38|36|34|35|46|46|44|56|39|43|46|41|54|50|52|55|48|50|39|62|46|50|—|52|38|42|54|53|44|52|58|66|50|52|65|63|66|52|74|73|78|82|100|
| **mega_scrafty_e** |13|34|30|37|30|28|38|29|52|26|45|59|52|49|43|54|49|47|50|43|51|31|48|55|48|—|57|40|56|58|40|71|70|50|56|64|60|52|65|78|70|86|80|93|100|
| **stevens_carbin** |36|28|34|28|26|44|47|37|38|46|54|40|43|48|52|42|48|46|50|47|48|46|44|45|62|43|—|62|56|34|59|56|36|70|68|62|50|52|82|66|65|73|77|93|100|
| **ns_zoroark_nig** |35|38|36|42|36|44|36|38|39|41|46|34|60|42|56|48|35|62|40|58|48|42|54|60|58|60|38|—|58|53|48|46|45|47|70|59|45|66|59|44|76|60|62|75|100|
| **meta_dragapult** |31|30|28|37|36|36|34|43|42|39|41|45|50|44|38|52|50|47|50|48|48|58|41|41|46|44|44|42|—|58|46|46|54|62|41|52|62|58|68|64|70|76|82|84|100|
| **eerie_inferno_** |29|27|26|28|42|42|44|58|38|49|31|36|41|38|53|48|44|40|42|24|51|54|52|52|47|42|66|47|42|—|38|51|48|54|58|52|57|67|56|73|66|68|85|90|100|
| **veluza_sinistc** |32|23|27|41|36|36|30|38|36|36|37|39|36|42|40|30|40|50|32|48|52|46|42|36|56|60|41|52|54|62|—|41|54|50|51|51|54|73|78|56|72|75|86|92|100|
| **hops_snorlax_s** |18|16|20|26|31|30|32|28|32|32|34|34|36|46|36|37|41|42|48|43|44|33|34|26|48|29|44|54|54|49|59|—|58|50|48|56|64|50|72|68|68|75|94|94|100|
| **chandelure_cen** |14|27|14|26|61|36|54|45|34|50|30|49|32|36|58|36|45|23|38|16|36|46|62|32|42|30|64|55|46|52|46|42|—|36|68|48|32|23|54|72|57|61|74|86|98|
| **team_rockets_s** |16|20|20|38|24|26|32|44|27|27|30|26|42|34|30|30|34|40|38|38|42|48|46|30|34|50|30|53|38|46|50|50|64|—|54|57|58|72|54|58|68|74|84|93|100|
| **meta_slowking** |30|18|17|41|36|36|30|45|26|38|38|28|43|46|45|36|36|46|29|48|30|40|42|50|50|44|32|30|59|42|49|52|32|46|—|53|60|58|57|45|74|64|62|80|100|
| **crabominable_v** |26|26|21|29|46|32|27|34|37|33|29|35|28|34|32|38|42|42|32|38|42|33|30|42|48|36|38|41|48|48|49|44|52|43|47|—|46|60|80|66|72|64|78|94|100|
| **tr_arbok_yvelt** |14|14|26|26|27|25|20|24|31|36|23|38|36|30|28|32|45|24|50|30|49|56|44|16|35|40|50|55|38|43|46|36|68|42|40|54|—|48|64|64|59|76|90|84|100|
| **darkness_mill_** |6|12|13|24|28|30|30|22|30|16|30|31|38|40|38|36|32|32|44|34|36|28|48|33|37|48|48|34|42|33|27|50|77|28|42|40|52|—|39|66|51|60|86|74|100|
| **meta_festival_** |16|40|21|34|42|22|21|40|46|28|24|46|36|28|22|36|52|27|20|29|39|40|34|14|34|35|18|41|32|44|22|28|46|46|43|20|36|61|—|47|61|54|62|78|100|
| **salazzle_ex_te** |19|16|15|18|24|35|38|28|21|28|18|21|30|34|38|29|22|37|26|25|26|29|38|38|48|22|34|56|36|27|44|32|28|42|55|34|36|34|53|—|46|46|57|89|99|
| **static_venom_d** |11|14|16|24|18|14|23|25|25|19|24|26|38|16|17|16|23|24|26|26|24|26|24|28|26|30|35|24|30|34|28|32|43|32|26|28|41|49|39|54|—|65|64|59|99|
| **team_rockets_w** |5|10|6|13|12|25|22|13|9|13|12|8|22|24|22|14|9|21|21|20|17|18|32|12|27|14|27|40|24|32|25|25|39|26|36|36|24|40|46|54|35|—|80|82|100|
| **feraligatr_mun** |5|5|6|12|22|23|22|6|6|10|7|6|12|22|22|9|6|15|14|5|14|10|20|16|22|20|23|38|18|15|14|6|26|16|38|22|10|14|38|43|36|20|—|80|98|
| **meta_ns_zoroar** |9|9|8|8|6|7|11|17|5|8|12|8|18|10|10|10|8|28|4|12|10|10|9|14|18|7|7|25|16|10|8|6|14|7|20|6|16|26|22|11|41|18|20|—|100|
| **selective_bloo** |0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|0|2|0|0|0|0|0|0|0|0|0|0|2|0|0|0|0|0|0|1|1|0|2|0|—|
