"""boardgame.py LIST OPP SEED -- one verbose game; at the end of each of
my turns print my board (name energy/damage), hand Pokemon/Energy count."""
import random, sys
sys.path.insert(0,'/home/user/Pokemon-card-search')
import simulate_versus as SV, tcg_model as M
SV._CARDS_BY_NAME.update(M.build_card_index(M.load_cards())[0])
A=SV.load_model(sys.argv[1],'me')[0]; B=SV.load_model(sys.argv[2],'o')[0]
_fin = SV.finish_turn
def fin(pl, opp, log):
    if pl.name == 'me':
        sp = lambda s: f"{s.name}[{s.energy_count()}E {s.damage}d{' P' if getattr(s,'conditions',None) else ''}]"
        log.append("    BOARD: " + (sp(pl.active) if pl.active else '-') + " | " + ", ".join(sp(b) for b in pl.bench)
                   + f" | hand E={sum(1 for k,_ in pl.hand if k=='Energy')} "
                   + ",".join(n for k,n in pl.hand if k!='Energy'))
    return _fin(pl, opp, log)
SV.finish_turn = fin
random.seed(int(sys.argv[3]))
r=SV.run_game(A,B,verbose=True)
