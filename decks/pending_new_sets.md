# Pending — ten lists, no longer blocked on data

**Not my lists.** Nine supplied by the user from a pastebin dated
2026-09-14, plus a tenth supplied 2026-09-16 (see the last section).
Held here rather than in the field: the card data has now landed, but
five of them still name a printing this pool cannot identify, and none has
been measured. No fenced decklist per deck on purpose — `check_decks.py`
would be right to reject a list whose SET NUM does not resolve exactly.

## Status, 2026-09-17 — the data landed

30th Celebration is in the API and in this pool.

```
2026/09/16  30C  30th Celebration                     161 cards
2026/09/16  30C  30th Celebration: Classic Collection  30 cards
```

`fetch_pokemon_cards.py` added **125 records and 32 new names**, among them
`Alolan Exeggutor`, `Espeon`, `Ditto`, `Cosmog`/`Cosmoem`, `Cherubi`/`Cherrim`,
`Hisuian Zoroark` and `Fuecoco ex`. The pool is now 2089 records / 1421
distinct names.

**No new regulation mark.** 30C ships under H/I/J, which
`ACTIVE_REGULATION_MARKS` already covers, so nothing needed widening — the
`K`/`L` probe came back empty, which is the answer it was written to give.
The Classic Collection subset is a separate set id (`me55c`) whose cards
carry old marks or none at all, so the mark-driven fetch never considered
them; that is correct, they are not Standard-legal printings.

## A parser bug was doing most of the damage

Five of these lists were recorded as blocked on a card called `Mew ex M6a`,
`Unown M6a`, `Greninja ex M6a` and so on. There is no such card. The set
code was being swallowed into the NAME:

    "2 Mew ex M6a 57"  ->  {name: "Mew ex M6a", set: None, number: "57"}

`parse_decklist_entries` accepted a set code only if `tokens[-1].isupper()`,
and `"M6a".isupper()` is False because of the trailing lower-case letter.
`M6a` is a Japanese-style set code, which is what these lists were written
with. Fixed by matching `[A-Z0-9]{2,7}[a-z]?` instead — two upper-case
characters are still required before the optional suffix, so short name
tokens (`Ho`, `ex`) cannot be mistaken for a code.

With that fixed, **all ten lists reach 60/60.** None is blocked any more.

## But nine of them resolve at least one card by NAME, not by SET NUM

`resolve_card` falls back to matching on name alone when the SET NUM is not
in the pool, and returns `matches[0]`. **418 names in this pool have more
than one functionally different card**, so that fallback is a coin toss
dressed as a result. The 45 measured field decks are clean — every line
there carries an exact SET NUM and `check_decks.py` refuses anything
else — but these ten lists are not.

`M6a`, `MP` and `MF` are all codes this pool does not contain. Here is what
each ambiguous line actually resolved to, and what it probably meant:

| written | fallback picked | 30C also has | verdict |
|---|---|---|---|
| `Sylveon ex` **MP 153** | SSP 86, 270 HP, Magical Charm | **30C 153**, 270 HP, Colorful Harmony | **fallback is wrong** — the number matches 30C exactly |
| `Greninja ex` **M6a 15** | TWM 106, 310 HP Tera, Shinobi Blade | 30C 21, 300 HP, Aqua Edge | undetermined, 30C likelier |
| `Gengar ex` **M6a 76** | TEF 104, 310 HP, Tricky Steps | 30C 90, 280 HP, Chaotic Pain | undetermined, 30C likelier |
| `Salamence ex` **M6a 88** | JTG 114, 320 HP, Dragon Impact | 30C 109, 330 HP, Dragon Pulse | undetermined, 30C likelier |
| `Umbreon ex` **MF 17** | PRE 161, 280 HP Tera, Moon Mirage | 30C 92, 270 HP, Lunatic Claw | undetermined; no set has a 17 |

The pattern is against the fallback in every row: these are 30th
Celebration lists, and the fallback picks the OLDER printing every time,
because it returns the first entry in pool order and the older sets were
fetched first.

Four lines are ambiguous but **safe**, because the pool holds exactly one
card of that name: `Mew ex M6a 57` → 30C 66, `Unown M6a 60` → 30C 72, and
`Alolan Exeggutor MP 148` → 30C 2. That last one is worth noting: `MP 148`
is a wrong number under any reading (30C 148 is Greninja ex), but Alolan
Exeggutor exists only in 30C, so it resolves correctly anyway.

**Nothing here has been measured.** Five lists cannot be simulated
honestly until those five set codes are resolved against the real cards.

