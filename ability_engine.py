#!/usr/bin/env python3
"""Executes compiled ability IR against a running game.

ability_ir.py turns card text into Effect/Action objects. This module is
the other half: it takes those objects and actually changes game state.
Keeping the two apart is the point of the design -- supporting a new card
shape means adding a RULE in ability_ir.py and, at most, one `op` handler
here. The simulator itself never grows card-specific code.

Two execution modes, because Pokemon effects come in two flavours:

  ACTIVATED -- ONCE_PER_TURN / ON_EVOLVE / ON_DAMAGED / ON_PLAY. These are
  run by `activate(...)`, which checks conditions, pays costs, then applies
  each Action in order.

  PASSIVE -- REDUCE_DAMAGE, BUFF_DAMAGE, PREVENT_DAMAGE, MODIFY_RETREAT,
  LOCK and friends never "happen"; they are continuously true. Those are
  QUERIED at the moment they matter (during damage calculation, during a
  retreat) via the `query_*` functions rather than executed.

The runtime is deliberately duck-typed against the simulator's existing
Player/InPlay objects rather than defining its own board representation,
so wiring it in did not require rewriting the engine.

Ops with no handler here are counted in `UNEXECUTED_OPS` and reported, so
"the IR understood this card" and "the engine can act on it" stay
separate, honestly-measured things.
"""
import random
from collections import Counter

import ability_ir as IR

STARTING_PRIZES = 6

# Ops that compiled but that the runtime has no handler for. Reported by
# the simulator so a compiled-but-inert ability is never mistaken for one
# that actually did something.
UNEXECUTED_OPS = Counter()

# Compiled IR for a Trainer / Tool / Energy card by name. Injected by the
# simulator at import time: simulate_versus imports this module, so this
# module cannot import it back to reach trainer_effect_ir. Defaults to
# "nothing compiles", which keeps this module importable on its own.
def TRAINER_IR(name):
    return None


# How much this player wants to KEEP a card in hand, low = pitch it first.
# Injected by the simulator, which is where deck knowledge lives. Defaults
# to "no preference", which reproduces the old blind behaviour.
def PITCH_RANK(pl, kind, name):
    return 0



# --------------------------------------------------------------------------
# Target resolution
# --------------------------------------------------------------------------

def resolve_targets(target, pl, opp, source, attacker=None):
    """Map an IR Target onto concrete in-play Pokemon."""
    T = IR.Target
    if target == T.SELF:
        return [source] if source else []
    if target == T.YOUR_ACTIVE:
        return [pl.active] if pl.active else []
    if target == T.YOUR_BENCHED:
        return list(pl.bench)
    if target in (T.YOUR_ANY, T.YOUR_ALL):
        return pl.in_play()
    if target == T.OPP_ACTIVE:
        return [opp.active] if opp.active else []
    if target == T.OPP_BENCHED:
        return list(opp.bench)
    if target in (T.OPP_ANY, T.OPP_ALL):
        return opp.in_play()
    if target == T.ATTACKING_POKEMON:
        return [attacker] if attacker else []
    if target == T.BOTH_ALL:
        return pl.in_play() + opp.in_play()
    return []


def matches_filter(pl, spot, filt):
    """Does this Pokemon satisfy an Action's filter (type / family)?"""
    if not filt:
        return True
    info = pl.POKEMON.get(spot.name, {})
    fam = filt.get("family")
    if fam and fam.lower() not in spot.name.lower():
        return False
    typ = filt.get("type")
    if typ and typ not in (info.get("types") or []):
        return False
    not_typ = filt.get("type_not")
    if not_typ and not_typ in (info.get("types") or []):
        return False
    if filt.get("stage") and info.get("stage") != filt["stage"]:
        return False
    if filt.get("stage_not") and info.get("stage") == filt["stage_not"]:
        return False
    return True


# --------------------------------------------------------------------------
# Conditions and costs
# --------------------------------------------------------------------------

def query_weakness_override(attacker_player, defender_player, defender_spot):
    """The Weakness a defending Pokemon has right now, or None.

    Lillie's Clefairy ex's Fairy Zone rewrites the Weakness of every Dragon
    Pokemon your opponent has in play. The op compiled and was listed as a
    known passive, and nothing ever asked for it -- so a card whose entire
    job is to make the mirror's Dragapult ex fall to a Psychic attack did
    nothing at all.
    """
    info = defender_player.POKEMON.get(defender_spot.name) or {}
    types = info.get("types") or []
    for holder, eff, act in _passive_actions(attacker_player,
                                             IR.Op.SET_WEAKNESS):
        if not conditions_met(eff, attacker_player, defender_player, holder):
            continue
        want = (act.filter or {}).get("from_type")
        if want and want not in types:
            continue
        to = (act.filter or {}).get("to_type")
        if to:
            return to
    return None

def query_condition_immunity(pl, spot, condition, opp=None):
    """Is this Pokemon immune to being given this Special Condition?

    CONDITION_IMMUNITY was in the same state ATTACK_TWICE was: the op
    compiled, it sat in the known-passive list so nothing reported it as
    missing, and no caller ever asked. Every "can't be Paralyzed" Ability,
    every Antique Fossil, Bubbly Water Energy and Festival Grounds were
    inert.

    Three sources, because immunity is printed on three kinds of card:
    an Ability on something in play, a Tool or Energy attached to the
    Pokemon itself, and the Stadium (which shelters BOTH players).
    """
    for holder, eff, act in _passive_actions(pl, IR.Op.CONDITION_IMMUNITY):
        if not conditions_met(eff, pl, opp or pl, holder):
            continue
        if act.target == IR.Target.SELF and holder is not spot:
            continue
        if act.target in (IR.Target.YOUR_ALL, IR.Target.BOTH_ALL):
            if not matches_filter(pl, spot, act.filter):
                continue
        if condition in ((act.filter or {}).get("conditions") or []):
            return True

    if _attached_grants_immunity(pl, spot, condition):
        return True

    # The Stadium is shared, so either player's copy shelters this spot.
    stadium = getattr(pl, "stadium", None) or (
        getattr(opp, "stadium", None) if opp is not None else None)
    if stadium and _stadium_grants_immunity(pl, spot, condition, stadium):
        return True
    return False


def _attached_grants_immunity(pl, spot, condition):
    """Immunity printed on a Tool or Energy attached to this Pokemon."""
    names = []
    tool = getattr(spot, "tool", None)
    if tool:
        names.append(tool)
    names.extend(getattr(spot, "energy_names", None) or [])
    for name in names:
        eff = TRAINER_IR(name)
        if eff is None or eff.unsupported:
            continue
        for act in eff.actions:
            if act.op is IR.Op.CONDITION_IMMUNITY and condition in (
                    (act.filter or {}).get("conditions") or []):
                return True
    return False


def _stadium_grants_immunity(pl, spot, condition, stadium):
    eff = TRAINER_IR(stadium)
    if eff is None or eff.unsupported:
        return False
    for act in eff.actions:
        if act.op is not IR.Op.CONDITION_IMMUNITY:
            continue
        if condition not in ((act.filter or {}).get("conditions") or []):
            continue
        if (act.filter or {}).get("requires_energy") and not spot.energy:
            continue
        return True
    return False


