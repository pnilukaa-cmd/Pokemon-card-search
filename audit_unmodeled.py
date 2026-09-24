"""List every card effect in the pool that the simulator does not model.

Three kinds, each checked the way the engine actually resolves it:

- Abilities that do not compile (`ability_ir`).
- Trainers and Special Energy that neither compile nor have a handler
  written by name in `simulate_versus` (Judge, Dawn, Air Balloon ... are
  hand-written and count as modelled).
- Attack texts that neither compile to a rider nor are read by any damage
  rule in `attack_damage` (DAMAGE_FALLTHROUGH), evaluated on a fixed board.
  Copy attacks are resolved by their own path and are excluded.

Usage:  python3 audit_unmodeled.py [--field]   (--field: only cards in decks/field)
"""
import glob
import sys

import ability_ir as IR
import simulate_versus as SV
import tcg_model as M

_SRC = open(SV.__file__).read()


def _board():
    cards = M.load_cards()
    SV._CARDS_BY_NAME.update(M.build_card_index(cards)[0])
    D = SV.load_model("decks/field/meta_raging_bolt.txt", "b")[0]
    E = SV.compile_effects_for(D[1], D[3])
    me, op = SV.Player("b", D[1], D[2], E), SV.Player("o", D[1], D[2], E)
    me.active = SV.InPlay("Raging Bolt ex", 0)
    me.active.energy = [["Lightning"], ["Fighting"], ["Grass"]]
    me.active.energy_names = ["Lightning Energy", "Fighting Energy", "Grass Energy"]
    op.active = SV.InPlay("Mega Kangaskhan ex", 0)
    op.active.damage = 50
    me.bench, op.bench = [SV.InPlay("Passimian", 0)], [SV.InPlay("Passimian", 0)]
    me._opp_ref, me.round_no, op.round_no = op, 4, 4
    return me, op


def _trainer_modelled(c):
    """Modelled outside the compiler: a handler by name, a Stadium's
    per-turn effect, Academy at Night's shape, or an Energy whose
    provision the text sets (energy_provisions)."""
    name = c["name"]
    if f'"{name}"' in _SRC or f"'{name}'" in _SRC:
        return True
    if SV.stadium_turn_effect_ir(name) is not None:
        return True
    text = " ".join(c.get("rules") or [])
    if any(rx.search(text) for rx in (SV._HAND_TO_TOP_RE, SV._GARDEN_RE, SV._BEACH_RE,
                                      SV._PROVIDES_EVERY_RE, SV._PROVIDES_EVERY_IF_RE)):
        return True
    if c.get("supertype") == "Energy":
        prov = SV.energy_provisions(name, SV._CARDS_BY_NAME)
        if prov and prov[0] != list(M.REAL_TYPES) or len(prov) > 1:
            return True
    return False


def _attack_modelled_elsewhere(text):
    """Text do_attack reads directly (Weakness/Resistance/effects ignored)."""
    only = SV._re.sub(r"this attack's damage isn't affected by[^.]*\.", "", text,
                      flags=SV._re.I).strip()
    return not only


def audit(only_names=None):
    me, op = _board()
    out = {"Ability": [], "Trainer": [], "Energy": [], "Attack": []}
    seen = set()
    for c in M.load_cards():
        if only_names is not None and c["name"] not in only_names:
            continue
        for ab in c.get("abilities") or []:
            e = IR.compile_effect(c["name"], ab.get("name") or "", ab.get("text") or "")
            if e.unsupported and e.unsupported != "no text":
                out["Ability"].append(f"{c['name']} / {ab.get('name')}")
        st = c.get("supertype")
        if st in ("Trainer", "Energy") and "Basic" not in (c.get("subtypes") or []):
            e = IR.compile_effect(c["name"], c["name"], " ".join(c.get("rules") or []))
            if e.unsupported and not _trainer_modelled(c):
                out[st].append(c["name"])
        for at in c.get("attacks") or []:
            t = at.get("text") or ""
            if not t or t in seen:
                continue
            seen.add(t)
            e = IR.compile_effect(c["name"], at.get("name") or "", t)
            if not e.unsupported or e.unsupported == "copies another attack":
                continue
            if SV._USE_AS_THIS_RE.search(t) or _attack_modelled_elsewhere(t):
                continue
            a = {"name": at.get("name"), "cost": [], "damage": int("".join(
                ch for ch in (at.get("damage") or "0") if ch.isdigit()) or 0), "text": t}
            SV.DAMAGE_FALLTHROUGH[0] = False
            SV.attack_damage(me, op, me.active, a, record=False)
            if SV.DAMAGE_FALLTHROUGH[0]:
                out["Attack"].append(f"{c['name']} / {at.get('name')}: {t}")
    return out


if __name__ == "__main__":
    names = None
    if "--field" in sys.argv:
        names = set()
        cards = M.load_cards()
        bn, bs = M.build_card_index(cards)
        for f in glob.glob("decks/field/*.txt"):
            for e in M.parse_decklist_entries(open(f).read()):
                c, _ = M.resolve_card(e, bn, bs)
                if c:
                    names.add(c["name"])
    res = audit(names)
    for k, v in res.items():
        print(f"== {k}: {len(v)}")
        for x in sorted(set(v)):
            print("  ", x[:220])
    print("total unmodelled:", sum(len(set(v)) for v in res.values()))
