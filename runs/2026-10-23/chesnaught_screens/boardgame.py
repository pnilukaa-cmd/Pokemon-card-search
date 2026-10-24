"""boardgame.py LIST OPP SEED [knobs] -- one verbose game; at the end of each of
my turns print my board (name energy/HP left), hand Energy count."""
import random, sys, os
sys.path.insert(0, '/home/user/Pokemon-card-search')
if len(sys.argv) > 4:
    os.environ["PROBE_KNOBS"] = sys.argv[4]
import simulate_versus as SV, tcg_model as M
SV._CARDS_BY_NAME.update(M.build_card_index(M.load_cards())[0])
A = SV.load_model(sys.argv[1], 'me')[0]; B = SV.load_model(sys.argv[2], 'o')[0]
if len(sys.argv) > 4:
    SV.PILOT_BY_NAME['me'] = 'probe'
_fin = SV.finish_turn
def fin(pl, opp, log):
    if pl.name == 'me':
        sp = lambda s: f"{s.name}[{len(SV.provided(pl, s))}E {SV.effective_hp(pl, s) - s.damage}hp{' ' + ','.join(sorted(s.conditions)) if s.conditions else ''}]"
        log.append("    BOARD: " + (sp(pl.active) if pl.active else '-') + " | " + ", ".join(sp(b) for b in pl.bench)
                   + f" | hand E={sum(1 for k, _ in pl.hand if k == 'Energy')} ")
    return _fin(pl, opp, log)
SV.finish_turn = fin
random.seed(int(sys.argv[3]))
r = SV.run_game(A, B, verbose=True)
