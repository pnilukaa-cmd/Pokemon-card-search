# Session context — Pokémon TCG Standard simulator

## Session 2 (2026-09-23 / 24), branch `claude/code-restructuring-yo2673`

Read this section first; section 1 onward is the previous session.

**Standing instructions added this session**
- Treat 30th Celebration (`30C`) as legal.
- When handed a real decklist: study it, teach the AI to play it, and keep
  learning and improving (method: `.claude/skills/tcg-theorycraft/SKILL.md`
  section 11e).
- **Always extend or enhance the programming. Pause only when nothing is
  left to fix or improve other than the deck rerun.**
- Still in force: check every deck-building rule, always print the PTCGL
  import, exact `SET NUM` on every line (Basic Energy excepted), 1000-trial
  baseline on every finished list, real measurements, pause before a new
  full run.

**Field.** 54 decks in `decks/field/` (`paralysis_ctl` and
`selective_bloom_cradily` dropped). The 2026-09-23 round robin
(`runs/2026-09-23/`, `decks/FIELD_RESULTS.md`) is **superseded** by every
engine fix since; a full rerun is the one open item.

**New decks studied:** `decks/dudunsparce_maushold_mill_wall.*` (a
tournament winner) and `decks/mew_ex_baby_lock.*`.

**Engine bugs fixed this session** (each has a regression test proven to
fail on the commit before it): hand-reset draws (Lillie's Determination in
46 decks, Lacey, Carmine) dropped their first half; optional draws had no
deck floor; "next turn" locks never expired; Pecharunt ex's Subjugating
Chains poisoned the opponent instead of switching; Neutralization Zone /
Battle Cage never played; Bench damage never checked against prevention
(Shaymin); Fan Call never fired; search type filters ignored; Nighttime
Mine never played; the inert-card guard passed dead Stadiums; energy /
energy_names drifted (crashed every run with Enhanced Hammer); discard
recovery returned Pokemon whatever the card said; Tool Scrapper, Accompanying
Flute; "can't use attacks" locks (16 cards) did nothing; "only if you have
X in play" requirements dropped (Glass Trumpet); attached Energy with no
named type provided every type; Eri's discard dropped; Lisia's Appeal,
Drasna, Mr. Mime miscompiled.

**Later in session 2 (2026-09-24).** Each with a regression test that
fails on the commit before it:
- *Triggers.* `on_play` Abilities fire when a Pokemon is benched from hand
  (Meowth ex's Last-Ditch Catch, which had also compiled as a self-lock;
  Iron Leaves ex's Rapid Vernier, taken only when the moved Energy pays for
  a better attack; Chien-Pao's Snow Sink, opponent's Stadium only).
  `on_damaged` runs more than counters (Incandescent Body, Smog Signals).
  Prize modifiers read their own wording (Mega Gengar ex's Shadowy
  Concealment cut every Prize). "that have X in their name" Bench searches
  keep the name (Roto Call, Smog Signals). Tri Kinesis compiles.
- *Deck orientation.* `deck[-1]` is the top. Seek Inspiration read the
  bottom and never discarded the card; it now reads and discards the top.
  Academy at Night (was never played) and Ciphermaniac's Codebreaking set
  up the copy target. The pilot heuristics for this were measured at
  -0.92 +/- 0.82 and reworked (Academy used just before the attack); the
  rework is under measurement.
- *Card conservation* (`audit_conservation.py`, standing test): Knock Outs
  now discard Energy, Tool and the Evolution stack (`InPlay.under`);
  Stadium replacement; attack Bench searches; Run Away Draw no longer
  duplicates Dudunsparce (**the Dudunsparce wall's earlier numbers were
  inflated by this**); refunds; double-provision Energy.
- *Rules.* No Supporter on the first turn going first; no evolving on
  either player's first turn (Rare Candy, Grand Tree); Grand Tree chains to
  Stage 2; same-name Stadium; mulligan extra draws.
- *Pilot, measured.* Basics that reach the hand after the Supporter are
  benched that turn: +0.97 +/- 0.27 over 6 meta decks, now the default.
  The lookahead also chooses the promotion after a Knock Out (measuring).
