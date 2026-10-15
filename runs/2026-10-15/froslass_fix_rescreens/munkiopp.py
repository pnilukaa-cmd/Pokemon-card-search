"""Per my turn (at the attack step): Munkidori in play, how many have Darkness
Energy, whether my board has counters to move -- against Adrena-Brain uses."""
import random, sys, io, glob, collections
sys.path.insert(0,'.')
import simulate_versus as SV, tcg_model as M, ability_engine as AE
SV._CARDS_BY_NAME.update(M.build_card_index(M.load_cards())[0])
A=SV.load_model(sys.argv[1],'me')[0]; opps=sorted(glob.glob('decks/field/*.txt')); real=sys.stdout
N=int(sys.argv[2]); random.seed(11); c=collections.Counter()
orig=SV.do_attack
def hooked(pl, opp, log):
    if pl.name=='me':
        munk=[p for p in pl.in_play() if p.name=='Munkidori']
        dark=[p for p in munk if any('Darkness' in e for e in p.energy)]
        fuel=any(p.damage>=10 for p in pl.in_play())
        c['turns']+=1; c['munk_in_play']+=len(munk); c['munk_with_dark']+=len(dark)
        if fuel: c['powered_munk_with_fuel']+=len(dark)
        c['dark_in_hand']+=sum(1 for k,n in pl.hand if k=='Energy' and 'Darkness' in n)
    return orig(pl, opp, log)
SV.do_attack=hooked
uses=0
for i in range(N):
    B=SV.load_model(random.choice(opps),'o')[0]
    sys.stdout=io.StringIO(); SV.run_game(A,B,verbose=True); out=sys.stdout.getvalue(); sys.stdout=real
    uses+=out.count('me: Munkidori uses Adrena-Brain')
print({k: round(v/N,1) for k,v in c.items()}, '| Adrena-Brain uses per game', round(uses/N,1))