def query_attacks_twice(pl, spot, opp=None):
    """May this Pokemon use its attack twice this turn?

    Dipplin, Seaking and Goldeen all carry Festival Lead, whose whole text
    is "if Festival Grounds is in play, this Pokemon may use an attack it
    has twice". The op compiled, was catalogued as a known passive, and
    nothing ever asked for it -- so an entire archetype dealt exactly half
    its damage.
    """
    for holder, eff, act in _passive_actions(pl, IR.Op.ATTACK_TWICE):
        if holder is not spot:
            continue
        if not conditions_met(eff, pl, opp or pl, holder):
            continue
        return True
    return False

def query_attack_gate(pl, spot):
    """False when an Ability forbids this Pokemon from attacking.

    "This Pokemon can't attack unless you have 4 or more Team Rocket's
    Pokemon in play" is a standing requirement re-checked every turn, not
    a one-off lock.
    """
    for holder, eff, act in _passive_actions(pl, IR.Op.ATTACK_GATE):
        if holder is not spot:
            continue            # the gate is on its own Pokemon only
        if True:
            fam = (act.filter or {}).get("family", "").lower()
            names = pl.in_play_names()
            if fam in ("", "pokemon", "pokémon"):
                have = len(names)
            else:
                have = sum(1 for n in names if fam in n.lower())
            if have < (act.amount or 0):
                return False
    return True

def conditions_met(effect, pl, opp, source, atk=None):
    for c in effect.conditions:
        k = c["kind"]
        if k == "self_is_active" and source is not pl.active:
            return False
        if k == "self_is_benched" and source not in pl.bench:
            return False
        if k == "lost_pokemon_last_turn":
            if not getattr(pl, "lost_pokemon_last_turn", False):
                return False
            fam = c.get("family")
            if fam and fam.lower() not in (
                    getattr(pl, "lost_pokemon_names", None) or ""):
                return False
        if k == "named_in_play" and c["name"] not in pl.in_play_names():
            return False
        if k == "played_this_turn" and c["name"] not in getattr(pl, "played_supporters_this_turn", set()):
            return False
        if k == "self_has_energy_type":
            if not any(c["type"] in e for e in source.energy):
                return False
        if k == "energy_in_play_at_least":
            have = sum(1 for p in pl.in_play() for e in p.energy if c["type"] in e)
            if have < c["count"]:
                return False
        if k == "opponent_active_is_type":
            if not opp.active:
                return False
            types = (opp.POKEMON.get(opp.active.name) or {}).get("types") or []
            if c["type"] not in types:
                return False
        if k == "self_has_tool" and not getattr(source, "tool", None):
            return False
        if k == "self_extra_energy":
            # "at least N extra Energy attached (in addition to THIS
            # ATTACK'S cost)" -- so it needs the attack being scored, which
            # is why conditions_met takes an optional atk. Falling back to
            # the Pokemon's most expensive attack when it is not given.
            if atk is not None:
                cost = len(atk["cost"])
            else:
                costs = [len(a["cost"]) for a in
                         (pl.POKEMON.get(source.name) or {}).get("attacks") or []]
                cost = max(costs) if costs else 0
            if source.energy_count() - cost < c["count"]:
                return False
        if k == "self_promoted_this_turn" and not getattr(
                source, "promoted_this_turn", False):
            return False
        if k == "any_stadium_in_play":
            if not (getattr(pl, "stadium", None) or getattr(opp, "stadium", None)):
                return False
        if k == "self_used_attack_last_turn":
            if getattr(source, "last_attack_used", None) != c["name"]:
                return False
        if k == "played_supporter_named":
            played = getattr(pl, "played_supporters_this_turn", set())
            if not any(c["name"].lower() in n.lower() for n in played):
                return False
        if k == "stadium_in_play":
            want = c["name"]
            if want not in (getattr(pl, "stadium", None),
                            getattr(opp, "stadium", None)):
                return False
        if k == "healed_this_turn" and not getattr(source, "healed_this_turn", False):
            return False
        if k == "self_full_hp":
            # "If this Pokemon has full HP and would be Knocked Out" is
            # about the state the attack FOUND it in. Checking damage
            # after the hit has landed makes the clause never true, which
            # is why every Endure Ability in the pool was inert.
            before = getattr(source, "prev_damage", None)
            if (before if before is not None else source.damage) > 0:
                return False
        if k == "active_is_type":
            if not pl.active:
                return False
            if c["type"] not in (pl.POKEMON.get(pl.active.name, {}).get("types") or []):
                return False
        if k == "self_hp_at_or_below":
            hp = pl.POKEMON[source.name]["hp"]
            if hp - source.damage > c["hp"]:
                return False
        if k == "opponent_has_in_play":
            if not any(c["what"].lower() in n.lower() for n in opp.in_play_names()):
                return False
        if k == "own_prizes_equal" and getattr(pl, "prizes", None) != c["count"]:
            return False
        if k == "named_ability_in_discard":
            want = c["ability"].lower()
            n = 0
            for name in pl.discard:
                for ab in (pl.POKEMON.get(name, {}).get("abilities") or []):
                    if (ab.get("name") or "").lower() == want:
                        n += 1
                        break
            if n < c["count"]:
                return False
        if k == "opponent_active_is_ex":
            if opp is pl or not opp.active:
                return False
            if opp.POKEMON[opp.active.name]["prize_value"] < 2:
                return False
        if k == "opponent_hand_size":
            if opp is pl:
                return False      # no opponent in view: fail closed, never guess
            n, want = len(opp.hand), c["count"]
            if c["op"] == "==" and n != want:
                return False
            if c["op"] == ">=" and n < want:
                return False
            if c["op"] == "<=" and n > want:
                return False
    return True


def pay_costs(effect, pl, source, log):
    """Returns True if every cost could be paid (and pays them)."""
    # Check affordability first so a partial payment never happens.
    for c in effect.costs:
        k = c["kind"]
        if k == "discard_hand" and len(pl.hand) < c["amount"]:
            return False
        if k == "discard_energy_from_hand":
            if not any(kind == "Energy" and c["type"] in name
                       for kind, name in pl.hand):
                return False
        if k == "discard_energy_from_self":
            if not any(c["type"] in e for e in source.energy):
                return False
    for c in effect.costs:
        k = c["kind"]
        if k == "discard_hand":
            # Pitch the least useful cards, not hand[0]. Paying blind, N's
            # Zoroark ex's Trade fed 282 Darkness Energy and 183 copies of
            # the deck's own attacker to the discard over 300 games -- in a
            # deck holding 8 Energy that could not pay for its attack on
            # 528 turns. Every "discard a card from your hand" cost in the
            # format was doing this.
            order = sorted(range(len(pl.hand)),
                           key=lambda i: (PITCH_RANK(pl, *pl.hand[i]), i))
            for i in sorted(order[:c["amount"]], reverse=True):
                pl.discard.append(pl.hand.pop(i)[1])
        elif k == "discard_energy_from_hand":
            i = next(i for i, (kind, name) in enumerate(pl.hand)
                     if kind == "Energy" and c["type"] in name)
            pl.discard.append(pl.hand.pop(i)[1])
        elif k == "discard_energy_from_self":
            i = next(i for i, e in enumerate(source.energy) if c["type"] in e)
            source.energy.pop(i)
            if getattr(source, "energy_names", None):
                source.energy_names.pop(i)
    return True


