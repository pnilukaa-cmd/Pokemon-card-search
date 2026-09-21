# ns_zoroark — TCGplayer, September 2026

<!-- field-results -->
> ### Field results — 2026-09-21
> **14.8% mean · 10.2% median · 1 of 44 winning matchups · rank 44 of 45**
>
> Best `selective_bloom_cradily` 100% · worst `dhelmise_veluza_hide_n_sneak` 4%.
>
> Full round robin, 200 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates the Fossil-setup fix**: a Fossil is an Item and cannot be your opening Pokemon, so it no longer counts as a Basic for the opening hand.
<!-- field-results -->












**Not my list.** From Natalie Millar's *The Best Pokémon TCG Decks Right
Now (September 2026)* on TCGplayer (2026-08-25), reproduced card-for-card.

The published lists give collector numbers without set codes, so every
line was resolved by number against this repo's pool. Basic Energy is
written without a set code, as everywhere else here.

`N's Zoroark ex`'s `Night Joker` copies a Benched N's Pokémon's attack --
usually `N's Zekrom` or `N's Darmanitan`. Note that
`check_energy_support` flags those two as uncastable and is right: they
are attack DONORS and never attack themselves.

**Last of the field, and the reason is not the one first written here.**

The first version of this note blamed `Rampaging Thunder`'s self-lock:
*"during your next turn, this Pokémon can't use attacks"* is copied along
with the damage by `Night Joker`, so `N's Zoroark ex` sits out the
following turn. That is true and it is not the cause. Over 300 games
against `meta_dragapult_pure` the deck reaches its attack step 2563 times
and attacks on 769 of them. The lock accounts for **134** of the 1794
failures -- 7%.

The real entry is four times bigger: **`N's Zoroark ex` could not pay for
`Night Joker` on 528 turns.** It sat on exactly 1 of the 2 Darkness it
needs for 359 of them. Tracing where the Energy went found the actual
defect, and it was not in this deck or in the pilot:

> Paying a "discard a card from your hand" cost picked `hand[0]`. Over
> those 300 games the deck pitched **282 Basic Darkness Energy** -- out of
> the 8 it owns -- and **183 copies of `N's Zoroark ex`**, its only win
> condition. The same blind pick sat in `Ultra Ball` (`others[:2]`) and
> `Kofu`. `Ultra Ball` is in all 44 decks here.

With that fixed: attacks that actually happen 878 -> 965, turns unable to
pay 528 -> 462, and Energy is no longer near the top of the pitch list.

Two attempts to fix the *pilot* were measured and neither is in the
engine. Making the self-lock penalty conditional on the swing taking a
Prize ("lockaware") scored **-3.80 points** over 1500 mirror games on each
of the two decks that own a copy-attack, worse on both -- waiving the
penalty on a lethal swing makes the locking attack more attractive, so it
got picked more (4450 borrows vs 4021) and spent more turns locked out
(150 vs 130), the exact opposite of the intent. An Energy-targeting rule
that deprioritised copy-attack donors moved 26 of 1423 attachments and 3
of 528 failures, and was dropped as unmeasurable complexity.

So the placement is still a floor rather than an evaluation -- every card
here is modelled, and `Night Joker` does pick the right attack, 188 times
in 150 games -- but the honest remaining cause is Energy density against a
draw engine that has to discard to work, not a decision the pilot is
getting wrong.

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
