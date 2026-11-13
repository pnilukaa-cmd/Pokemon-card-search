"""Fit matrix and variant lists: which Delta Reign cards each field deck can
use, and the standard cut for each. Writes var/<deck>__<cand>.txt and fit.json."""
import json, subprocess, sys, os
S = "/tmp/claude-0/-home-user-Pokemon-card-search/32313191-2e9b-5f12-921b-86b3863481b6/scratchpad"
R = "/home/user/Pokemon-card-search"
P = json.load(open(f"{S}/dlr2/profile.json"))
VARIANT = f"{R}/runs/2026-10-23/snorlax_screens/variant.py"
FLEX_ITEMS = ["Night Stretcher", "Switch", "Pokégear 3.0", "Energy Search", "Energy Switch",
              "Energy Retrieval", "Energy Recycler", "Max Rod", "Super Rod", "Pal Pad"]
CANDS = {
    # name: (line, copies, kind)
    "aarune": ("Aarune DLR 89", 1, "supporter"),
    "pyroduct": ("Legendary Pyroduct DLR 94", 2, "stadium"),
    "vest": ("Custom Vest DLR 91", 2, "tool"),
    "darkrai": ("Darkrai DLR 63", 2, "pokemon"),
    "raikou": ("Raikou ex DLR 33", 2, "pokemon"),
    "heat_rotom": ("Heat Rotom ex DLR 23", 2, "pokemon"),
    "wishiwashi": ("Wishiwashi ex DLR 29", 2, "pokemon"),
    "giratina": ("Giratina DLR 45", 2, "pokemon"),
}
TYPE_CAND = {"Darkness": "darkrai", "Lightning": "raikou", "Fire": "heat_rotom",
             "Water": "wishiwashi", "Psychic": "giratina"}


def basic_energy(d):
    out = {}
    for e in d["energy"]:
        if e.get("basic"):
            for t in e["types"]:
                out[t] = out.get(t, 0) + e["n"]
    return out


def cuts_for(d, kind, k):
    """The standard cut: k cards, as [(line, n)]."""
    tr = d["trainers"]
    def pool(pred):
        return sorted([t for t in tr if pred(t)], key=lambda t: -t["n"])
    sup = pool(lambda t: "Supporter" in t["sub"] and t["name"] != "Boss's Orders")
    if kind == "supporter":
        order = sup
    elif kind == "stadium":
        order = pool(lambda t: "Stadium" in t["sub"]) + pool(lambda t: t["name"] in FLEX_ITEMS) + sup
    elif kind == "tool":
        order = pool(lambda t: "Pokémon Tool" in t["sub"] and "ACE SPEC" not in t["sub"]) \
            + pool(lambda t: t["name"] in FLEX_ITEMS) + sup
    else:
        order = pool(lambda t: t["name"] in FLEX_ITEMS) + sup
    out, left = [], k
    for t in order:
        if left <= 0:
            break
        take = min(t["n"], left)
        out.append((t["raw"], take))
        left -= take
    return out if left == 0 else None


fit = {}
for deck, d in sorted(P.items()):
    names = {p["name"] for p in d["pokemon"]} | {t["name"] for t in d["trainers"]}
    evo_abil = any(p["stage"] != "Basic" and p["abil"] for p in d["pokemon"])
    megas = any("MEGA" in p["sub"] for p in d["pokemon"])
    be = basic_energy(d)
    cands = ["aarune", "vest"]
    if not evo_abil:
        cands.append("pyroduct")
    for t, c in TYPE_CAND.items():
        if be.get(t, 0) >= 8:
            cands.append(c)
    fit[deck] = {}
    for c in cands:
        line, k, kind = CANDS[c]
        if line.rsplit(" ", 2)[0] in names:
            fit[deck][c] = "already plays it"
            continue
        if c == "vest" and megas and all("MEGA" in p["sub"] or p["stage"] != "Basic"
                                          for p in d["pokemon"] if p["n"] >= 3):
            pass
        cut = cuts_for(d, kind, k)
        if cut is None:
            fit[deck][c] = "no standard cut"
            continue
        out = f"{S}/dlr2/var/{deck}__{c}.txt"
        args = [f"{line}:+{k}"] + [f"{raw}:-{n}" for raw, n in cut]
        r = subprocess.run([sys.executable, VARIANT, f"{R}/decks/field/{deck}.txt", out] + args,
                           capture_output=True, text=True, cwd=R)
        fit[deck][c] = {"add": f"{k} {line}", "cut": [f"{n} {raw}" for raw, n in cut],
                        "file": out} if r.returncode == 0 else f"variant failed: {r.stderr[-200:]}"
json.dump(fit, open(f"{S}/dlr2/fit.json", "w"), indent=1, ensure_ascii=False)
n = sum(1 for v in fit.values() for x in v.values() if isinstance(x, dict))
print("decks", len(fit), "variants", n)
from collections import Counter
print(Counter(c for v in fit.values() for c, x in v.items() if isinstance(x, dict)))
print([ (d, c, x) for d, v in fit.items() for c, x in v.items() if not isinstance(x, dict)][:20])