- *Lookahead information leak.* The lookahead's copies kept the real
  deck order and the opponent's real hand, so it played against the actual
  future. Fixed (`_hide_information`); every earlier lookahead number is
  optimistic (Mew ex read 17.29 -> 43.91 with the leak).

**Pilot.** `policies.LOOKAHEAD` (`PILOT=lookahead` in `vs_field.py`): each
attack (and gust-attack target), Boss's Orders target and retreat choice is
played out through the opponent's reply. Greedy stays the default and is
bit-identical. Measured attack-only lookahead vs greedy: Mew ex +4.54,
Wugtrio +1.92, Dudunsparce +0.65, N's Zoroark -0.09.

**Tools.** `vs_field.py` (in repo), `run_phases` / `finish_turn` /
`lookahead_pick` in `simulate_versus.py`, `test_ability_engine.py` runs
under pytest honestly (`conftest.py`).

---

Branch `claude/pokemon-standard-cards-fetcher-mucwsu`, from `be14f9d` to `17c6142`.
Written as a handoff: what was asked, what was fixed, what was measured, what
is still open, and the methodology mistakes worth not repeating.

---

## 1. Standing instructions from the user

These persist across every request in this project:

- When asked for a deck, **check every deck-building rule**, even if it takes longer.
- **Always print the PTCGL import.**
- Every card line needs an exact `SET NUM` pair. Basic Energy is the exception
  and is written with no set code.
- **Run a 1000-trial baseline** on every finished decklist.
- Later addition: **do real measurements**, not reasoning presented as results.
- Later addition: **pause after fixing bugs, before launching a new run.**

---

## 2. What was asked, in order

1. Build a deck focused around **Paralysis to prevent retreating**.
2. Re-measure the decks that had been carrying an inert card.
3. Study five new mill decklists (Maushold, Drill Mill, Zweilous, Centiskorch, Flygon).
4. "Is there a way to devolve a Pokémon, like Flygon, so you can mill more?"
5. Make the simulator compile faster and more accurately; hand over the Lurantis import.
6. Keep fixing bugs and ensure they stay fixed; then a full rerun of all decks.

---

## 3. The deck that was asked for

`decks/wugtrio_paralysis_pin.ptcgl.txt`, written up in
`decks/wugtrio_paralysis_pin.md`.

**69.86% (±0.46) over all 45 field decks at 1000 games each, winning 41 of 45 —
rank 3**, behind `lurantis_heal_punish` (73.00) and
`team_rockets_persian_ex_attack_theft` (71.97).

The engine is `Wugtrio ex TEF 190`'s Numbing Hold: two Water for 120 damage plus
"the Defending Pokémon can't retreat", on a 250 HP Stage 1 that retreats for one.
The Paralysis flips (`Cryogonal SSP 47`, `Misty's Staryu DRI 46`, one Energy each)
deny the retreat AND the attack. Four `Boss's Orders` choose who gets stranded.

**Paralysis is worth +4.58 points** — 69.86 against 65.28 for the same 60 cards
with all six Paralysis cards swapped for their closest legal twins
(`Cryogonal BLK 111`, `Staryu POR 20`). SE on the difference 0.33, about 14 sigma.
It helped in 37 of 45 matchups, most against decks that need their Active to keep
doing a job (NS Zoroark +17.5, Arbok/Muk +15.5, Krookodile +15.0), and cost points
against decks that only ever attack from the Active (lurantis −4.0, dragapult −4.0).

**Cheap Paralysis beats guaranteed Paralysis.** The condition is cured at the end
of the opponent's next turn, so it buys one turn and must be re-applied every turn.
`Regice ex` (four Energy, discards two) measured 48.8 and `Weavile` (discards all
its Energy) 42.3, both at or BELOW a no-Paralysis control at 50.4, while the
one-Energy flips measured 57.7–59.4 on the same 8-deck sample.

---

## 4. Engine bugs found and fixed (19)

Seventeen of them are one shape: **a restriction the card prints was silently
dropped**. A dropped restriction never weakens a card — it makes it unconditional.

