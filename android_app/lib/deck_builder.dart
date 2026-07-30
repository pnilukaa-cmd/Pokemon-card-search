/// Given a single Pokemon name, generates a playable 60-card decklist built
/// around that Pokemon's full evolution line -- pure combinatorics/heuristics
/// over the bundled Standard-legal card pool (assets/card_pool.json), no
/// simulation. This is a starting point, not a tuned tournament list: run
/// the result back through `generateRecommendations` (card_categories.dart)
/// to see how well-formed it actually is.
library deck_builder;

import 'dart:convert';

import 'card_categories.dart' show stripDiacritics;

class PokemonAttack {
  final String name;
  final List<String> cost;
  final String damage;
  PokemonAttack(this.name, this.cost, this.damage);

  int get energyCost => cost.length;

  int get damageValue {
    final match = RegExp(r'(\d+)').firstMatch(damage);
    return match != null ? int.parse(match.group(1)!) : 0;
  }
}

class PokemonCardInfo {
  final List<String> types;
  final int hp;
  final String? stage;
  final String? evolvesFrom;
  final List<String> evolvesTo;
  final int retreatCost;
  final List<String> weaknesses;
  final List<PokemonAttack> attacks;

  PokemonCardInfo({
    required this.types,
    required this.hp,
    required this.stage,
    required this.evolvesFrom,
    required this.evolvesTo,
    required this.retreatCost,
    required this.weaknesses,
    required this.attacks,
  });
}

Map<String, PokemonCardInfo> parseCardPool(String jsonText) {
  final decoded = jsonDecode(jsonText) as Map<String, dynamic>;
  return decoded.map((name, value) {
    final v = value as Map<String, dynamic>;
    final attacks = (v['attacks'] as List<dynamic>).map((a) {
      final am = a as Map<String, dynamic>;
      return PokemonAttack(
        am['name'] as String,
        (am['cost'] as List<dynamic>).map((c) => c as String).toList(),
        am['damage'] as String,
      );
    }).toList();
    return MapEntry(
      name,
      PokemonCardInfo(
        types: (v['types'] as List<dynamic>).map((t) => t as String).toList(),
        hp: v['hp'] as int,
        stage: v['stage'] as String?,
        evolvesFrom: v['evolvesFrom'] as String?,
        evolvesTo: (v['evolvesTo'] as List<dynamic>).map((t) => t as String).toList(),
        retreatCost: v['retreatCost'] as int,
        weaknesses: (v['weaknesses'] as List<dynamic>).map((t) => t as String).toList(),
        attacks: attacks,
      ),
    );
  });
}

/// Finds the pool key matching [query], case/diacritic-insensitive. Returns
/// null if nothing matches exactly.
String? findSeedMatch(String query, Map<String, PokemonCardInfo> pool) {
  if (pool.containsKey(query)) return query;
  final normalizedQuery = stripDiacritics(query).trim().toLowerCase();
  for (final name in pool.keys) {
    if (stripDiacritics(name).toLowerCase() == normalizedQuery) return name;
  }
  return null;
}

/// Substring suggestions for a query that didn't match exactly, capped at 5.
List<String> suggestNames(String query, Map<String, PokemonCardInfo> pool) {
  final normalizedQuery = stripDiacritics(query).trim().toLowerCase();
  if (normalizedQuery.isEmpty) return [];
  final matches = pool.keys
      .where((name) => stripDiacritics(name).toLowerCase().contains(normalizedQuery))
      .toList()
    ..sort();
  return matches.take(5).toList();
}

class EvolutionLine {
  final List<String> stageNames; // ordered Basic -> ... -> final stage
  EvolutionLine(this.stageNames);
}

/// Walks backward via evolvesFrom to the Basic, then forward via evolvesTo
/// to the final known evolution, starting from [seedName]. If a Pokemon
/// branches into multiple named evolutions (e.g. Eevee's many Eeveelutions),
/// picks the branch that shares a type with the current stage, falling back
/// to the first option alphabetically for a deterministic result.
EvolutionLine? buildEvolutionLine(String seedName, Map<String, PokemonCardInfo> pool) {
  if (!pool.containsKey(seedName)) return null;

  final backward = <String>[];
  String? current = seedName;
  final seenBackward = <String>{};
  while (current != null && seenBackward.add(current)) {
    backward.add(current);
    current = pool[current]?.evolvesFrom;
    if (current != null && !pool.containsKey(current)) break;
  }
  final chain = backward.reversed.toList();

  var tail = chain.last;
  final seenForward = Set<String>.from(chain);
  while (true) {
    final info = pool[tail];
    if (info == null || info.evolvesTo.isEmpty) break;
    final candidates = info.evolvesTo.where((n) => pool.containsKey(n) && !seenForward.contains(n)).toList()
      ..sort();
    if (candidates.isEmpty) break;
    final sameType =
        candidates.where((n) => pool[n]!.types.any((t) => info.types.contains(t))).toList();
    final next = sameType.isNotEmpty ? sameType.first : candidates.first;
    chain.add(next);
    seenForward.add(next);
    tail = next;
  }

  return EvolutionLine(chain);
}

