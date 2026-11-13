"""How the four confirmed additions are used: 10 logged games against each of
the eight opponents in opps8.txt."""
import sys, os, io, random, contextlib, re, collections
R = "/home/user/Pokemon-card-search"; sys.path.insert(0, R); os.chdir(R)
import simulate_versus as SV, tcg_model as M
SV._CARDS_BY_NAME.update(M.build_card_index(M.load_cards())[0])
S = "/tmp/claude-0/-home-user-Pokemon-card-search/32313191-2e9b-5f12-921b-86b3863481b6/scratchpad"
opps = [l.split("/")[-1][:-4] for l in open(f"{S}/fr/opps8.txt").read().split()]
for var, pats in [
    ("feraligatr_munkidori_damage_transfer__wishiwashi", ["Wishiwashi ex uses Hydro Splash", "Oceanic Gain", "Wishiwashi ex.*(?:Knocked Out|is KO)"]),
    ("kyurem_vanilluxe_blizzard__wishiwashi", ["Wishiwashi ex uses Hydro Splash", "Oceanic Gain", "Wishiwashi ex.*(?:Knocked Out|is KO)"]),
    ("munkidori_ex_pecharunt_chains__pyroduct", ["Legendary Pyroduct"]),
    ("team_rocket_hypno_exeggutor__pyroduct", ["Legendary Pyroduct"])]:
    me = var.split("__")[0]
    A = SV.load_model(f"{S}/dlr2/var/{var}.txt", me)[0]
    cnt = collections.Counter(); wins = games = 0
    for o in opps:
        B = SV.load_model(f"{R}/decks/field/{o}.txt", o)[0]
        random.seed(hash((var, o)) & 0xffff)
        for g in range(10):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                r = SV.run_game(A, B, verbose=True)
            log = buf.getvalue(); games += 1; wins += r["winner"] == me
            for p in pats:
                cnt[p] += len(re.findall(r"me?.*" + p if False else p, log))
            cnt["_any_line"] += 0
    print(var, f"wins {wins}/{games}", {k: round(v / games, 2) for k, v in cnt.items() if not k.startswith("_")})
