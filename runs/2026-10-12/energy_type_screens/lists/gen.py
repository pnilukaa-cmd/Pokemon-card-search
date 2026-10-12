"""gen.py <search: ub|en> -- write one Cinderace shell per Energy type into et/.

Same frame as the Fighting list: 4 Cinderace, 2 main hitters, 1 second
hitter, 1 Mega Audino ex, the same generic Trainers. Fighting-only cards
(Fighting Gong, Premium Power Pro, Core Memory, Rocky Fighting Energy)
become the type's own support where it exists.
"""
import sys, os
search = sys.argv[1]
out = os.path.dirname(os.path.abspath(__file__))
CORE = [(4, "Lillie's Determination MEG 184"), (4, "Team Rocket's Petrel DRI 226"),
        (2, "Iris's Fighting Spirit JTG 180"), (3, "Boss's Orders MEG 114"),
        (4, "Jumbo Ice Cream CRI 109"), (1, "Mega Signal MEG 171"), (1, "Switch PFL 123"),
        (1, "Hero's Cape TEF 152"), (1, "Team Rocket's Factory DRI 173")]
SEARCH = [(4, "Ultra Ball MEG 131")] if search == "ub" else []
T = {
  "fire": dict(mon=[(2, "Gouging Fire ex TEF 188"), (1, "Reshiram ex JTG 30")],
               basic="Fire", special=[(3, "Nitro Fire Energy CRI 86")],
               flex=[(1, "Blowtorch PFL 117")], stadium=(1, "Lively Stadium SSP 180")),
  "water": dict(mon=[(2, "Black Kyurem ex SSP 218"), (1, "Dondozo ex DRI 211")],
                basic="Water", special=[(3, "Bubbly Water Energy CRI 84")],
                flex=[(1, "Misty's Vitality PBL 111")], stadium=(1, "Lively Stadium SSP 180")),
  "grass": dict(mon=[(2, "Mega Heracross ex PFL 108"), (1, "Iron Leaves ex TEF 186")],
                basic="Grass", special=[(3, "Growing Grass Energy POR 86")],
                flex=[], stadium=(1, "Lively Stadium SSP 180"),
                search=[(4, "Bug Catching Set TWM 143")]),
  "lightning": dict(mon=[(2, "Mega Zeraora ex PBL 114"), (1, "Pikachu ex PRE 28")],
                    basic="Lightning", special=[(3, "Voltaic Lightning Energy PBL 84")],
                    flex=[], stadium=(1, "Lively Stadium SSP 180")),
  "psychic": dict(mon=[(2, "Mega Diancie ex PFL 41"), (1, "Mega Floette ex CRI 101")],
                  basic="Psychic", special=[(3, "Telepathic Psychic Energy POR 88")],
                  flex=[(1, "Jacinthe POR 110")], stadium=(1, "Lively Stadium SSP 180")),
  "darkness": dict(mon=[(2, "Mega Absol ex MEG 161"), (1, "Yveltal ex POR 105")],
                   basic="Darkness", special=[(3, "Shadowy Darkness Energy PBL 83")],
                   flex=[(1, "Janine's Secret Art SFA 59")], stadium=(1, "Lively Stadium SSP 180")),
  "metal": dict(mon=[(2, "Mega Mawile ex MEG 162"), (1, "Hop's Zacian ex JTG 111")],
                basic="Metal", special=[(3, "Magnetic Metal Energy CRI 85")],
                flex=[], stadium=(1, "Full Metal Lab TEF 148")),
  "colorless": dict(mon=[(2, "Mega Kangaskhan ex MEG 104"), (1, "Bloodmoon Ursaluna ex TWM 141")],
                    basic="Fighting", special=[(3, "Mist Energy TEF 161")],
                    flex=[(1, "Backtrack Badge PBL 74")], stadium=(1, "Lively Stadium SSP 180")),
  "firepsychic": dict(mon=[(2, "Mega Latias ex MEG 100"), (1, "Gouging Fire ex TEF 188")],
                      basic=("Fire", "Psychic"), special=[(3, "Prism Energy ASC 216")],
                      flex=[], stadium=(1, "Lively Stadium SSP 180")),
}
for name, t in T.items():
    mon = [(4, "Cinderace MEG 28")] + t["mon"] + [(1, "Mega Audino ex ASC 253")]
    tr = CORE + t.get("search", SEARCH) + t["flex"] + [t["stadium"]]
    n_basic = 60 - sum(n for n, _ in mon + tr + t["special"])
    if isinstance(t["basic"], tuple):
        a = (n_basic + 1) // 2
        en = [(a, f"Basic {t['basic'][0]} Energy"), (n_basic - a, f"Basic {t['basic'][1]} Energy")]
    else:
        en = [(n_basic, f"Basic {t['basic']} Energy")]
    en += t["special"]
    lines = []
    for head, sec in (("Pokémon", mon), ("Trainer", tr), ("Energy", en)):
        lines.append(f"{head}: {sum(n for n, _ in sec)}")
        lines += [f"{n} {c}" for n, c in sec] + [""]
    lines.append("Total Cards: 60")
    open(f"{out}/T_{name}_{search}.txt", "w").write("\n".join(lines) + "\n")