# --------------------------------------------------------------------------
# Action handlers
# --------------------------------------------------------------------------

def _find_in_deck(pl, pred):
    for i, (k, n) in enumerate(pl.deck):
        if pred(k, n):
            card = pl.deck.pop(i)
            random.shuffle(pl.deck)
            return card
    return None


# The counter total the format's "exactly N counters" Knock Out effects
# key off (Mega Absol ex's Terminal Period, Glaceon ex's Euclase).
KO_THRESHOLD = 60


def apply_action(act, pl, opp, source, log, attacker=None, make_inplay=None):
    O = IR.Op
    op = act.op

    if op == O.DRAW:
        target_size = act.filter.get("up_to_hand_size")
        before = len(pl.hand)
        if target_size is not None:
            while len(pl.hand) < target_size and pl.deck:
                pl.draw(1)
        else:
            pl.draw(act.amount or 1)
            if act.target == IR.Target.BOTH_ALL:
                opp.draw(act.amount or 1)
        log.append(f"    draw {len(pl.hand) - before}")
        return True

    if op == O.PLACE_COUNTERS:
        hits = resolve_targets(act.target, pl, opp, source, attacker)
        per = act.filter.get("per_discard_card")
        if per:
            # "2 damage counters for each Basic Grass Energy card in your
            # discard pile" -- count the fuel, then (Re-Brew) spend it.
            want = per.replace("basic ", "").strip()
            fuel = [c for c in pl.discard if want in c.lower()]
            if not fuel or not hits:
                return False
            target = max(hits, key=lambda h: pl.POKEMON.get(h.name, {}).get("hp", 0))
            target.damage += (act.amount or 0) * 10 * len(fuel)
            log.append(f"    place {(act.amount or 0) * 10 * len(fuel)} damage "
                       f"({len(fuel)} {want} in discard)")
            if act.filter.get("consumes_fuel"):
                for c in fuel:
                    pl.discard.remove(c)
                    pl.deck.append((("Energy"), c))
                random.shuffle(pl.deck)
                log.append(f"    {len(fuel)} {want} shuffled back into the deck")
            return True
        # A "put N damage counters ... in any way you like" budget is
        # SPLIT across targets, and how it is split decides whether the
        # attack takes a Prize or nothing. The old rule topped Pokemon up
        # toward a flat KO_THRESHOLD of 60 regardless of their real HP,
        # and sorted so that an UNDAMAGED Pokemon outranked one five
        # counters from dying: Phantom Dive put all six on a fresh 70 HP
        # Basic while two sat at 20, and Knocked Out nothing.
        if act.filter.get("distribute") and (act.amount or 0) > 0:
            budget = act.amount
            pool = [h for h in hits if h is not None]
            owner = opp
            def _left(h):
                hp = (owner.POKEMON.get(h.name) or {}).get("hp") or 0
                return max(0, hp - h.damage)
            def _prize(h):
                return (owner.POKEMON.get(h.name) or {}).get("prize_value", 1)
            # Finish whatever can be finished, richest Prize first, then
            # cheapest to finish.
            placed = 0
            for h in sorted(pool, key=lambda x: (-_prize(x), _left(x))):
                need = (_left(h) + 9) // 10
                if 0 < need <= budget:
                    h.damage += need * 10
                    budget -= need
                    placed += need
            # Anything left goes on the most valuable survivor, which is
            # what sets up next turn's Knock Out.
            if budget:
                alive = [h for h in pool if _left(h) > 0]
                if alive:
                    tgt = max(alive, key=lambda x: (_prize(x), -_left(x)))
                    tgt.damage += budget * 10
                    placed += budget
            if placed:
                log.append(f"    place {placed * 10} damage, split to finish "
                           f"what it could")
            return placed > 0

        if act.target == IR.Target.OPP_ALL:
            chosen = hits
        else:
            # "choose N of your opponent's Pokemon and put X on each"
            n = act.filter.get("targets", 1)
            # Focus fire toward a cash-in total rather than sprinkling.
            # A counter-placement deck is building one target up to an
            # exact threshold (Mega Absol ex's Terminal Period wants
            # exactly 60), so top up whoever is closest to it from below
            # and only spread once nobody is a candidate.
            step = (act.amount or 0) * 10
            def _priority(h):
                room = KO_THRESHOLD - h.damage
                if 0 < room and room >= step:
                    return (0, room)          # can still climb toward it
                return (1, -(pl.POKEMON.get(h.name, {}).get("hp", 0) - h.damage))
            chosen = sorted(hits, key=_priority)[:n]
        # Mega Zygarde ex's Nullifying Zero flips a separate coin for each
        # of the opponent's Pokemon. Without this the attack either always
        # landed on everything or (as compiled) did nothing at all.
        odds = act.filter.get("chance_each")
        if odds is not None:
            chosen = [h for h in chosen if random.random() < odds]
        # Arboliva ex's Oil Salvo chooses a target SIX times and says the
        # same Pokemon may be chosen more than once, so a 5-Pokemon board
        # still takes all six hits. Truncating to distinct targets lost a
        # third of the attack.
        want = act.filter.get("targets")
        if want and chosen and len(chosen) < want:
            chosen = [chosen[i % len(chosen)] for i in range(want)]
        for h in chosen:
            h.damage += (act.amount or 0) * 10
        if chosen:
            log.append(f"    place {(act.amount or 0)*10} damage on "
                       f"{len(chosen)} Pokemon")
        return bool(chosen)

    if op == O.CONDITIONAL_KO:
        # Terminal Period / Euclase: a Knock Out keyed off an exact counter
        # total, ignoring HP entirely. Resolution lives in the match loop
        # (it takes Prizes); this only reports whether it is live.
        return False

    if op == O.MOVE_COUNTERS:
        src = act.filter.get("from")
        if src in (IR.Target.OPP_BENCHED, IR.Target.OPP_ANY, IR.Target.OPP_ALL):
            pool = opp.bench if src == IR.Target.OPP_BENCHED else opp.in_play()
        else:
            pool = pl.in_play()
        donors = [q for q in pool if q.damage >= 10]
        hits = resolve_targets(act.target, pl, opp, source, attacker) or \
            ([opp.active] if opp.active else [])
        if not donors or not hits:
            return False
        donor = max(donors, key=lambda q: q.damage)
        if act.filter.get("any_number"):
            amount = donor.damage        # "any number" -- take it all
        else:
            amount = min((act.amount or 0) * 10, donor.damage)
        donor.damage -= amount
        hits[0].damage += amount
        log.append(f"    move {amount} damage {donor.name} -> {hits[0].name}")
        return True

    if op == O.HEAL:
        hits = resolve_targets(act.target, pl, opp, source, attacker)
        healed = 0
        for h in hits:
            amt = h.damage if act.filter.get("all") else min(h.damage, (act.amount or 0))
            h.damage -= amt
            healed += amt
            if amt:
                # Lurantis ex's Lively Cutter is 60 that becomes 260 "if
                # this Pokemon was healed during this turn", and nothing
                # recorded that it had been.
                h.healed_this_turn = True
        if healed:
            log.append(f"    heal {healed}")
        return healed > 0

    if op == O.DISCARD_SELF_ENERGY:
        if source is None or not source.energy:
            return False
        want = (act.filter or {}).get("type")
        idxs = [i for i in range(len(source.energy))
                if not want or want in source.energy[i]]
        if act.amount is not None:
            idxs = idxs[:act.amount]
        for i in sorted(idxs, reverse=True):
            source.energy.pop(i)
            pl.discard.append("Energy")
        if idxs:
            log.append(f"    {source.name} discards {len(idxs)} Energy")
        return bool(idxs)

    if op == O.SELF_DAMAGE:
        if source is not None:
            source.damage += act.amount or 0
            log.append(f"    {source.name} takes {act.amount} recoil")
            return True
        return False

    if op == O.ATTACH_ENERGY:
        src = act.filter.get("from")
        want_type = act.filter.get("type")
        card = None
        if src == "hand":
            i = next((i for i, (k, n) in enumerate(pl.hand)
                      if k == "Energy" and (not want_type or want_type in n)), None)
            if i is not None:
                card = pl.hand.pop(i)
        elif src == "discard":
            nm = next((n for n in pl.discard
                       if n.endswith("Energy") and (not want_type or want_type in n)), None)
            if nm:
                pl.discard.remove(nm)
                card = ("Energy", nm)
        else:  # deck
            card = _find_in_deck(pl, lambda k, n: k == "Energy" and (not want_type or want_type in n))
        if not card:
            return False
        hits = resolve_targets(act.target, pl, opp, source, attacker) or [source]
        tgt = hits[0] if hits else source
        if tgt is None:
            return False
        tgt.energy.append([want_type] if want_type else list(IR.TYPES.split("|")))
        if getattr(tgt, "energy_names", None) is not None:
            tgt.energy_names.append(card[1])
        log.append(f"    attach {card[1]} to {tgt.name}")
        return True

    if op == O.MOVE_ENERGY:
        srcs = [q for q in pl.in_play() if q.energy and q is not pl.active]
        if not srcs or not pl.active:
            return False
        donor = srcs[0]
        n = len(donor.energy) if act.filter.get("any_amount") else min(act.amount or 1, len(donor.energy))
        for _ in range(n):
            pl.active.energy.append(donor.energy.pop())
            if getattr(donor, "energy_names", None):
                pl.active.energy_names.append(donor.energy_names.pop())
        log.append(f"    move {n} Energy {donor.name} -> {pl.active.name}")
        return True

    if op == O.SEARCH_TO_BENCH:
        placed = []
        for _ in range(act.amount or 1):
            if len(pl.bench) >= 5:
                break
            want = act.filter.get("name_contains")
            stage = act.filter.get("stage", "Basic")
            ptype = act.filter.get("type")

            def pred(k, n, want=want, stage=stage, ptype=ptype):
                if k != "Pokemon":
                    return False
                info = pl.POKEMON.get(n, {})
                # Only a Basic can go straight onto the Bench, whatever the
                # card's own wording says.
                if info.get("stage") != "Basic":
                    return False
                if stage not in (None, "Basic") and info.get("stage") != stage:
                    return False
                if ptype and ptype not in (info.get("types") or []):
                    return False
                return not want or want.lower() in n.lower()

            card = _find_in_deck(pl, pred)
            if not card:
                break
            if make_inplay:
                pl.bench.append(make_inplay(card[1]))
                placed.append(card[1])
        if placed:
            log.append(f"    bench {', '.join(placed)}")
        return bool(placed)

    if op == O.SEARCH_TO_HAND:
        got = []
        for _ in range(act.amount or 1):
            want = act.filter.get("name_contains")
            kind = (act.filter.get("kind") or "").lower()
            def pred(k, n, want=want, kind=kind):
                if kind.startswith("pok") and k != "Pokemon":
                    return False
                if kind == "energy" and k != "Energy":
                    return False
                # "Tool" is its own kind in the deck model (a Pokemon Tool
                # is an Item subtype but the model splits it out), and this
                # predicate did not know the word -- so a search naming a
                # Tool matched anything at all.
                if kind in ("supporter", "item", "stadium", "tool") \
                        and k.lower() != kind:
                    return False
                return not want or want.lower() in n.lower()
            card = _find_in_deck(pl, pred)
            if not card:
                break
            pl.hand.append(card)
            got.append(card[1])
        if got:
            log.append(f"    search {', '.join(got)}")
        return bool(got)

    if op == O.SWAP_IN_PLACE:
        # The discarded Pokemon takes over a board position outright: the
        # card says attachments, damage counters, Special Conditions and
        # turns in play all remain, so only the NAME changes. Everything
        # else about the spot is left exactly as it was.
        f = act.filter or {}

        def ok(name):
            info = pl.POKEMON.get(name)
            if not info:
                return False
            if f.get("stage") and info.get("stage") != f["stage"]:
                return False
            if f.get("family") and f["family"].lower() not in name.lower():
                return False
            if f.get("rule_box") and info.get("prize_value", 1) < 2:
                return False
            return True

        spots = [p for p in pl.in_play() if ok(p.name)]
        cand = sorted({n for n in pl.discard if ok(n)})
        if not spots or not cand:
            return False

        # The point of the card is to put a big body where the Energy
        # already is, so score the PAIR: HP gained, heavily weighted by
        # what is already attached to that spot and by whether it is the
        # one doing the attacking. Swapping a 1-Prize Basic for a 2-Prize
        # one hands the opponent an extra Prize, so that is priced in.
        def score(spot, n):
            info, cur = pl.POKEMON[n], pl.POKEMON[spot.name]
            gain = info["hp"] - cur["hp"]
            if gain <= 0:
                return None
            v = gain + 50 * spot.energy_count()
            if spot is pl.active:
                v += 25
            v -= 120 * (info.get("prize_value", 1) - cur.get("prize_value", 1))
            return v

        pairs = [(score(sp, n), sp, n) for sp in spots for n in cand]
        pairs = [x for x in pairs if x[0] is not None and x[0] > 0]
        if not pairs:
            return False
        _, spot, best = max(pairs, key=lambda x: (x[0], x[2]))
        pl.discard.remove(best)
        pl.discard.append(spot.name)
        log.append(f"    swap {spot.name} -> {best} (keeps "
                   f"{spot.energy_count()} Energy, {spot.damage} damage)")
        spot.name = best
        return True

    if op == O.FROM_DISCARD_TO_HAND:
        got = []
        for _ in range(act.amount or 1):
            nm = next((n for n in pl.discard if n in pl.POKEMON), None)
            if not nm:
                break
            pl.discard.remove(nm)
            pl.hand.append(("Pokemon", nm))
            got.append(nm)
        return bool(got)

    if op == O.MILL_OPPONENT:
        n = min(act.amount or 1, len(opp.deck))
        for _ in range(n):
            opp.discard.append(opp.deck.pop()[1])
        if n:
            log.append(f"    mill {n} from opponent")
        return n > 0

    if op == O.SWITCH:
        if act.filter.get("gust"):
            if opp.bench and opp.active:
                tgt = min(opp.bench, key=lambda p: opp.POKEMON[p.name]["hp"] - p.damage)
                opp.bench.remove(tgt)
                opp.bench.append(opp.active)
                opp.active = tgt
                log.append(f"    gust up {tgt.name}")
                return True
            return False
        if pl.bench and pl.active:
            tgt = pl.bench.pop(0)
            pl.bench.append(pl.active)
            pl.active = tgt
            return True
        return False

    if op == O.SHUFFLE_SELF_INTO_DECK:
        if source is None:
            return False
        pl.deck.append(("Pokemon", source.name))
        if source is pl.active:
            pl.active = pl.bench.pop(0) if pl.bench else None
        elif source in pl.bench:
            pl.bench.remove(source)
        random.shuffle(pl.deck)
        return True

    if op == O.DISCARD_ENERGY_FROM_OPPONENT:
        hits = resolve_targets(act.target, pl, opp, source, attacker)
        # "Discard an Energy from 1 of your opponent's Pokemon" lets you
        # CHOOSE which. Taking hits[:1] took whatever happened to be first
        # -- usually an Active with nothing attached -- so the card fizzled
        # and was never even spent. Crushing Hammer was attempted 255 times
        # in 30 games and resolved zero.
        if act.target in (IR.Target.OPP_ANY, IR.Target.OPP_ALL):
            hits = sorted(hits, key=lambda h: -len(getattr(h, "energy", [])))
        n = 0
        for h in hits[:1]:
            for _ in range(act.amount or 1):
                if h.energy:
                    h.energy.pop()
                    if getattr(h, "energy_names", None):
                        opp.discard.append(h.energy_names.pop())
                    n += 1
        if n:
            log.append(f"    discard {n} Energy from opponent")
        return n > 0

    if op == O.DISCARD_FROM_OPPONENT:
        # "until they have N cards in their hand" is an absolute floor, not
        # a count to remove -- and a hand already at or below it discards
        # nothing at all, so the card must not be spent.
        down_to = (act.filter or {}).get("down_to")
        if down_to is not None:
            n = max(0, len(opp.hand) - down_to)
        else:
            n = min(act.amount or 1, len(opp.hand))
        for _ in range(n):
            kind, name = opp.hand.pop(random.randrange(len(opp.hand)))
            # "shuffles them into their deck" vs discard -- the IR records
            # which, because returning a card to the deck is weaker.
            if act.filter.get("to") == "deck":
                opp.deck.append((kind, name))
            else:
                opp.discard.append(name)
        if n and act.filter.get("to") == "deck":
            random.shuffle(opp.deck)
        if n:
            log.append(f"    strip {n} card(s) from opponent's hand")
        return n > 0

    if op == O.SEARCH_TO_TOP_OF_DECK:
        # A generic want-list, because the card names no restriction: a
        # Basic while the board is still thin, then a Supporter if the
        # hand has none, then Energy, then anything. The cards go on TOP
        # (pl.deck[-1] is the next draw), so this is next turn's draw
        # being chosen rather than this turn's hand.
        def wants():
            if len(pl.in_play()) < 3:
                yield lambda k, n: (k == "Pokemon"
                                    and pl.POKEMON.get(n, {}).get("stage")
                                    == "Basic")
            if not any(k == "Supporter" for k, _ in pl.hand):
                yield lambda k, n: k == "Supporter"
            if not any(k == "Energy" for k, _ in pl.hand):
                yield lambda k, n: k == "Energy"
            yield lambda k, n: True

        picked = []
        for pred in wants():
            if len(picked) >= (act.amount or 1):
                break
            card = _find_in_deck(pl, pred)
            if card:
                picked.append(card)
        while len(picked) < (act.amount or 1):
            card = _find_in_deck(pl, lambda k, n: True)
            if not card:
                break
            picked.append(card)
        if not picked:
            return False
        pl.deck.extend(picked)          # last appended is drawn first
        log.append(f"    to top of deck: {', '.join(c[1] for c in picked)}")
        return True

    if op == O.REROLL_PRIZES:
        n = len(getattr(pl, "prize_cards", []) or [])
        if not n or len(pl.deck) < n:
            return False
        old = pl.prize_cards
        random.shuffle(old)
        pl.deck = old + pl.deck          # index 0 is the BOTTOM of the deck
        pl.prize_cards = [pl.deck.pop() for _ in range(n)]
        log.append(f"    re-roll {n} Prize cards")
        return True

    if op == O.DISCARD_TO_DECK:
        f = act.filter or {}
        want, typ = f.get("kind"), f.get("type")

        def ok(name):
            if want == "Pokemon":
                if name not in pl.POKEMON:
                    return False
                return not typ or typ in (pl.POKEMON[name].get("types") or [])
            if not name.endswith("Energy"):
                return False
            return not typ or typ in name

        moved = 0
        for name in [n for n in list(pl.discard) if ok(n)][:act.amount or 1]:
            pl.discard.remove(name)
            pl.deck.append(("Pokemon" if want == "Pokemon" else "Energy", name))
            moved += 1
        if moved:
            random.shuffle(pl.deck)
            log.append(f"    shuffle {moved} {want} back into deck")
        return moved > 0

    if op == O.CLEAR_CONDITIONS:
        hits = [h for h in resolve_targets(act.target, pl, opp, source, attacker)
                if getattr(h, "conditions", None)]
        if not hits:
            return False
        for h in hits:
            h.conditions = set()
        log.append(f"    clear Special Conditions on {len(hits)}")
        return True

    if op == O.DISCARD_FROM_SELF:
        down_to = (act.filter or {}).get("down_to")
        n = (max(0, len(pl.hand) - down_to) if down_to is not None
             else min(act.amount or 1, len(pl.hand)))
        for _ in range(n):
            pl.discard.append(pl.hand.pop(random.randrange(len(pl.hand)))[1])
        if n:
            log.append(f"    discard {n} from own hand")
        return True          # a symmetric cost is paid even at zero

    if op == O.DEVOLVE:
        targets = resolve_targets(act.target, pl, opp, source, attacker)
        hit = 0
        for spot in targets:
            info = pl.POKEMON.get(spot.name) or opp.POKEMON.get(spot.name) or {}
            prev = info.get("evolves_from")
            if not prev:
                continue
            owner = pl if spot in pl.in_play() else opp
            # The Evolution card goes back to its owner's HAND (or, on
            # Espeon ex, is shuffled into their deck) -- it is never
            # discarded, and discarding it handed the opponent a free
            # Night Stretcher target instead of a card they have to
            # re-draw and re-play.
            if (act.filter or {}).get("to") == "deck":
                owner.deck.append(("Pokemon", spot.name))
                random.shuffle(owner.deck)
            else:
                owner.hand.append(("Pokemon", spot.name))
            spot.name = prev
            # Devolving clears damage above the lower stage's HP the same
            # way any HP change does, and Special Conditions stay.
            hit += 1
        if hit:
            log.append(f"    devolves {hit} Pokemon")
        return hit > 0

    if op == O.SEARCH_TO_DISCARD:
        n = 0
        for _ in range(act.amount or 1):
            card = _find_in_deck(pl, lambda k, nm: k == "Energy")
            if not card:
                break
            pl.discard.append(card[1])
            n += 1
        if n:
            log.append(f"    search {n} Energy to discard")
        return n > 0

    if op == O.REVEAL_OPPONENT_HAND:
        return False        # information only; no state change to model

    if op == O.DAMAGE_TO_HP_THRESHOLD:
        # "Put damage counters until its remaining HP is N." Counters, not
        # attack damage, so Weakness and damage reduction do not apply --
        # the same reason Matcha Spin goes through this path.
        hits = resolve_targets(act.target, pl, opp, source, attacker)
        placed = 0
        for spot in hits:
            hp = (opp.POKEMON.get(spot.name) or {}).get("hp") or 0
            want = max(0, hp - (act.amount or 0))
            if want > spot.damage:
                placed += want - spot.damage
                spot.damage = want
        if placed:
            log.append(f"    damage counters to {act.amount} HP remaining "
                       f"(+{placed})")
        return placed > 0

    if op == O.MULTIPLY_COUNTERS:
        hits = resolve_targets(act.target, pl, opp, source, attacker)
        if act.filter.get("targets"):
            # Pick the ones already carrying the most, since multiplying
            # nothing is worth nothing.
            hits = sorted(hits, key=lambda h: -h.damage)[:act.filter["targets"]]
        factor = act.amount or 2
        moved = 0
        for spot in hits:
            if spot.damage <= 0:
                continue
            before = spot.damage
            spot.damage *= factor
            moved += spot.damage - before
        if moved:
            log.append(f"    multiplies counters x{factor} (+{moved} damage)")
        return moved > 0

    if op == O.DISCARD_STADIUM:
        if getattr(pl, "stadium", None) or getattr(opp, "stadium", None):
            pl.stadium = None
            opp.stadium = None
            return True
        return False

    if op == O.SET_OPPONENT_HAND:
        # Their whole hand goes to the bottom of the deck, then they draw a
        # fixed number back. Vivillon's wording only redraws if they had
        # cards to put down, so an empty hand stays empty.
        if not opp.hand:
            return False
        opp.deck[:0] = opp.hand          # bottom of deck (deck draws off the end)
        opp.hand = []
        for _ in range(act.amount or 0):
            if opp.deck:
                opp.hand.append(opp.deck.pop())
        log.append(f"    opponent's hand reset to {len(opp.hand)}")
        return True

    if op == O.SWAP_HAND_WITH_DECK:
        if not pl.hand or not pl.deck:
            return False
        i = random.randrange(len(pl.hand))
        pl.hand[i], pl.deck[-1] = pl.deck[-1], pl.hand[i]
        return True

    if op == O.FORCE_BENCH_OPPONENT:
        placed = 0
        for kind, name in list(opp.hand):
            if len(opp.bench) >= 5:
                break
            if kind == "Pokemon" and opp.POKEMON.get(name, {}).get("stage") == "Basic":
                opp.hand.remove((kind, name))
                if make_inplay:
                    opp.bench.append(make_inplay(name))
                    placed += 1
        if placed:
            log.append(f"    force {placed} Basic(s) onto opponent's Bench")
        return placed > 0

    if op == O.APPLY_CONDITION:
        hits = resolve_targets(act.target, pl, opp, source, attacker)
        if not hits:
            return False
        conds = act.filter.get("conditions") or []
        if act.filter.get("choose_one") and conds:
            conds = [conds[0]]
        # Dark Bell hits BOTH Active Pokemon, and only those -- a board-wide
        # target with an "active_only" restriction, since there is no
        # Target for "both Active Spots".
        if act.filter.get("active_only"):
            hits = [h for h in hits if h is pl.active or h is opp.active]
        if act.filter.get("type_not"):
            hits = [h for h in hits
                    if matches_filter(pl if h in pl.in_play() else opp,
                                      h, act.filter)]
        if not hits:
            return False
        for h in (hits if act.filter.get("active_only") else hits[:1]):
            existing = getattr(h, "conditions", None)
            if existing is None:
                return False          # board object has no condition slot
            # Asleep/Confused/Paralyzed are mutually exclusive; Burned and
            # Poisoned stack alongside one of them.
            EXCLUSIVE = {"asleep", "confused", "paralyzed"}
            # An Ability, an attached Tool or Energy, or the Stadium can
            # make the target immune. Owner is whichever side `h` is on --
            # immunity is read off the defender's own board, not the
            # attacker's.
            owner, other = (pl, opp) if h in pl.in_play() else (opp, pl)
            applied = []
            for c in conds:
                if query_condition_immunity(owner, h, c, other):
                    continue
                if c in EXCLUSIVE:
                    h.conditions -= EXCLUSIVE
                h.conditions.add(c)
                applied.append(c)
            conds = applied
        if not conds:
            log.append("    condition(s) prevented")
            return False
        log.append(f"    apply {', '.join(conds)}")
        return True

    if op == O.DISCARD_STADIUM:
        # Stadium removal only started mattering once Stadiums did
        # anything; before that this was correctly inert and is now
        # nine live card effects.
        for side in (pl, opp):
            if getattr(side, "stadium", None):
                log.append(f"    discards Stadium {side.stadium}")
                side.stadium = None
                if side is not pl and getattr(pl, "stadium", None) is None:
                    pass
                return True
        return False

    if op == O.LOOK_AT_DECK:
        # Look at the top N and take the most useful one. Without this the
        # 13 selection Abilities in the pool drew nothing at all; with it
        # they are worth roughly a tutor, which is what they cost.
        n = act.amount or 2
        top = pl.deck[-n:]
        if not top:
            return False
        want = act.filter.get("kind")
        pick = None
        for cand in reversed(top):
            if want and want.lower() not in cand[0].lower():
                continue
            pick = cand
            break
        pick = pick or top[-1]
        pl.deck.remove(pick)
        pl.hand.append(pick)
        log.append(f"    looks at top {n}, takes {pick[1]}")
        return True

    # Turn-scoped locks ARE executed -- they are riders an attack applies
    # to a specific Pokemon, not static properties of a card in play.
    # Lumping every LOCK in with the passives below meant "During your
    # opponent's next turn, the Defending Pokemon can't retreat" (38 card
    # effects) and "...can't attack" (6 more) compiled cleanly and then
    # did nothing at all, which quietly wrote off every retreat-lock
    # control deck in the folder. The genuinely static locks (Ability
    # lockdown, "as long as this Pokemon is Active") stay passive.
    if op == O.LOCK and act.filter.get("what") in ("retreat", "attack", "play"):
        what = act.filter["what"]
        if act.target in (IR.Target.OPPONENT, IR.Target.OPP_ACTIVE):
            if what == "play":
                opp.item_locked = True
                log.append("    opponent can't play Item cards next turn")
                return True
            victim = opp.active
            if victim is None:
                return False
            if what == "retreat":
                victim.retreat_locked = True
            else:
                victim.attack_locked_by_opponent = True
            log.append(f"    {victim.name} can't {what} during their next turn")
            return True
        if act.target == IR.Target.SELF and source is not None:
            if what == "retreat":
                source.retreat_locked = True
            elif what == "attack":
                source.attack_locked = True
            else:
                return False
            log.append(f"    {source.name} can't {what} during your next turn")
            return True
        return False

    # Passive / static ops are queried elsewhere, never "executed".
    if op in (IR.Op.REDUCE_DAMAGE, IR.Op.BUFF_DAMAGE, IR.Op.PREVENT_DAMAGE,
              IR.Op.MODIFY_RETREAT, IR.Op.LOCK, IR.Op.MODIFY_HP,
              IR.Op.MODIFY_ATTACK_COST, IR.Op.GRANT_ATTACK_ACCESS,
              IR.Op.CONDITION_IMMUNITY, IR.Op.SET_WEAKNESS, IR.Op.EVOLVE_EARLY,   # EVOLVE_EARLY: query_evolves_early
              IR.Op.ATTACK_FIRST_TURN, IR.Op.MODIFY_PRIZE, IR.Op.ENDURE,
              IR.Op.BUFF_CONDITION_DAMAGE, IR.Op.SET_TYPE,
              IR.Op.IGNORE_OPPONENT_EFFECTS, IR.Op.ENERGY_PROVIDES_EXTRA,
              IR.Op.EXTRA_TOOLS, IR.Op.ATTACK_TWICE,
              IR.Op.RETURN_TO_HAND_ON_KO, IR.Op.LOCK_COUNTER_MOVEMENT,
              IR.Op.ATTACH_TOOL,
              # WIN_GAME ends the game rather than changing board state, so
              # the match loop owns it (see attack_wins_game).
              IR.Op.WIN_GAME):
        return False

    UNEXECUTED_OPS[op] += 1
    return False


