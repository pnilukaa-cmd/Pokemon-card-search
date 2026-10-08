## The Team Rocket's Trainers that make the family work

- **Team Rocket's Proton**: 3 Basic Team Rocket's Pokémon, playable on turn 1 going first.
- **Team Rocket's Ariana**: draw to 5, or **to 8 if every Pokémon you have in play is Team Rocket's**. This is why the best lists stay pure.
- **Team Rocket's Energy**: 2 Energy in any mix of Psychic and Darkness, Team Rocket's Pokémon only. It pays DD, PP, and the Colorless part of every cost.
- **Team Rocket's Petrel / Transceiver / Factory**: any Trainer, a Team Rocket Supporter, and draw 2 after one. These feed Kangaskhan ex's +100, Honchkrow and Porygon-Z.
- **Team Rocket's Giovanni**: switch your Active Team Rocket's Pokémon with a Benched one, *then* gust.
- **Team Rocket's Archer**: only after one of your Team Rocket's Pokémon was Knocked Out. Both hands are shuffled in; you draw 5, they draw 3.
- **Team Rocket's Great Ball**: heads finds an Evolution Team Rocket's Pokémon, tails a Basic one. **Venture Bomb**: heads puts 2 counters on them, tails 2 on your own Active.

## What the simulator was getting wrong (fixed in this study)

Every Team Rocket's card was checked against its printed text on a real
board. Each fix below has a regression test that fails on the commit before it.

- **Prize cards never reached the hand** after an attack, Checkup or
  retaliation Knock Out; only the Bench sweep moved them. Every deck in the
  field was affected, which is why the whole field was rerun.
- **"Whenever your opponent ..." Abilities never fired**: Dugtrio's Holes,
  Ampharos's Darkest Impulse, Gengar ex's Gnawing Curse, Magcargo, Mismagius ex.
- **Checkup Abilities never ran**: Tyranitar's Sand Stream, Froslass, Snorlax's
  Good Sleep. Bench Knock Outs at Checkup are now resolved.
- **Tainted Horn** put its 80 on Nidoking ex itself. Poison now carries its own
  counter count; Crobat's Poison Fang and Mega Dragalge ex had the same bug.
- **Love Impact** read "a Nidoking on your Bench" as Nidoqueen being Benched,
  so it never paid +120. The same bug hit Mightyena, Volbeat and Durant.
- **Evil Incineration** was a 3-Prize Knock Out with or without Team Rocket's
  Energy; it is now a paid discard with no Prize.
- **"Flip 2 coins. If both of them are tails"** resolved 75% of the time
  (Raticate's self-damage, Bewear, Miltank, Bombirdier, Energy Coin).
- **Searches**: "an Item card" looked for a name containing "n" (Procurement
  ×3, Hilda, Dragonair, Great Ball). Stage filters were never read.
  Transceiver fetched any Supporter. Archer and Unfair Stamp kept your hand.
- **Hypno, Sneasel, Giovanni, Torment, Rocket Mirror, Dark Awakening**: each
  now resolves as printed.
- **Pilot:** Orbeetle's Rocket Brain is aimed at a counter-scaling attacker:
  +6.0 for Orbeetle / Morpeko ex, +3.6 for Wobbuffet / Orbeetle.

## What did not work

| Tried | Result (200-game screen) |
|---|---|
| Houndoom (Burn + Confuse) into Muk's Hazardous Venom | 38.0%: the conditions come off before Muk can swing |
| Porygon-Z alongside Honchkrow | 64.8% vs 70.7% without it |
| Exeggutor's self-damage as Rocket Brain fuel | 56.7% vs 60.8% without it |
| Standalone Ampharos / Zapdos | 52.3%; Ampharos works better as a tax in Raticate (65.1%) |
| Petrel choosing the most useful Trainer (pilot) | −1.5 on Persian ex; removed |

The 200-game screens, drafts and paired comparisons are in
`runs/2026-10-08/team_rocket_screens/`.
