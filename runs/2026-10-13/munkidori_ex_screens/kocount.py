import random, sys, io, glob, re, collections
sys.path.insert(0,'.')
import simulate_versus as SV, tcg_model as M
SV._CARDS_BY_NAME.update(M.build_card_index(M.load_cards())[0])
A=SV.load_model(sys.argv[1],'me')[0]; opps=sorted(glob.glob('decks/field/*.txt')); real=sys.stdout
c=collections.Counter(); random.seed(5)
for i in range(int(sys.argv[2])):
    B=SV.load_model(random.choice(opps),'o')[0]
    sys.stdout=io.StringIO(); SV.run_game(A,B,verbose=True); out=sys.stdout.getvalue(); sys.stdout=real
    for m in re.finditer(r"KO on (Munkidori ex|Okidogi ex|Pecharunt ex) \(\+(\d) prizes?\)", out):
        # only KOs the OPPONENT made on my Pokemon: the line is in the o: block
        pass
    for line in out.splitlines():
        m=re.search(r"^  o: KO on (Munkidori ex|Okidogi ex|Pecharunt ex) \(\+(\d)", line)
        if m: c[(m.group(1), int(m.group(2)))]+=1
for k,v in sorted(c.items()): print(k, v)