# --------------------------------------------------------------------------
# Activation
# --------------------------------------------------------------------------

def activate(effect, pl, opp, source, log, attacker=None, make_inplay=None):
    if not conditions_met(effect, pl, opp, source):
        return False
    # Coin flips are real randomness in the game, so roll them rather than
    # treating a flip-gated Ability as always-on or always-off.
    if getattr(effect, "chance", 1.0) < 1.0 and random.random() >= effect.chance:
        return False
    snapshot_hand = list(pl.hand)
    if not pay_costs(effect, pl, source, log):
        return False
    did = False
    for act in effect.actions:
        if apply_action(act, pl, opp, source, log, attacker, make_inplay):
            did = True
    if not did:
        pl.hand[:] = snapshot_hand      # refund an unpayable activation
        return False
    # Costs that resolve only after the effect succeeded.
    for c in effect.costs:
        if c["kind"] == "self_ko" and source is not None:
            # Dusclops/Dusknoir's Cursed Blast: the Ability Knocks its own
            # user Out, which hands the opponent a Prize. Leaving this
            # unpaid made Cursed Blast a free, repeatable 130 damage --
            # the Prize cost IS the balancing drawback on the card.
            source.damage = 10 ** 6
            log.append(f"    {source.name} Knocks itself Out")
        if c["kind"] == "shuffle_self" and source is not None:
            pl.deck.append(("Pokemon", source.name))
            if source is pl.active:
                pl.active = pl.bench.pop(0) if pl.bench else None
            elif source in pl.bench:
                pl.bench.remove(source)
            random.shuffle(pl.deck)
            log.append(f"    {source.name} shuffles itself away")
    return True


