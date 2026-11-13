"""Per field deck: types, stages, Trainers by role, for the Delta Reign fit matrix."""
import sys, os, glob, json, re
os.chdir("/home/user/Pokemon-card-search"); sys.path.insert(0, ".")
import tcg_model as M
cards = M.load_cards(); by_name, by_setnum = M.build_card_index(cards)
out = {}
for p in sorted(glob.glob("decks/field/*.txt")):
    ents = M.parse_decklist_entries(open(p).read())
    rows = []
    d = {"pokemon": [], "trainers": [], "energy": []}
    for e in ents:
        c, _ = M.resolve_card(e, by_name, by_setnum)
        raw = " ".join(x for x in (e["name"], e.get("set") or "", str(e.get("number") or "")) if x)
        if not c:
            m = re.match(r"(?:Basic )?(\w+) Energy$", e["name"])
            d["energy"].append({"n": e["count"], "name": e["name"], "raw": raw, "basic": True,
                                "types": [m.group(1)] if m else []})
            continue
        rows.append((e["count"], c, raw))
    for n, c, raw in rows:
        sup = c.get("supertype")
        st = c.get("subtypes") or []
        line = {"n": n, "name": c["name"], "raw": raw, "sub": st, "types": c.get("types") or [],
                "set": (c.get("printings") or [[c["set"].get("ptcgoCode"), c.get("number")]])[0]}
        if sup == "Pokémon":
            line["stage"] = next((s for s in ("Basic", "Stage 1", "Stage 2") if s in st), "?")
            line["abil"] = bool(c.get("abilities"))
            line["costs"] = [a.get("cost") for a in c.get("attacks") or []]
            d["pokemon"].append(line)
        elif sup == "Trainer":
            d["trainers"].append(line)
        else:
            d["energy"].append(line)
    out[os.path.basename(p)[:-4]] = d
json.dump(out, open(sys.argv[1], "w"), indent=0, ensure_ascii=False)
print(len(out))
