#!/usr/bin/env python3
"""Executes compiled ability IR against a running game.

STATUS: WRITTEN AND IMPORTABLE, BUT NOT YET WIRED INTO simulate_versus.py.
A first integration attempt was reverted: routing every Ability through
this runtime dropped the Alakazam deck's turn-6 hand from ~13.6 cards
(what simulate_baseline.py measures) to ~2, which collapsed Powerful
Hand from ~270 damage to 40. The draw Abilities stopped firing somewhere
in the activation path. Rather than ship a simulator that silently
reports wrong win rates, simulate_versus.py was restored to its previous
hand-written ability handling, which is tested and correct. Wiring this
in is the remaining work, and it needs a per-ability firing test (assert
each Ability actually fires and changes state) before it replaces the
existing path -- coverage of the IR is proven, execution is not.


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

# Ops that compiled but that the runtime has no handler for. Reported by
# the simulator so a compiled-but-inert ability is never mistaken for one
# that actually did something.
UNEXECUTED_OPS = Counter()


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
    return True


# --------------------------------------------------------------------------
# Conditions and costs
# --------------------------------------------------------------------------

def conditions_met(effect, pl, opp, source):
    for c in effect.conditions:
        k = c["kind"]
        if k == "self_is_active" and source is not pl.active:
            return False
        if k == "self_is_benched" and source not in pl.bench:
            return False
        if k == "lost_pokemon_last_turn" and not getattr(pl, "lost_pokemon_last_turn", False):
            return False
        if k == "named_in_play" and c["name"] not in pl.in_play_names():
            return False
        if k == "played_this_turn" and c["name"] not in getattr(pl, "played_supporters_this_turn", set()):
            return False
        if k == "self_has_energy_type":
            if not any(c["type"] in e for e in source.energy):
                return False
        if k == "self_full_hp" and source.damage > 0:
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
            for _ in range(c["amount"]):
                kind, name = pl.hand.pop(0)
                pl.discard.append(name)
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
        for h in hits[:1] if act.target != IR.Target.OPP_ALL else hits:
            h.damage += (act.amount or 0) * 10
        if hits:
            log.append(f"    place {(act.amount or 0)*10} damage")
        return True

    if op == O.MOVE_COUNTERS:
        donors = [q for q in pl.in_play() if q.damage >= 10]
        hits = resolve_targets(act.target, pl, opp, source, attacker) or \
            ([opp.active] if opp.active else [])
        if not donors or not hits:
            return False
        donor = max(donors, key=lambda q: q.damage)
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
        if healed:
            log.append(f"    heal {healed}")
        return healed > 0

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
            card = _find_in_deck(pl, lambda k, n: k == "Pokemon"
                                 and pl.POKEMON[n]["stage"] == "Basic"
                                 and (not want or want.lower() in n.lower()))
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
                if kind in ("supporter", "item", "stadium") and k.lower() != kind:
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

    # Passive / static ops are queried elsewhere, never "executed".
    if op in (IR.Op.REDUCE_DAMAGE, IR.Op.BUFF_DAMAGE, IR.Op.PREVENT_DAMAGE,
              IR.Op.MODIFY_RETREAT, IR.Op.LOCK, IR.Op.MODIFY_HP,
              IR.Op.MODIFY_ATTACK_COST, IR.Op.GRANT_ATTACK_ACCESS,
              IR.Op.CONDITION_IMMUNITY, IR.Op.SET_WEAKNESS, IR.Op.EVOLVE_EARLY,
              IR.Op.ATTACK_FIRST_TURN, IR.Op.MODIFY_PRIZE, IR.Op.ENDURE,
              IR.Op.BUFF_CONDITION_DAMAGE):
        return False

    UNEXECUTED_OPS[op] += 1
    return False


# --------------------------------------------------------------------------
# Activation
# --------------------------------------------------------------------------

def activate(effect, pl, opp, source, log, attacker=None, make_inplay=None):
    if not conditions_met(effect, pl, opp, source):
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


def query_prevented(pl, spot, opp=None):
    """Is all damage to `spot` prevented outright?"""
    for holder, eff, act in _passive_actions(pl, IR.Op.PREVENT_DAMAGE):
        if act.filter.get("effects_only"):
            continue          # prevents EFFECTS, not damage
        if not conditions_met(eff, pl, opp or pl, holder):
            continue
        if act.target == IR.Target.SELF and holder is not spot:
            continue
        if act.target == IR.Target.YOUR_BENCHED and spot not in pl.bench:
            continue
        return True
    return False


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
    total = 0
    for holder, eff, act in _passive_actions(pl, IR.Op.MODIFY_RETREAT):
        if not conditions_met(eff, pl, opp or pl, holder):
            continue
        if act.target == IR.Target.SELF and holder is not spot:
            continue
        total += act.amount or 0
    return total