## Two new cards need rules before these lists can be simulated

`analyze_mechanics.py` leaves both untagged:

- `Mew ex` — **Memory Helix**: "This Pokémon can use the attacks of any of
  your Benched Pokémon." Same shape as `N's Zoroark ex`'s Night Joker. The
  copy-attack machinery is built and exercised; only the rule that
  recognises this text is missing.
- `Sylveon ex` — **Colorful Harmony**: "50 damage for each type of Basic
  Energy attached to all of your Pokémon." A typed-Energy scaler counting
  DISTINCT TYPES rather than count, which is a shape `attack_damage` does
  not currently have.

## What is left to do

1. **Resolve the five ambiguous lines above against the real cards** —
   `Sylveon ex MP 153`, `Greninja ex M6a 15`, `Gengar ex M6a 76`,
   `Salamence ex M6a 88`, `Umbreon ex MF 17`. Once each is rewritten with a
   SET NUM this pool holds, `resolve_card` matches exactly and the name
   fallback never fires.
2. **Write the two missing rules** (Memory Helix, Colorful Harmony).
3. Then measure. Nothing in this file has a win rate yet.

30C is tournament legal from **2026-09-25**.

## The lists as supplied

### mew_bunny

```text
Pokémon: 19
4 Dunsparce JTG 120
3 Dudunsparce TEF 129
1 Dudunsparce ex JTG 121
3 Buneary PFL 83
3 Mega Lopunny ex PFL 84
2 Mew ex M6a 57
1 Fan Rotom ASC 171
1 Lillie's Clefairy ex ASC 76
1 Chien-Pao SSP 56
Trainer: 32
4 Lillie's Determination ASC 192
3 Hilda WHT 84
3 Wally's Compassion MEG 132
3 Boss's Orders ASC 183
4 Buddy-Buddy Poffin ASC 184
4 Poké Pad POR 81
3 Ultra Ball ASC 213
2 Wondrous Patch PFL 94
1 Pokégear 3.0 BLK 84
2 Air Balloon BLK 79
3 Battle Cage PFL 85
Energy: 9
4 Psychic Energy MEE 5
4 Mist Energy TEF 161
1 Enriching Energy SSP 191
```

### umbreon

```text
Pokémon: 17
3 Eevee SFA 50
3 Umbreon ex MF 17
2 Toxel PFL 67
2 Toxtricity PFL 68
2 Munkidori ASC 99
2 Pecharunt ex SFA 39
1 Chi-Yu PBL 59
1 Fezandipiti ex ASC 142
1 Pecharunt PR-SV 149
Trainer: 33
4 Lillie's Determination ASC 192
3 Boss's Orders MEG 114
2 Judge POR 76
2 Team Rocket's Petrel ASC 207
4 Ultra Ball ASC 213
4 Buddy-Buddy Poffin ASC 184
4 Pokégear 3.0 BLK 84
2 Poké Pad POR 81
1 Unfair Stamp TWM 165
1 Energy Recycler DRI 164
1 Night Stretcher ASC 196
2 Binding Mochi PRE 95
1 Air Balloon ASC 181
2 Team Rocket's Watchtower ASC 210
Energy: 10
10 Darkness Energy MEE 7
```

### unown

```text
Pokémon: 22
4 Slowpoke SCR 57
3 Slowking SCR 58
3 Mega Kangaskhan ex MEG 104
2 Latias ex SSP 76
2 Metagross CRI 61
2 Kyurem SFA 47
1 Annihilape SSP 100
1 Annihilape PBL 41
1 Unown M6a 60
1 Fezandipiti ex ASC 142
1 Lillie's Clefairy ex ASC 76
1 Meowth ex POR 62
Trainer: 28
4 Lillie's Determination ASC 192
4 Ciphermaniac's Codebreaking PRE 104
4 Ultra Ball ASC 213
4 Poké Pad POR 81
3 Wondrous Patch PFL 94
3 Night Stretcher SFA 61
1 Switch MEG 130
1 Prime Catcher PRE 119
4 Academy at Night SFA 54
Energy: 10
4 Telepathic Psychic Energy POR 88
4 Psychic Energy MEE 5
2 Boomerang Energy TWM 166
```

### greninja

