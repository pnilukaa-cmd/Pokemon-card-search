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
    if filt.get("stage") and info.get("stage") != filt["stage"]:
        return False
    if filt.get("stage_not") and info.get("stage") == filt["stage_not"]:
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
        if k == "own_prizes_equal" and getattr(pl, "prizes", None) != c["count"]:
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
        for h in chosen:
            h.damage += (act.amount or 0) * 10
        if chosen:
            log.append(f"    place {(act.amount or 0)*10} damage on "
                       f"{len(chosen)} Pokemon")
        return True

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

    if op == O.DISCARD_ENERGY_FROM_OPPONENT:
        hits = resolve_targets(act.target, pl, opp, source, attacker)
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

    if op == O.LOOK_AT_DECK:
        # Deck manipulation with no board effect; the closest honest
        # approximation is that it improves the next draw, which this engine
        # does not track. Counted as a no-op but NOT as an unhandled op.
        return False

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

    if op == O.DEVOLVE:
        evolved = [q for q in opp.in_play()
                   if opp.POKEMON.get(q.name, {}).get("evolves_from")]
        if not evolved:
            return False
        tgt = max(evolved, key=lambda q: opp.POKEMON[q.name]["hp"])
        pre = opp.POKEMON[tgt.name]["evolves_from"]
        opp.hand.append(("Pokemon", tgt.name))
        tgt.name = pre
        log.append(f"    devolve -> {pre}")
        return True

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
        for h in hits[:1]:
            existing = getattr(h, "conditions", None)
            if existing is None:
                return False          # board object has no condition slot
            # Asleep/Confused/Paralyzed are mutually exclusive; Burned and
            # Poisoned stack alongside one of them.
            EXCLUSIVE = {"asleep", "confused", "paralyzed"}
            for c in conds:
                if c in EXCLUSIVE:
                    h.conditions -= EXCLUSIVE
                h.conditions.add(c)
        log.append(f"    apply {', '.join(conds)}")
        return True

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
        if act.filter.get("no_rule_box") and pl.POKEMON[spot.name]["rule_box"]:
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