# --------------------------------------------------------------------------
# Passive queries
# --------------------------------------------------------------------------

def _passive_actions(pl, op):
    """Yield (holder, action) for every in-play passive of a given op."""
    for holder in pl.in_play():
        for eff in pl.EFFECTS.get(holder.name, []):
            if eff.unsupported:
                continue
            for act in eff.actions:
                if act.op == op:
                    yield holder, eff, act


def query_damage_reduction(pl, spot, opp=None):
    """Flat damage reduction applying to `spot` right now."""
    total = 0
    for holder, eff, act in _passive_actions(pl, IR.Op.REDUCE_DAMAGE):
        if not conditions_met(eff, pl, opp or pl, holder):
            continue
        if act.target == IR.Target.SELF and holder is not spot:
            continue
        if act.target in (IR.Target.YOUR_ALL, IR.Target.BOTH_ALL):
            if not matches_filter(pl, spot, act.filter):
                continue
        total += act.amount or 0
    return total


def query_damage_buff(pl, spot, opp=None):
    total = 0
    for holder, eff, act in _passive_actions(pl, IR.Op.BUFF_DAMAGE):
        if not conditions_met(eff, pl, opp or pl, holder):
            continue
        if act.target == IR.Target.SELF and holder is not spot:
            continue
        if act.target == IR.Target.YOUR_ALL and not matches_filter(pl, spot, act.filter):
            continue
        total += act.amount or 0
    return total