```text
Pokémon: 19
4 Froakie CRI 20
2 Frogadier CRI 21
2 Mega Greninja ex CRI 22
1 Greninja ex M6a 15
1 Greninja ex TWM 106
2 Dunsparce JTG 120
1 Dunsparce PRE 79
3 Dudunsparce PRE 80
1 Dudunsparce ex JTG 121
1 Budew ASC 16
1 Fezandipiti ex ASC 142
Trainer: 32
4 Lillie's Determination ASC 192
3 Hilda WHT 84
2 Boss's Orders ASC 183
1 Judge POR 76
4 Rare Candy MEG 125
4 Buddy-Buddy Poffin ASC 184
4 Poké Pad POR 81
2 Ultra Ball ASC 213
1 Special Red Card CRI 82
1 Night Stretcher ASC 196
1 Energy Retrieval WHT 82
2 Air Balloon BLK 79
3 Surfing Beach MEG 129
Energy: 9
7 Water Energy MEE 3
1 Neo Upper Energy TEF 162
1 Ignition Energy WHT 86
```

### mew_mega

```text
Pokémon: 18
2 Mew ex M6a 57
2 Mega Audino ex ASC 172
2 Mega Kangaskhan ex MEG 104
2 Mega Absol ex MEG 86
2 Munkidori ASC 99
1 Yveltal MEG 88
2 Pecharunt ex SFA 39
1 Fezandipiti ex ASC 142
1 Moltres PFL 14
1 Lillie's Clefairy ex ASC 76
1 Meowth ex POR 62
1 Latias ex SSP 76
Trainer: 29
4 Lillie's Determination ASC 192
3 Boss's Orders ASC 183
2 Brock's Scouting JTG 146
2 Crispin PRE 105
4 Mega Signal MEG 121
4 Ultra Ball ASC 213
2 Night Stretcher ASC 196
2 Energy Switch MEG 115
1 Special Red Card CRI 82
2 Pokégear 3.0 BLK 84
1 Hero's Cape TEF 152
1 Team Rocket's Watchtower ASC 210
1 Lively Stadium SSP 180
Energy: 13
7 Darkness Energy MEE 7
3 Mist Energy TEF 161
2 Psychic Energy MEE 5
1 Fire Energy MEE 2
```

### exeggutor

```text
Pokémon: 19
2 Exeggcute SSP 1
2 Exeggcute MEG 4
3 Alolan Exeggutor MP 148
4 Teal Mask Ogerpon ex TWM 25
3 Chikorita MEG 8
2 Bayleef MEG 9
2 Meganium MEG 10
1 Fezandipiti ex ASC 142
Trainer: 30
4 Lillie's Determination ASC 192
2 Gwynn PBL 78
2 Boss's Orders ASC 183
1 Lana's Aid TWM 155
4 Energy Switch MEG 115
4 Bug Catching Set PRE 102
4 Poké Pad POR 81
2 Ultra Ball ASC 213
2 Jumbo Ice Cream PFL 91
1 Night Stretcher ASC 196
1 Hero's Cape TEF 152
3 Forest of Vitality ASC 188
Energy: 11
11 Grass Energy MEE 1
```

### sylveon

```text
Pokémon: 18
4 Eevee SFA 50
3 Sylveon ex MP 153
4 Team Rocket's Tarountula ASC 18
4 Team Rocket's Spidops ASC 19
1 Lillie's Clefairy ex JTG 56
1 Fezandipiti ex ASC 142
1 Meowth ex POR 62
Trainer: 31
4 Lillie's Determination ASC 192
2 Crispin PRE 105
2 Boss's Orders MEG 114
2 Team Rocket's Petrel ASC 207
4 Energy Switch MEG 115
4 Buddy-Buddy Poffin ASC 184
4 Ultra Ball ASC 213
3 Poké Pad POR 81
2 Wondrous Patch PFL 94
1 Night Stretcher ASC 196
1 Energy Search Pro SSP 176
1 Air Balloon ASC 181
1 Prism Tower CRI 80
Energy: 11
4 Psychic Energy MEE 5
1 Grass Energy MEE 1
1 Fire Energy MEE 2
1 Water Energy MEE 3
1 Lightning Energy MEE 4
1 Fighting Energy MEE 6
1 Darkness Energy MEE 7
1 Metal Energy MEE 8
```

### gengar

