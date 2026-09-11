# ns_zoroark — TCGplayer, September 2026

**Not my list.** From Natalie Millar's *The Best Pokémon TCG Decks Right
Now (September 2026)* on TCGplayer (2026-08-25), reproduced card-for-card.

The published lists give collector numbers without set codes, so every
line was resolved by number against this repo's pool. Basic Energy is
written without a set code, as everywhere else here.

`N's Zoroark ex`'s `Night Joker` copies a Benched N's Pokémon's attack --
usually `N's Zekrom` or `N's Darmanitan`. Note that
`check_energy_support` flags those two as uncastable and is right: they
are attack DONORS and never attack themselves.

**This deck's placement is a floor, not an evaluation, and I can say
exactly why.** Every card in it is now modelled -- `Transformation Tome`
(4 copies, the last unmodeled card here) resolves 49 times per 120 games
and `Secret Box` 198 -- and the placement barely moved when they went
live. The engine is copying the right attack: over 150 games against
`meta_dragapult_pure`, `Night Joker` fires 188 times and picks
`Rampaging Thunder` for 250. The problem is the other half of that
card's text. *"During your next turn, this Pokémon can't use attacks"*
is copied along with the damage, so `N's Zoroark ex` sits out the
following turn -- 76 skipped attack turns in those same 150 games. A
human alternates: `Shred` for 70 when no Knock Out is on offer,
`Rampaging Thunder` when one is. The greedy policy takes the bigger
number every time (halved in scoring for the lock, 125 vs 70, so it
still wins) and eats the lock. That is a pilot limitation, not a
modelling gap, and six measured attempts at a smarter pilot all came
back at no detectable difference.

## Decklist

```
Pokémon: 18
4 N's Zorua JTG 97
4 N's Zoroark ex JTG 98
2 N's Zekrom ASC 155
2 Munkidori PRE 44
1 N's Darumaka ASC 32
1 N's Darmanitan ASC 33
1 Pecharunt ex SFA 39
1 Meowth ex POR 62
1 Fezandipiti ex SFA 38
1 Yveltal MEG 88

Trainer: 34
4 Buddy-Buddy Poffin ASC 184
4 Lillie's Determination ASC 192
4 Transformation Tome CRI 83
3 Boss's Orders MEG 114
3 N's PP Up JTG 153
3 Ultra Ball ASC 213
2 Night Stretcher ASC 196
2 Binding Mochi PRE 95
2 Cyrano SSP 170
2 N's Castle JTG 152
1 Poké Pad ASC 198
1 Team Rocket's Venture Bomb DRI 179
1 Black Belt's Training ASC 255
1 Special Red Card CRI 82
1 Secret Box TWM 163

Energy: 8
8 Basic Darkness Energy

Total Cards: 60
```
