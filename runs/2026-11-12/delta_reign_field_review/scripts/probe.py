"""Stage a board and run one card's effect through the real engine."""
import sys, os, random
os.chdir("/home/user/Pokemon-card-search"); sys.path.insert(0, ".")
import simulate_versus as SV, tcg_model as M, ability_engine as AE, ability_ir as IR
SV._CARDS_BY_NAME.update(M.build_card_index(M.load_cards())[0])
S = "/tmp/claude-0/-home-user-Pokemon-card-search/32313191-2e9b-5f12-921b-86b3863481b6/scratchpad"

def model(lines, label="me"):
    p = f"{S}/dr/_probe_{label}.txt"
    open(p, "w").write("\n".join(lines) + "\n")
    return SV.load_model(p, label)[0]

def players(mine, theirs=("1 Dragapult ex TWM 130", "1 Drakloak TWM 129", "1 Dreepy TWM 128",
                          "1 Fezandipiti ex SFA 38")):
    A = model(list(mine), "me"); O = model(list(theirs), "o")
    me = SV.Player("me", A[1], [], SV.compile_effects_for(A[1], A[3]))
    op = SV.Player("o", O[1], [], SV.compile_effects_for(O[1], O[3]))
    me._opp_ref, op._opp_ref = op, me
    me.round_no = op.round_no = 5
    return me, op

def atk_of(pl, name, atk):
    return next(a for a in pl.POKEMON[name]["attacks"] if a["name"] == atk)