def query_prevented(pl, spot, opp=None, attacker=None):
    """Is all damage to `spot` prevented outright?

    `attacker` is the Pokemon actually swinging. Several of these walls
    only stop a particular kind of attacker -- Safeguard stops Pokemon ex,
    Cornerstone Stance stops Pokemon that have an Ability -- and without
    the attacker in hand those restrictions cannot be checked, so they
    were silently ignored and the walls read as total immunity.
    """
    for holder, eff, act in _passive_actions(pl, IR.Op.PREVENT_DAMAGE):
        if act.filter.get("effects_only"):
            continue          # prevents EFFECTS, not damage
        if not conditions_met(eff, pl, opp or pl, holder):
            continue
        if act.target == IR.Target.SELF and holder is not spot:
            continue
        if act.target == IR.Target.YOUR_BENCHED and spot not in pl.bench:
            continue
        if act.filter.get("no_rule_box") and pl.POKEMON[spot.name]["rule_box"]:
            continue
        if act.filter.get("attacker_is_ex") or act.filter.get("attacker_has_ability"):
            # An attacker-restricted wall cannot be evaluated without one.
            if attacker is None or opp is None:
                continue
            card = opp.POKEMON.get(attacker.name, {})
            if act.filter.get("attacker_is_ex") and card.get("prize_value", 1) < 2:
                continue
            if act.filter.get("attacker_has_ability") and \
                    not opp.EFFECTS.get(attacker.name):
                continue
        return True
    return False


