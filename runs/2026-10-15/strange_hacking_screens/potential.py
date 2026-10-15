"""At the start of each of my attacks: counters on their board, and the Prizes one
Strange Hacking could take with them (whether or not Alakazam TWM is ready)."""
import random, sys, io, glob, collections
sys.path.insert(0,'.')
import simulate_versus as SV, tcg_model as M, ability_engine as AE
SV._CARDS_BY_NAME.update(M.build_card_index(M.load_cards())[0])
A=SV.load_model(sys.argv[1],'me')[0]; opps=sorted(glob.glob('decks/field/*.txt')); real=sys.stdout
N=int(sys.argv[2]); random.seed(11)
orig=SV.do_attack; rec=[]
def hooked(pl, opp, log):
    if pl.name=='me' and opp.active is not None:
        spots=opp.in_play(); pool=sum(s.damage for s in spots)
        ch,_=AE.plan_counter_knockouts(opp,[s for s in spots if s.damage>=10],spots)
        rec[-1].append((pool, sum(opp.POKEMON[c.name]['prize_value'] for c in ch)))
    return orig(pl, opp, log)
SV.do_attack=hooked
for i in range(N):
    B=SV.load_model(random.choice(opps),'o')[0]; rec.append([])
    sys.stdout=io.StringIO(); SV.run_game(A,B,verbose=False); sys.stdout=real
best=collections.Counter(max((p for _,p in g), default=0) for g in rec)
pools=sorted(max((c for c,_ in g), default=0) for g in rec)
print('max Prizes a Strange Hacking could take, best turn per game:', dict(sorted(best.items())))
print('largest pool of damage on their board per game: median', pools[len(pools)//2], ' 90th pct', pools[int(len(pools)*.9)], ' max', pools[-1])