class GeneratedDeck {
  final String seedName;
  final EvolutionLine line;
  final Map<String, int> pokemonCounts;
  final Map<String, int> trainerCounts;
  final Map<String, int> energyCounts;
  final String featuredAttackName;
  final int featuredAttackDamage;
  final List<String> notes;

  GeneratedDeck({
    required this.seedName,
    required this.line,
    required this.pokemonCounts,
    required this.trainerCounts,
    required this.energyCounts,
    required this.featuredAttackName,
    required this.featuredAttackDamage,
    required this.notes,
  });

  int get totalCards =>
      pokemonCounts.values.fold<int>(0, (a, b) => a + b) +
      trainerCounts.values.fold<int>(0, (a, b) => a + b) +
      energyCounts.values.fold<int>(0, (a, b) => a + b);

  /// Plain decklist text, in the same shape the app's own parser accepts
  /// (Pokemon TCG Live-style section headers). Set codes are intentionally
  /// omitted -- only card names matter for hand-odds math and the
  /// recommendation engine, and every name here is unambiguous within the
  /// current Standard pool.
  String toDecklistText() {
    final buffer = StringBuffer();
    final pokemonTotal = pokemonCounts.values.fold<int>(0, (a, b) => a + b);
    buffer.writeln('Pokémon: $pokemonTotal');
    pokemonCounts.forEach((name, count) => buffer.writeln('$count $name'));
    buffer.writeln();
    final trainerTotal = trainerCounts.values.fold<int>(0, (a, b) => a + b);
    buffer.writeln('Trainer: $trainerTotal');
    trainerCounts.forEach((name, count) => buffer.writeln('$count $name'));
    buffer.writeln();
    final energyTotal = energyCounts.values.fold<int>(0, (a, b) => a + b);
    buffer.writeln('Energy: $energyTotal');
    energyCounts.forEach((name, count) => buffer.writeln('$count $name'));
    return buffer.toString().trimRight();
  }
}

// A rotation of generic, broadly-useful Standard staples used to pad the
// Trainer count out to a realistic size once the seed's own evolution line
// and the always-included core (Ultra Ball, Boss's Orders, a draw
// Supporter, Switch, Night Stretcher) are set. Each is real, currently
// Standard-legal, and capped at the format's 4-copy limit.
const List<String> _staplePriority = [
  "Drayton",
  "Judge",
  "Colress's Tenacity",
  "Brock's Scouting",
  'Energy Search',
  'Cheren',
  'Perrin',
];

// A single evolution line rarely reaches a healthy Pokemon count on its own
// (a 1-2 stage line caps out at 4-8 copies total). These are Basic, single-
// prize, Colorless-type attackers with Colorless-only attack costs, so they
// slot into a deck of *any* type without requiring a new Energy type or
// diluting the seed's own attacker. Used to pad the Pokemon count toward a
// healthier range before the Trainer package is sized.
const List<String> _genericSupportPriority = ['Tornadus', 'Bouffalant'];
const int _targetMinPokemon = 12;

