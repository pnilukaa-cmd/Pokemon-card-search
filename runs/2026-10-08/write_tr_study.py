"""Write decks/TEAM_ROCKET_STUDY_2026-10-08.md from the field run summary.

Every Team Rocket's line, its best measured home and how to play it. Win
rates come from runs/2026-10-08/field_summary.json (full round robin, 1000
games per pairing); the 200-game screens are quoted where noted.
"""
import json, os
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
S = json.load(open(os.path.join(REPO, "runs/2026-10-08/field_summary.json")))
summ = S["summary"]
order = sorted(summ, key=lambda n: -summ[n]["mean"])
rank = {n: i + 1 for i, n in enumerate(order)}
N = len(order)

def r(slug):
    s = summ[slug]
    return f"**{s['mean']:.1f}%** (rank {rank[slug]}/{N}, {s['winning']}/{s['played']} winning)"

def link(slug):
    md = os.path.join(REPO, "decks", slug + ".md")
    return f"[`{slug}`]({slug}.md)" if os.path.exists(md) else f"`{slug}`"

# line -> (best home deck, how the line plays, other homes)
LINES = [
 ("Rattata → Raticate", "team_rocket_raticate_rush",
  "90 for one Energy of any type on a one-Prize Stage 1; Maximum Belt makes it 140 into an ex, Backtrack Badge re-flips its two-tails self-Knock Out, Mist Energy makes it immune to placed counters (Alakazam). Trade one Prize for two every turn.", []),
 ("Nidoran♀ → Nidorina → Nidoqueen", "team_rocket_nidoking_nidoqueen",
  "Love Impact: 180 for a single Darkness Energy while any Nidoking is on the Bench. Rare Candy or Nidorina's Dark Awakening gets it out on turn 2-3.", []),
 ("Nidoran♂ → Nidorino → Nidoking ex", "team_rocket_nidoking_nidoqueen",
  "The 330-HP Bench enabler for Nidoqueen, and the backup: Tainted Horn Poisons for 8 counters a Checkup, Kingly Impact 240.", []),
 ("Meowth → Persian ex", "team_rockets_persian_ex_attack_theft",
  "Haughty Order borrows an attack from the top 10 of the opponent's deck; Cruel Slash 140 + Confusion when the reveal misses.", ["team_rocket_raticate_rush"]),
 ("Kangaskhan ex", "team_rocket_honchkrow_kangaskhan",
  "Wicked Impact 220 on any turn you played a Team Rocket Supporter. The best Basic in the family; it slots into every Team Rocket's Supporter shell.", ["team_rocket_raticate_rush", "team_rockets_persian_ex_attack_theft"]),
 ("Murkrow → Honchkrow", "team_rocket_honchkrow_kangaskhan",
  "Rocket Feathers cashes Team Rocket Supporters you can't play this turn at 60 each; Murkrow's Deceit searches a Supporter.", []),
 ("Porygon → Porygon2 → Porygon-Z", "team_rocket_porygon_z_kangaskhan",
  "R Command: 20 per Team Rocket Supporter in your discard; Reconstitute bins spare cards. Slower than Honchkrow, which cashes the same cards from hand.", []),
 ("Tarountula → Spidops", "tr_spidops_mewtwo_hammer",
  "Rocket Rush: 30 per Team Rocket's Pokémon in play; Charging Up re-attaches Basic Energy from the discard every turn.", ["team_rockets_spidops_swarm"]),
 ("Mewtwo ex", "tr_spidops_mewtwo_hammer",
  "Erasure Ball 160 + 60 per Benched Energy discarded (280), but only with 4+ Team Rocket's Pokémon in play — easy in an all-Team Rocket's deck.", ["team_rocket_hypno_wobbuffet"]),
 ("Articuno", "tr_spidops_mewtwo_hammer",
  "Repelling Veil shields your Basic Team Rocket's Pokémon from attack effects; Dark Frost 120 with Team Rocket's Energy. A support Basic.", []),
 ("Mimikyu", "tr_spidops_mewtwo_hammer",
  "Gemstone Mimicry copies an opposing Tera Pokémon's attack; zero Retreat Cost pivot.", ["team_rocket_hypno_wobbuffet"]),
 ("Koffing → Weezing", "team_rockets_koffing_weezing_bench_swarm",
  "Explode Together Now: 40 per Koffing/Weezing in play (both sides); Smog Signals benches more Koffing when hit.", []),
 ("Grimer → Muk", "panic_poison_paralysis",
  "Hazardous Venom: 100 per Special Condition on their Active. Best fed by the other Arbok's Panic Poison (three conditions → 300); Gooped Up locks retreat.", ["arbok_team_rockets_muk_condition_stack"]),
 ("Ekans → Arbok", "team_rockets_persian_ex_attack_theft",
  "Potent Glare (while Active) stops the opponent playing Ability Pokémon from hand; Spinning Tail 30 to each. Works as a lock piece, not an attacker.", ["arbok_team_rockets_muk_condition_stack", "tr_arbok_yveltal_snow_coating"]),
 ("Zubat → Golbat → Crobat ex", "golbat_brute_bonnet_punch",
  "Free counters when they evolve (Sneaky Bite 2, Biting Spree 2+2) cashed by Brute Bonnet's 50 + 50 per counter.", ["tr_crobat_absol_bench_snipe"]),
 ("Larvitar → Pupitar → Tyranitar", "team_rocket_tyranitar_sandstorm",
  "Sand Stream: 2 counters on every opposing Basic at every Checkup while Active (40 a round); Demolition Tackle 180.", []),
 ("Diglett → Dugtrio", "team_rocket_tyranitar_sandstorm",
  "Holes: 2 counters whenever their Active retreats or switches out on their turn. Removing it from the Tyranitar deck cost 1.9 points.", []),
 ("Sneasel", "team_rocket_tyranitar_sandstorm",
  "Strike the Sleeper: 20 per counter on one Benched Pokémon — the finisher for any counter-spreading deck.", []),
 ("Moltres ex", "team_rocket_moltres_houndoom",
  "Evil Incineration discards their Active and everything on it (no Prize, costs a Team Rocket's Energy); Flame Screen 110 and -50 next turn.", []),
 ("Houndour → Houndoom", "team_rocket_moltres_houndoom",
  "Scorching Fire 120 for two Energy; Cruel Coal Burns and Confuses for one.", []),
 ("Blipbug → Dottler → Orbeetle", "team_rocket_orbeetle_morpeko",
  "Rocket Brain moves counters off Team Rocket's Pokémon onto Morpeko ex (40 + 40 per counter on itself).", ["team_rockets_wobbuffet_orbeetle_damage_launder"]),
 ("Drowzee → Hypno", "team_rocket_hypno_wobbuffet",
  "Bench Manipulation: 80 per tails, one coin per opposing Benched Pokémon, ignores Weakness — about 200 into a full Bench.", ["team_rocket_hypno_exeggutor"]),
 ("Wobbuffet", "team_rocket_hypno_wobbuffet",
  "Rocket Mirror throws every counter on a Benched Team Rocket's Pokémon at their Active.", ["team_rockets_wobbuffet_orbeetle_damage_launder"]),
 ("Exeggcute → Exeggutor", "team_rocket_hypno_exeggutor",
  "Double-Edge 150 (30 to itself); Tri Kinesis Knocks Out anything on three heads (12.5%). The weakest evolution line here.", []),
 ("Mareep → Flaaffy → Ampharos", "team_rocket_raticate_ampharos",
  "Darkest Impulse: 4 counters on every Pokémon the opponent evolves from hand — needs no Energy, so it taxes from the Bench. Standalone (Head Bolt 140 + Zapdos) measured 52%.", []),
 ("Zapdos", None,
  "Wicked Thunder 120 with Team Rocket's Energy; Jamming Wing moves an Energy off their Active. Only in the standalone Ampharos list (`team_rocket_ampharos_zapdos.ptcgl.txt`, 52% in the 200-game screen).", []),
 ("Chingling", "team_rockets_persian_ex_attack_theft",
  "Chiming Commotion discards a random card from their hand for no Energy; 0 Retreat. A turn-1 nuisance in Supporter shells.", ["team_rocket_hypno_wobbuffet"]),
]

