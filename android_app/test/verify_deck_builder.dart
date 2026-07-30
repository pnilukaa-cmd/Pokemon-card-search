// Standalone verification for deck_builder.dart -- run with `dart run`.
// Not a flutter_test widget test; exercises the pure-Dart deck generation
// logic directly against the real bundled card pool.

import 'dart:io';

import '../lib/card_categories.dart';
import '../lib/deck_builder.dart';
import '../lib/deck_parser.dart';

void check(bool cond, String message) {
  if (!cond) {
    stderr.writeln('FAILED: $message');
    exit(1);
  }
}

void main() {
  final jsonText = File('assets/card_pool.json').readAsStringSync();
  final pool = parseCardPool(jsonText);
  print('Loaded ${pool.length} Pokemon into the card pool.');

  final categoryJson = File('assets/card_categories.json').readAsStringSync();
  final lookup = parseCategoryLookup(categoryJson);

  // A representative spread: a Basic with no evolutions, a 2-stage line, a
  // 3-stage line, an ex, and Leafeon ex specifically because its attack
  // costs 3 distinct energy types (Grass/Fire/Water) -- the edge case the
  // energy-split rounding logic has to handle without crashing.
  final seeds = ['Munkidori', 'Whimsicott', 'Feraligatr', 'Dragapult ex', 'Leafeon ex', 'Pikachu'];

  for (final seed in seeds) {
    print('\n=== $seed ===');
    final deck = buildDeckForPokemon(seed, pool);
    if (deck == null) {
      final suggestions = suggestNames(seed, pool);
      print('  Not found. Suggestions: $suggestions');
      continue;
    }
    print('  Line: ${deck.line.stageNames.join(' -> ')}');
    print('  Featured attack: ${deck.featuredAttackName} (${deck.featuredAttackDamage} dmg)');
    print('  Pokemon: ${deck.pokemonCounts}');
    print('  Trainer: ${deck.trainerCounts}');
    print('  Energy: ${deck.energyCounts}');
    print('  Total: ${deck.totalCards}');
    check(deck.totalCards == 60, '$seed: expected exactly 60 cards, got ${deck.totalCards}');

    for (final entry in [...deck.pokemonCounts.entries, ...deck.trainerCounts.entries]) {
      check(entry.value <= 4, '$seed: ${entry.key} has ${entry.value} copies, exceeds the 4-copy limit');
    }
    for (final entry in deck.energyCounts.entries) {
      check(entry.value >= 1, '$seed: ${entry.key} has non-positive count ${entry.value}');
    }

    for (final note in deck.notes) {
      print('  Note: $note');
    }

    // Round-trip: parse the generated text back through the app's own
    // parser and confirm it's recognized as a clean 60-card deck with no
    // warnings, then check what the recommendation engine says about it.
    final parsed = parseDecklist(deck.toDecklistText());
    check(parsed.totalCards == 60, '$seed: generated text did not parse back to 60 cards');
    check(parsed.warnings.isEmpty, '$seed: generated text produced parser warnings: ${parsed.warnings}');

    final unrecognized = <String>[];
    final normalized = buildNormalizedLookup(lookup);
    parsed.cardCounts.forEach((name, count) {
      final key = stripDiacritics(name).toLowerCase();
      if (lookup[name] == null && normalized[key] == null && !name.toLowerCase().contains('energy')) {
        unrecognized.add(name);
      }
    });
    check(unrecognized.isEmpty, '$seed: generated deck has unrecognized non-energy names: $unrecognized');

    final recs = generateRecommendations(parsed, lookup);
    print('  Recommendations on the generated deck (${recs.length}):');
    for (final r in recs) {
      print('    [${r.level}] ${r.message}');
    }
  }

  // Not-found path.
  final missing = buildDeckForPokemon('Zzyzxblorp', pool);
  check(missing == null, 'Expected a nonsense name to return null');
  final suggestions = suggestNames('char', pool);
  print('\nSuggestions for "char": $suggestions');
  check(suggestions.isNotEmpty, 'Expected substring suggestions for "char"');

  print('\nALL CHECKS PASSED');
}