```text
Pokémon: 20
4 Gastly POR 48
2 Haunter ASC 124
3 Gengar ex M6a 76
1 Mega Gengar ex ASC 125
2 Toxel PFL 67
2 Toxtricity PFL 68
2 Munkidori ASC 99
1 Tatsugiri TWM 131
1 Shaymin DRI 10
1 Chi-Yu PBL 59
1 Pecharunt ex SFA 39
Trainer: 31
4 Lillie's Determination ASC 192
2 Boss's Orders MEG 114
2 Team Rocket's Petrel DRI 176
4 Rare Candy MEG 125
4 Buddy-Buddy Poffin ASC 184
4 Ultra Ball ASC 213
3 Poké Pad POR 81
1 Night Stretcher ASC 196
1 Unfair Stamp TWM 165
1 Special Red Card CRI 82
1 Energy Recycler DRI 164
2 Air Balloon ASC 181
2 Team Rocket's Watchtower ASC 210
Energy: 9
9 Darkness Energy MEE 7
```

### salamence

```text
Pokémon: 20
4 Dreepy ASC 158
4 Drakloak ASC 159
2 Dragapult ex ASC 160
2 Bagon JTG 112
1 Shelgon JTG 113
2 Salamence ex M6a 88
1 Fezandipiti ex ASC 142
1 Meowth ex POR 62
1 Budew ASC 16
1 Patrat CRI 70
1 Moltres PFL 14
Trainer: 31
4 Lillie's Determination ASC 192
3 Crispin PRE 105
2 Boss's Orders MEG 114
1 Rosa's Encouragement POR 84
1 Judge POR 76
4 Buddy-Buddy Poffin ASC 184
4 Poké Pad POR 81
3 Rare Candy MEG 125
3 Ultra Ball ASC 213
1 Unfair Stamp TWM 165
2 Night Stretcher ASC 196
1 Special Red Card CRI 82
1 Air Balloon ASC 181
1 Team Rocket's Watchtower ASC 210
Energy: 9
4 Fire Energy MEE 2
3 Water Energy MEE 3
2 Psychic Energy MEE 5
```

## A tenth list, supplied 2026-09-16 — `ogerpon_exeggutor`

Same archetype as `exeggutor` above, but a **different build**, and it
names the blocked card under a **different printing**:
`Alolan Exeggutor 30C 2` here versus `Alolan Exeggutor MP 148` in the
pastebin list. Neither set code is in the pool, so both lists are blocked
on the same card for the same reason; when 30C lands, `30C 2` is the one
that should resolve directly.

Resolution as supplied: **57/60**, unresolved `Alolan Exeggutor` only.
Legality check: clean.

Two things were normalised before checking, and are normalised in the
transcription below:

- `12 Basic {G} Energy MEE 1` → `12 Basic Grass Energy`. `MEE` is the 30th
  Celebration foil Basic Energy subset; Basic Energy carries no set code
  in this repo. Same rewrite as every other list in this file.
- `Bug Catching Set TWM 143` arrived split across two lines, `3` and `1`.
  Merged to `4`. The split is legal in PTCGL's exporter but
  `check_decks.py` counts lines, not cards.

The header counts are line counts, not card counts — `Pokémon: 9` is 9
lines / 18 cards, `Trainer: 14` is 14 lines / 30 cards, `Energy: 1` is 1
line / 12 cards. 18 + 30 + 12 = 60, so the deck itself is legal; only the
headers are wrong. Rewritten below with true card counts.

Deck differences worth noting against the pastebin `exeggutor`: this one
runs `Dawn PFL 87` and `Ciphermaniac's Codebreaking TEF 145` over
`Gwynn PBL 78` / `Lana's Aid TWM 155` / `Jumbo Ice Cream PFL 91`, trades a
`Chikorita MEG 8` for `Chikorita ASC 8`, adds `Meowth ex POR 62`,
`Special Red Card CRI 82` and `Air Balloon ASC 181`, and goes to 12 Energy
from 11.

```text
Pokémon: 18
4 Teal Mask Ogerpon ex TWM 25
2 Meganium MEG 10
3 Alolan Exeggutor 30C 2
2 Exeggcute SSP 1
2 Chikorita ASC 8
2 Bayleef MEG 9
1 Fezandipiti ex ASC 142
1 Exeggcute MEG 4
1 Meowth ex POR 62
Trainer: 30
4 Bug Catching Set TWM 143
2 Dawn PFL 87
3 Poké Pad POR 81
1 Hero's Cape TEF 152
3 Ultra Ball ASC 213
1 Special Red Card CRI 82
1 Night Stretcher ASC 196
4 Lillie's Determination ASC 192
3 Forest of Vitality ASC 188
1 Ciphermaniac's Codebreaking TEF 145
2 Boss's Orders ASC 183
1 Air Balloon ASC 181
4 Energy Switch MEG 115
Energy: 12
12 Basic Grass Energy
```