/// Builds a starting-point 60-card deck around [query]. Returns null (with
/// [suggestions] populated via the separate [suggestNames] call) if the name
/// doesn't match anything in the pool.
GeneratedDeck? buildDeckForPokemon(String query, Map<String, PokemonCardInfo> pool) {
  final seedName = findSeedMatch(query, pool);
  if (seedName == null) return null;

  final line = buildEvolutionLine(seedName, pool)!;
  final notes = <String>[];

  // Pokemon quantities: heavier on the Basic and final stage, light on any
  // middle "bridge" stage (Rare Candy is included to skip past it when a
  // Stage 2 is present).
  final pokemonCounts = <String, int>{};
  final n = line.stageNames.length;
  if (n == 1) {
    pokemonCounts[line.stageNames[0]] = 4;
  } else if (n == 2) {
    pokemonCounts[line.stageNames[0]] = 4;
    pokemonCounts[line.stageNames[1]] = 4;
  } else {
    pokemonCounts[line.stageNames.first] = 4;
    for (var i = 1; i < n - 1; i++) {
      pokemonCounts[line.stageNames[i]] = 2;
    }
    pokemonCounts[line.stageNames.last] = 4;
  }
  var pokemonTotal = pokemonCounts.values.fold<int>(0, (a, b) => a + b);

  // A single evolution line usually can't reach a healthy Pokemon count on
  // its own -- pad with generic, energy-agnostic support attackers so the
  // deck doesn't lean unrealistically hard on Trainers to fill 60 cards.
  if (pokemonTotal < _targetMinPokemon) {
    for (final support in _genericSupportPriority) {
      if (pokemonTotal >= _targetMinPokemon) break;
      if (pokemonCounts.containsKey(support) || !pool.containsKey(support)) continue;
      pokemonCounts[support] = 4;
      pokemonTotal += 4;
    }
    notes.add('Padded with generic single-prize support Pokemon '
        '(${_genericSupportPriority.where((s) => pokemonCounts.containsKey(s)).join(', ')}) '
        "since $seedName's own evolution line alone doesn't reach a healthy Pokemon count.");
  }

  final finalStageName = line.stageNames.last;
  final finalStage = pool[finalStageName]!;
  final basicStageName = line.stageNames.first;
  final basicStage = pool[basicStageName]!;

  // Featured attack: the final stage's highest-damage attack (falls back to
  // its first attack if every attack is purely a status/utility effect).
  PokemonAttack? featured;
  for (final atk in finalStage.attacks) {
    if (featured == null || atk.damageValue > featured.damageValue) featured = atk;
  }
  featured ??= finalStage.attacks.isNotEmpty ? finalStage.attacks.first : null;

  final energyTypeCounts = <String, int>{};
  if (featured != null) {
    for (final c in featured.cost) {
      if (c != 'Colorless') energyTypeCounts[c] = (energyTypeCounts[c] ?? 0) + 1;
    }
  }
  if (energyTypeCounts.isEmpty) {
    final fallbackType = finalStage.types.isNotEmpty ? finalStage.types.first : 'Colorless';
    energyTypeCounts[fallbackType] = 1;
    if (featured == null) {
      notes.add('$finalStageName has no attacks in the bundled data -- energy '
          'typing falls back to its own type ($fallbackType).');
    } else {
      notes.add("${featured.name} costs only Colorless energy, so energy typing "
          'falls back to $finalStageName\'s own type ($fallbackType).');
    }
  }

  final hasStage2 = n >= 3;
  final basicIsSmall = basicStage.hp <= 70;

  final energyTarget = energyTypeCounts.length >= 2 ? 14 : 12;
  final energyCounts = <String, int>{};
  final typeList = energyTypeCounts.keys.toList();
  final totalNonColorless = energyTypeCounts.values.fold<int>(0, (a, b) => a + b);
  var remainingEnergy = energyTarget;
  for (var i = 0; i < typeList.length; i++) {
    final isLast = i == typeList.length - 1;
    int amount;
    if (isLast) {
      amount = remainingEnergy;
    } else {
      final rawShare = (energyTarget * energyTypeCounts[typeList[i]]! / totalNonColorless).round();
      // Reserve at least 1 copy for every type still left to allocate after
      // this one, so the clamp below never gets an inverted (upper < lower)
      // range even for an attack costing 3+ distinct types.
      final reserveForRest = typeList.length - 1 - i;
      final upperBound = remainingEnergy - reserveForRest;
      amount = rawShare.clamp(1, upperBound < 1 ? 1 : upperBound);
    }
    energyCounts['Basic ${typeList[i]} Energy'] = amount;
    remainingEnergy -= amount;
  }

  final trainerTarget = 60 - pokemonTotal - energyTarget;

  final trainerCounts = <String, int>{
    'Ultra Ball': 4,
    "Boss's Orders": 4,
    "Lillie's Determination": 4,
    'Switch': 3,
    'Night Stretcher': 3,
  };
  if (basicIsSmall) {
    trainerCounts['Buddy-Buddy Poffin'] = 4;
  } else {
    notes.add('$basicStageName is ${basicStage.hp} HP (over the 70 HP cap), so '
        "Buddy-Buddy Poffin was left out -- it can't fetch it to the Bench.");
  }
  if (hasStage2) {
    trainerCounts['Rare Candy'] = 4;
  }

  var trainerSoFar = trainerCounts.values.fold<int>(0, (a, b) => a + b);
  for (final staple in _staplePriority) {
    if (trainerSoFar >= trainerTarget) break;
    final add = (trainerTarget - trainerSoFar).clamp(0, 4);
    if (add <= 0) break;
    trainerCounts[staple] = add;
    trainerSoFar += add;
  }
  if (trainerSoFar < trainerTarget) {
    // Staple pool exhausted (shouldn't normally happen) -- top up the most
    // generic, always-safe search card rather than leave the deck short.
    trainerCounts['Ultra Ball'] = (trainerCounts['Ultra Ball'] ?? 0) +
        (trainerTarget - trainerSoFar).clamp(0, 4 - (trainerCounts['Ultra Ball'] ?? 0));
  }

  notes.add(
      '${line.stageNames.join(' -> ')} is the full evolution line built around $seedName.');
  if (featured != null) {
    notes.add(
        "Featured attack: $finalStageName's \"${featured.name}\" (${featured.cost.isEmpty ? 'free' : featured.cost.join('+')}) "
        'for ${featured.damage.isEmpty ? 'no direct damage (status/utility attack)' : '${featured.damage} damage'}.');
  }
  notes.add('This is a generated starting point, not a tuned list -- run it through '
      '"By Category" mode to see its own recommendations and adjust from there.');

  return GeneratedDeck(
    seedName: seedName,
    line: line,
    pokemonCounts: pokemonCounts,
    trainerCounts: trainerCounts,
    energyCounts: energyCounts,
    featuredAttackName: featured?.name ?? '(none)',
    featuredAttackDamage: featured?.damageValue ?? 0,
    notes: notes,
  );
}