tr_decks = [n for n in order if n.startswith(("team_rocket", "tr_", "team_rockets"))
            or n in ("golbat_brute_bonnet_punch", "panic_poison_paralysis",
                     "arbok_team_rockets_muk_condition_stack",
                     "salazzle_ex_team_rockets_muk_condition_stack",
                     "arbok_muk_laser_darkbell", "arbok_muk_trolley_darkbell")]

out = [f"# Team Rocket's study — every line, a deck for each\n",
       f"All {len(LINES)} Team Rocket's Pokémon lines in the Standard pool (52 cards), each with its best measured home.",
       f"Win rates are from the full round robin of {S['stamp']} — **{N} decks, {S['games']} games per pairing**, every deck against every other on the same engine (see [FIELD_RESULTS.md](FIELD_RESULTS.md)).\n",
       "## Team Rocket decks, ranked\n",
       "| Field rank | Deck | Mean | Winning matchups | Worst matchup |", "|---|---|---|---|---|"]
for n in tr_decks:
    s = summ[n]
    worst = s["worst"] if not isinstance(s["worst"], str) else eval(s["worst"])
    out.append(f"| {rank[n]} | {link(n)} | {s['mean']:.1f}% | {s['winning']}/{s['played']} | {worst[0]} {worst[1]:.0f}% |")
out += ["", "## Every line and where it plays best\n",
        "| Line | Best home | How it plays | Also in |", "|---|---|---|---|"]
for line, home, how, also in LINES:
    h = f"{link(home)} {r(home)}" if home else "—"
    a = ", ".join(link(x) for x in also) or ""
    out.append(f"| **{line}** | {h} | {how} | {a} |")
out.append("")
out.append(open(os.path.join(REPO, "runs/2026-10-08/tr_study_body.md")).read())
open(os.path.join(REPO, "decks", "TEAM_ROCKET_STUDY_2026-10-08.md"), "w").write("\n".join(out) + "\n")
print("wrote decks/TEAM_ROCKET_STUDY_2026-10-08.md")