def query_ignores_opponent_effects(pl, spot, opp=None):
    """Does this attacker ignore effects on the Defending Pokemon?

    12 card effects say some version of "this attack's damage isn't
    affected by any effects on your opponent's Active Pokemon" -- which is
    precisely the answer to the damage-reduction and prevention walls that
    only started working recently. Compiled and never consulted, so the
    cards whose whole job is beating a wall did not beat one.
    """
    for holder, eff, act in _passive_actions(pl, IR.Op.IGNORE_OPPONENT_EFFECTS):
        if holder is not spot:
            continue
        if not conditions_met(eff, pl, opp or pl, holder):
            continue
        return True
    return False


def query_hp_modifier(pl, spot, opp=None):
    """Extra HP granted by an Ability, e.g. Okidogi's Adrena-Power (+100)."""
    total = 0
    for holder, eff, act in _passive_actions(pl, IR.Op.MODIFY_HP):
        if holder is not spot:
            continue
        if not conditions_met(eff, pl, opp or pl, holder):
            continue
        amount = act.amount or 0
        per = act.filter.get("per_prize_taken")
        if per:
            amount *= (STARTING_PRIZES - (opp.prizes if opp else STARTING_PRIZES))
        total += amount
    return total


def query_endures(pl, spot, opp=None):
    """Would a lethal hit leave this Pokemon on 10 HP instead of dead?

    Pikachu ex's Resolute Heart and friends. Gated on being at full HP,
    which the caller checks by passing the pre-damage state.
    """
    for holder, eff, act in _passive_actions(pl, IR.Op.ENDURE):
        if holder is not spot:
            continue
        if not conditions_met(eff, pl, opp or pl, holder):
            continue
        return True
    return False


