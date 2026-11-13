"""Every Delta Reign attack's damage on a fixed board, with the damage-rule
fall-through flag. Attacker Active with its own types' Energy; opponent's
Active a Dragapult ex with 50 damage and 2 Energy, Bench of 3 (2 with
Abilities, 1 Energy each, 1 damaged); 3 Basic Fire Energy in my discard;
opponent's hand 6; my hand 3 Pokemon of different types; my Bench 2."""
import sys, os, random
os.chdir("/home/user/Pokemon-card-search"); sys.path.insert(0, ".")
import simulate_versus as SV, tcg_model as M
SV._CARDS_BY_NAME.update(M.build_card_index(M.load_cards())[0])
A = SV.load_model(sys.argv[1], "me")[0]
O = SV.load_model("decks/field/meta_dragapult_pure.txt", "o")[0]
E = SV.compile_effects_for(A[1], A[3]); Eo = SV.compile_effects_for(O[1], O[3])
rows = []
for name, info in sorted(A[1].items()):
    for atk in info.get("attacks") or []:
        random.seed(1)
        me = SV.Player("me", A[1], [], E); op = SV.Player("o", O[1], [], Eo)
        me._opp_ref, op._opp_ref = op, me; me.round_no = op.round_no = 5
        me.active = SV.InPlay(name, 3)
        types = info.get("types") or ["Colorless"]
        me.active.energy = [[t if t != "Colorless" else "Psychic"] for t in (types * 4)[:4]]
        me.active.energy_names = [f"{e[0]} Energy" for e in me.active.energy]
        me.bench = [SV.InPlay("Tauros", 2), SV.InPlay("Eevee", 2)]
        me.discard = ["Fire Energy"] * 3
        me.hand = [("Pokemon", "Tauros"), ("Pokemon", "Heracross"), ("Pokemon", "Raikou ex")]
        op.active = SV.InPlay("Dragapult ex", 2); op.active.damage = 50
        op.active.energy, op.active.energy_names = [["Fire"], ["Psychic"]], ["Fire Energy", "Psychic Energy"]
        op.bench = [SV.InPlay("Drakloak", 2), SV.InPlay("Fezandipiti ex", 2), SV.InPlay("Dreepy", 2)]
        op.bench[2].damage = 20
        for b in op.bench:
            b.energy, b.energy_names = [["Psychic"]], ["Psychic Energy"]
        op.hand = [("Item", "x")] * 6
        SV.DAMAGE_FALLTHROUGH[0] = False
        try:
            dmg = SV.attack_damage(me, op, me.active, atk)
        except Exception as e:
            dmg = f"ERR {e!r}"[:60]
        rows.append((name, atk["name"], atk.get("damage"), dmg, SV.DAMAGE_FALLTHROUGH[0], (atk.get("text") or "")[:95]))
for r in rows:
    flag = "FALL" if r[4] and r[5] else "    "
    print(f"{flag} {r[0][:16]:16s} {r[1][:18]:18s} printed={str(r[2]):5s} -> {str(r[3]):6s} | {r[5]}")
