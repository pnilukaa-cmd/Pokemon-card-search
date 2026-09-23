# Field results -- 1000 games per pairing, 45 decks, 990 pairings

990,000 games. 95% CI on each deck's mean: +/-0.47 points.

Measured on the engine as of this branch, after seven correctness fixes
and the card-database memoisation (verified bit-identical on 200 seeds).
The previous 200-game run of the same field moved no deck by more than
0.92 points, so the ranking is stable at both sample sizes.

| rank | deck | mean | median | winning |
|-----:|------|-----:|-------:|--------:|
| 1 | `lurantis_heal_punish` | 73.00 | 72.3 | 42/44 |
| 2 | `team_rockets_persian_ex_attack_theft` | 71.97 | 71.2 | 44/44 |
| 3 | `panic_poison_paralysis` | 69.12 | 68.4 | 40/44 |
| 4 | `scovillain_salazzle_spicy_rage` | 64.55 | 64.5 | 37/44 |
| 5 | `krookodile_ex_relicanth_hand_disruption` | 63.44 | 64.9 | 37/44 |
| 6 | `meta_raging_bolt` | 62.77 | 61.5 | 37/44 |
| 7 | `toxic_slumber_vileplume_ex` | 60.86 | 60.2 | 34/44 |
| 8 | `heracross_sinistcha_tea` | 60.80 | 60.0 | 34/44 |
| 9 | `meta_mega_excadrill` | 60.65 | 58.9 | 35/44 |
| 10 | `arbok_muk_laser_darkbell` | 59.01 | 58.4 | 32/44 |
| 11 | `arbok_muk_trolley_darkbell` | 57.19 | 55.8 | 30/44 |
| 12 | `kyurem_vanilluxe_blizzard` | 57.10 | 54.8 | 27/44 |
| 13 | `mega_chandelure_ex_retreat_tax` | 56.73 | 56.7 | 31/44 |
| 14 | `meta_dragapult_pure` | 55.41 | 52.4 | 28/44 |
| 15 | `metal_metang_excadrill` | 55.31 | 51.0 | 25/44 |
| 16 | `decidueye_ex_judge_sniper_lock` | 55.22 | 53.5 | 27/44 |
| 17 | `arbok_team_rockets_muk_condition_stack` | 55.01 | 52.6 | 29/44 |
| 18 | `dhelmise_veluza_hide_n_sneak` | 54.89 | 50.5 | 23/44 |
| 19 | `water_aggro` | 54.46 | 49.7 | 22/44 |
| 20 | `mega_lopunny_dusknoir_snipe_finisher` | 54.45 | 50.8 | 25/44 |
| 21 | `team_rockets_koffing_weezing_bench_swarm` | 54.10 | 51.8 | 28/44 |
| 22 | `tr_crobat_absol_bench_snipe` | 53.11 | 52.0 | 26/44 |
| 23 | `kangaskhan_tyrantrum_flip_mill` | 53.00 | 52.0 | 23/44 |
| 24 | `orthworm_ex_metal_retaliation` | 52.55 | 49.6 | 22/44 |
| 25 | `mega_scrafty_ex_darkness_tank` | 52.53 | 52.5 | 26/44 |
| 26 | `meta_dragapult_blaziken` | 52.30 | 49.1 | 19/44 |
| 27 | `stevens_carbink_damage_wall` | 51.85 | 49.7 | 21/44 |
| 28 | `ns_zoroark_night_joker_toolbox` | 50.82 | 49.2 | 19/44 |
| 29 | `meta_dragapult_dusknoir` | 50.01 | 46.4 | 15/44 |
| 30 | `eerie_inferno_ninetales_burn` | 49.40 | 48.0 | 19/44 |
| 31 | `veluza_sinistcha_ex_tea_service` | 49.27 | 46.1 | 17/44 |
| 32 | `chandelure_centiskorch_deck_out` | 46.58 | 44.0 | 15/44 |
| 33 | `hops_snorlax_stacked_buff` | 46.20 | 40.8 | 15/44 |
| 34 | `meta_slowking` | 45.75 | 44.8 | 14/44 |
| 35 | `crabominable_veluza_food_prep` | 45.10 | 41.2 | 11/44 |
| 36 | `team_rockets_spidops_swarm` | 44.81 | 40.0 | 13/44 |
| 37 | `tr_arbok_yveltal_snow_coating` | 44.28 | 43.6 | 14/44 |
| 38 | `darkness_mill_hand_lock` | 39.53 | 34.9 | 7/44 |
| 39 | `meta_festival_lead` | 37.75 | 34.6 | 7/44 |
| 40 | `salazzle_ex_team_rockets_muk_condition_stack` | 35.02 | 29.8 | 6/44 |
| 41 | `static_venom_drapion` | 31.20 | 26.8 | 5/44 |
| 42 | `team_rockets_wobbuffet_orbeetle_damage_launder` | 26.71 | 22.3 | 3/44 |
| 43 | `feraligatr_munkidori_damage_transfer` | 21.05 | 17.4 | 2/44 |
| 44 | `meta_ns_zoroark` | 14.67 | 10.8 | 1/44 |
| 45 | `selective_bloom_cradily` | 0.45 | 0.3 | 0/44 |