| # | Card / system | Bug | Reach |
|---|---|---|---|
| 1 | Paralysis | `try_retreat` never read `CANNOT_ATTACK`; a Paralyzed Pokémon walked away | every Paralysis card |
| 2 | Conditions | cleared on retreat/evolve only, not "leaves the Active Spot"; a gusted condition became permanent | all 3 switch executors |
| 3 | Accelerators | 55 effects double-emitted an attach | every accelerator |
| 4 | Accelerators | executor ignored `act.amount`; Punk Up put down 1 of 5 | same |
| 5 | Jumbo Ice Cream | "3 or more Energy attached" gate dropped | 1 card |
| 6 | Backtrack Badge | never attached; `query_reflip` and `_expected_heads` were unreachable, so every coin flip was a flat 50% | whole format |
| 7 | Buddy-Buddy Poffin | 70 HP cap dropped; fetched a 230 HP ex | 36 of 45 decks |
| 8 | Poké Pad | "doesn't have a Rule Box" dropped; tutored a Pokémon ex | 23 of 45 decks |
| 9 | Bastiodon | "2 or less Energy attached" dropped; benched Bastiodon was total board immunity | 2 cards |
| 10 | `attack_side_effects` | copy-attack chain had no depth guard; Slowking borrowed itself to 981 frames and killed a 45,000-game run | any deck with Slowking |
| 11 | Cyrano | "Pokémon ex" dropped; took three one-Prize support Pokémon | 6 decks |
| 12 | Ascension family | fell through to `search_any_card`; a universal tutor that also skipped the evolution | 9 cards |
| 13 | Crispin | "of different types" dropped; 2 Energy in a mono-Energy deck | 1 field deck |
| 14 | Binding Mochi | missing from `DAMAGE_TOOLS` | 1 deck |
| 15 | Hop's Choice Band | missing from `DAMAGE_TOOLS` | 1 deck |
| 16 | Repel | `FORCE_SWITCH_OPPONENT` not in `TRAINER_IR_OPS` | 1 deck |
| 17 | Iron Defender | `REDUCE_DAMAGE` is a passive op the Trainer path ignores | 1 deck |
| 18 | Lucky Helmet / Handheld Fan / TR's Hypnotizer | when-damaged Tools never attached, never fired | 4 decks |
| 19 | Poffin species guard | `endswith("pokemon")` too narrow; compiled to two Bench searches, benched 2 only by luck | 1 card |

Plus one performance fix: `run_game` called `load_cards()` and
`build_card_index()` **on every game**, re-parsing the 2000-card JSON 198,000
times in a round robin — 65% of runtime. Memoised: **19.5x faster
(67.0 → 3.4 ms/game), bit-identical on all 200 seeds.**

### Deliberately unmodelled

- `Academy at Night` — symmetric, no sensible heuristic for which card to put back
- `Future Booster Energy Capsule` — in no deck
- Hop's Choice Band's cost-reduction half — only its damage half is modelled
- Tera's bench-damage immunity — affects `Wugtrio ex`; conservative

---

## 5. The standing guard

`test_no_card_in_any_decklist_is_silently_inert` checks every Trainer in all 66
decklists against the path that actually CONSUMES it — named registry, Tool
tables, reflip path, Stadium turn effect, `TRAINER_IR_OPS` — and fails on
anything matching none of them, with a `KNOWN` allowlist carrying reasons.

**Its first version passed against the very engine that ignored Binding Mochi and
Hop's Choice Band**, because it accepted any card whose IR merely compiled. A
guard that cannot fail on the bug it was written for is the same
compiled-is-not-executed trap as everything else. Tightened to per-type
consumption, it immediately found four of the last six bugs.

---

## 6. Methodology — what went wrong and the rule that came out of it

**The Paralysis number was reported wrong four times: +9, +14.8, +2.1, then +4.72,
settling at +4.58.** Causes: an 8-deck hand-picked sample, and a "control" that
still ran 3 `Misty's Staryu` whose Bubble Beam is also a Paralysis flip — only 3
of the 6 Paralysis cards had been swapped. CRN pairing controls the dice, not
which opponents were picked. Once the control was matched and the sample was all
45 opponents, 200-game and 1000-game runs agreed to within 0.18.

