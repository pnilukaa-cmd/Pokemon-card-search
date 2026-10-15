"""Counter flow per game: Freezing Shroud counters on my board / theirs,
counters Munkidori's Adrena-Brain moved, and my Pokemon Knocked Out at checkup."""
import random, sys, io, glob, re, collections
sys.path.insert(0,'.')
import simulate_versus as SV, tcg_model as M, ability_engine as AE
SV._CARDS_BY_NAME.update(M.build_card_index(M.load_cards())[0])
A=SV.load_model(sys.argv[1],'me')[0]; opps=sorted(glob.glob('decks/field/*.txt')); real=sys.stdout
N=int(sys.argv[2]); random.seed(11)
tot=collections.Counter()
orig_apply=AE.apply_action
def hooked(act, pl, opp, source, log, *a, **k):
    if act.op==AE.IR.Op.PLACE_COUNTERS and (act.filter or {}).get('has_ability'):
        before={id(s):s.damage for s in pl.in_play()+opp.in_play()}
        r=orig_apply(act, pl, opp, source, log, *a, **k)
        me = pl if pl.name=='me' else opp; them = opp if me is pl else pl
        tot['shroud_on_me']+=sum(s.damage-before.get(id(s),s.damage) for s in me.in_play())//10
        tot['shroud_on_them']+=sum(s.damage-before.get(id(s),s.damage) for s in them.in_play())//10
        return r
    if act.op==AE.IR.Op.MOVE_COUNTERS and pl.name=='me' and (act.filter or {}).get('from')==AE.IR.Target.YOUR_ANY:
        before=sum(s.damage for s in pl.in_play())
        r=orig_apply(act, pl, opp, source, log, *a, **k)
        tot['adrena_moved']+=(before-sum(s.damage for s in pl.in_play()))//10
        tot['adrena_uses']+=1 if r else 0
        return r
    return orig_apply(act, pl, opp, source, log, *a, **k)
AE.apply_action=hooked
wins=0
for i in range(N):
    B=SV.load_model(random.choice(opps),'o')[0]
    sys.stdout=io.StringIO(); r=SV.run_game(A,B,verbose=True); out=sys.stdout.getvalue(); sys.stdout=real
    wins+=r['winner']=='me'
    tot['my_checkup_KOs']+=len(re.findall(r"^  me: .* KO'd at checkup", out, re.M))
print('wins',wins,'/',N, '| per game:', {k: round(v/N,1) for k,v in sorted(tot.items())})