def query_prize_modifier(taker, loser):
    """Extra (or fewer) Prizes for a Knock Out, from either side's Abilities."""
    total = 0
    for side, sign in ((taker, 1), (loser, 1)):
        for holder, eff, act in _passive_actions(side, IR.Op.MODIFY_PRIZE):
            if not conditions_met(eff, side, taker if side is loser else loser,
                                  holder):
                continue
            amount = act.amount or 0
            if act.filter.get("fewer") or side is loser:
                amount = -abs(amount)
            chance = getattr(eff, "chance", 1.0)
            if chance < 1.0 and random.random() >= chance:
                continue
            total += amount
    return total


def query_retaliation(defender, attacker_spot, attacker_player=None):
    """Damage counters the defender puts back onto the attacking Pokemon."""
    total = 0
    for holder in defender.in_play():
        for eff in defender.EFFECTS.get(holder.name, []):
            if eff.unsupported or eff.trigger != IR.Trigger.ON_DAMAGED:
                continue
            if not conditions_met(eff, defender, attacker_player or defender, holder):
                continue
            for act in eff.actions:
                if act.op != IR.Op.PLACE_COUNTERS:
                    continue
                if act.target != IR.Target.ATTACKING_POKEMON:
                    continue
                total += (act.amount or 0) * 10
    return total


def query_retreat_modifier(pl, spot, opp=None):
    """Net Retreat-Cost modifier on `spot`, counting BOTH sides.

    Retreat is the one stat an opponent routinely modifies: Mega
    Chandelure ex's Binding Flame and Ariados's Big Net tax YOUR Active
    from across the table. Reading only the owner's own passives missed
    every one of them, which also silently zeroed out any attack that
    scales off the number (Phantom Maze, String Bind, Shadowy Knot).

    -99 is the "no Retreat Cost" sentinel and wins outright.
    """
    total = 0
    for holder, eff, act in _passive_actions(pl, IR.Op.MODIFY_RETREAT):
        if not conditions_met(eff, pl, opp or pl, holder):
            continue
        if act.target == IR.Target.OPP_ACTIVE:
            continue          # aimed across the table, not at our own side
        if act.target == IR.Target.SELF and holder is not spot:
            continue
        if act.target in (IR.Target.YOUR_ALL, IR.Target.YOUR_ANY):
            if not matches_filter(pl, spot, act.filter):
                continue
        if (act.amount or 0) <= -99:
            return -99
        total += act.amount or 0

    # The other player's retreat taxes, which only reach our Active.
    if opp is not None and opp is not pl and spot is pl.active:
        for holder, eff, act in _passive_actions(opp, IR.Op.MODIFY_RETREAT):
            if act.target != IR.Target.OPP_ACTIVE:
                continue
            if not conditions_met(eff, opp, pl, holder):
                continue
            if not matches_filter(pl, spot, act.filter):
                continue
            total += act.amount or 0
    return total


def effective_retreat(pl, spot, opp=None, tool_mod=0):
    """Printed Retreat Cost after every modifier, floored at 0."""
    base = pl.POKEMON[spot.name]["retreat"]
    mod = query_retreat_modifier(pl, spot, opp)
    if mod <= -99:
        return 0
    return max(0, base + mod + tool_mod)


def query_ignored_cost_types(pl, spot, opp=None):
    """Energy types this Pokemon's attack costs ignore right now.

    Decidueye ex's Sniper's Eye ("ignore all Colorless Energy in the costs
    of attacks used by this Pokemon") is conditional on the opponent's hand
    size, so this has to be re-evaluated every time an attack is priced --
    it is on or off turn by turn, not a property of the card.
    """
    out = set()
    for holder, eff, act in _passive_actions(pl, IR.Op.MODIFY_ATTACK_COST):
        if act.target == IR.Target.SELF and holder is not spot:
            continue
        if not conditions_met(eff, pl, opp or pl, holder):
            continue
        if (act.amount or 0) <= -99:
            out.add(act.filter.get("type") or "ALL")
    return out


def query_cost_reduction(pl, spot, opp=None):
    """How many Energy of each type come off this Pokemon's attack costs.

    Separate from query_ignored_cost_types, which is the all-or-nothing
    "ignore every Colorless" shape. This one is a *count*, and for the
    scaling Abilities it is re-derived every time: Food Prep is worth 0
    before a Kofu has hit the discard and 4 once they all have.
    """
    out = {}
    for holder, eff, act in _passive_actions(pl, IR.Op.MODIFY_ATTACK_COST):
        if act.target == IR.Target.SELF and holder is not spot:
            continue
        if not conditions_met(eff, pl, opp or pl, holder):
            continue
        amount = act.amount or 0
        if amount <= -99 or amount >= 0:
            continue
        named = act.filter.get("per_named_card_in_discard")
        if named:
            amount *= sum(1 for c in pl.discard if c == named)
        elif act.filter.get("per_opponent_prize_taken"):
            amount *= (6 - getattr(opp, "prizes", 6)) if opp is not None else 0
        elif act.filter.get("per_opponent_benched"):
            amount *= len(opp.bench) if opp is not None else 0
        if amount:
            t = act.filter.get("type") or "Colorless"
            out[t] = out.get(t, 0) + -amount
    return out


def query_evolves_early(pl, spot, opp=None):
    """Can this Pokemon be evolved on the turn it was played (or turn 1)?

    Luxio's Fighting Roar is the reason this exists: against an ex Active
    it collapses Shinx -> Luxio -> Luxray ex from three turns to two, which
    is the whole clock of a Luxray deck. Gated on the opponent's Active, so
    it has to be asked fresh each turn rather than baked into the card.
    """
    for holder, eff, act in _passive_actions(pl, IR.Op.EVOLVE_EARLY):
        if act.target == IR.Target.SELF and holder is not spot:
            continue
        if not conditions_met(eff, pl, opp or pl, holder):
            continue
        return True
    return False


def query_condition_damage_bonus(pl, condition):
    """Extra damage counters a player's Abilities add to a Special Condition
    at Pokemon Checkup (Pecharunt's Toxic Subjugation, Magmortar's Magma
    Surge). Returns a COUNT OF COUNTERS, not damage."""
    total = 0
    for holder, eff, act in _passive_actions(pl, IR.Op.BUFF_CONDITION_DAMAGE):
        if not conditions_met(eff, pl, pl, holder):
            continue
        if (act.filter.get("condition") or "").lower() != condition:
            continue
        total += act.amount or 0
    return total