**A regression test must be proven to fail on the unfixed code.** The copy-chain
test took five attempts: three were wrong theories about `Ethan's Sudowoodo`, and
the fourth built the board by hand and PASSED against the unfixed engine. The
culprit (Slowking) was found by instrumenting real nesting depth per opponent,
not by reasoning about which cards looked like they ought to loop.

**Hand-built test boards are a repeated source of false results.** Three separate
failures: reading damage after a KO had promoted a fresh Pokémon; passing an
empty card map to `compile_effects_for`, which compiles no Abilities and made
Bastiodon look inert rather than over-strong; and a string `damage` value that
crashed the damage path. Drive tests off `load_model` and real decks.

**Wrong predictions worth remembering.** The engine fixes were predicted to shake
up the field; the largest move across 45 decks was 0.92, because the fixes hit
every deck symmetrically. Centiskorch was predicted to move after the Bastiodon
fix; git timestamps showed the fix had landed 63 seconds before that run, so the
premise was false. `Iron Defender` was first wired into the Supporter chain and
fired 0 times in 40 games.

---

## 7. Measured results

**Field, 45 decks, 1000 games per pairing (`decks/FIELD_RESULTS.md`), ±0.47:**
rank 1 `lurantis_heal_punish` 73.00, 2 `team_rockets_persian_ex` 71.97 (the only
deck with no losing matchup, 44/44), 3 `panic_poison_paralysis` 69.12.

**Decks re-measured at 1000 games** — every one reproduced its 200-game figure
within noise, largest move 0.63:

    paralysis_pin     69.86     paralysis_ctl     65.28
    tauros            64.63     maushold_mill     58.60
    new_drillmill     56.51     new_zweilous      43.08
    new_maushold      36.50     new_flygon        23.24
    new_centiskorch   14.84

**The five mill decks (`decks/STUDY_MILL_DECKS.md`).** Mill is not a win condition
in this field: the best of them discards 7.28 cards a game against a ~53 card
requirement, and the ranking tracks damage, not mill rate. The engine is not at
fault — Gnaw Together was verified at exactly its printed rate over 2000 trials
(4 Maushold in play → 4.04 cards). Drill Mill works because `Relicanth`'s Memory
Dive gives `Mega Excadrill ex` a one-Energy Burrow alongside a 90-damage Undermine
and a 330-damage finisher on a 340 HP body.

**Devolve question: no.** `Strange Timepiece MEG 128` is the only card that
devolves your own Pokémon and it only targets Psychic; Flygon is Fighting. Even
with matching types it is +1 card milled per turn for one Item. Sandy Flapping
already self-loops — it fires on evolution and again when Flygon is Knocked Out.

---

## 8. Infrastructure

- Field decklists are committed under `decks/field/` (55 files). They previously
  lived only in the container scratchpad, where a restart nearly lost them.
- `roundrobin.py <field_dir> <out.json> <shard> <nshards> <games> rr1` — N×N.
- `vs_field.py` (scratchpad) — one candidate against a whole field.
- `simulate_baseline.py <deck> 1000` — development speed, no opponent.
- `deckcheck.validate(text)` — run before any measurement.
- Liveness: `ps -eo cmd | grep '[r]oundrobin.py'`, and check output mtimes.

---

## 9. Open items

1. **The full rerun is not started** — paused at the user's request. It would be
   55 decks, 1485 pairings, 1,485,000 games, ~20 min on 4 cores. This is a
   LARGER field than the 45-deck table, so results will not be directly
   comparable; every mean shifts because the opponent pool changed.
2. **Field composition undecided** — whether the 5 study mill decks, the 2
   Cradily builds and `paralysis_ctl` belong in the field proper. The control
   especially is a testing artifact, not a real deck.
3. **`selective_bloom_cradily`** cannot start a game. It self-excludes from the
   round robin. Deleting it changes every other deck's mean; left in place.
4. **`decks/pending_new_sets.md`** — 5 lists naming printings that do not resolve
   (`Sylveon ex MP 153`, `Greninja ex M6a 15`, `Gengar ex M6a 76`,
   `Salamence ex M6a 88`, `Umbreon ex MF 17`).
