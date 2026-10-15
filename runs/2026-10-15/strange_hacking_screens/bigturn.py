"""Per game: Prizes taken by each of my turns, and what each Strange Hacking took."""
import random, sys, io, glob, re, collections
sys.path.insert(0,'.')
import simulate_versus as SV, tcg_model as M
SV._CARDS_BY_NAME.update(M.build_card_index(M.load_cards())[0])
A=SV.load_model(sys.argv[1],'me')[0]; opps=sorted(glob.glob('decks/field/*.txt')); real=sys.stdout
N=int(sys.argv[2]); random.seed(11)
best=collections.Counter(); sh=collections.Counter(); wins=0; sh_used=0
for i in range(N):
    B=SV.load_model(random.choice(opps),'o')[0]
    sys.stdout=io.StringIO(); r=SV.run_game(A,B,verbose=True); out=sys.stdout.getvalue(); sys.stdout=real
    wins += r['winner']=='me'
    turns=re.split(r"^-- Turn \d+ \((me|o)\) --$", out, flags=re.M)
    top=0
    for j in range(1,len(turns),2):
        who, body = turns[j], turns[j+1]
        # Prizes I took during my turn and the checkup right after it
        took=sum(int(x) for x in re.findall(r"^  me: KO on .*\(\+(\d+) prizes?\)", body, re.M))
        took+=sum(int(x) for x in re.findall(r"^  o: .* KO'd at checkup \(\+(\d+) to me\)", body, re.M))
        if who=='me':
            top=max(top,took)
            if 'uses Strange Hacking' in body:
                sh_used+=1; sh[took]+=1
    best[top]+=1
print('wins',wins,'/',N,'| Strange Hacking used',sh_used)
print('most Prizes taken in one of my turns, per game:', dict(sorted(best.items())))
print('Prizes taken on Strange Hacking turns:', dict(sorted(sh.items())))
