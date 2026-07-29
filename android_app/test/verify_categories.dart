import 'dart:io';

import '../lib/card_categories.dart';
import '../lib/deck_parser.dart';
import '../lib/hand_odds.dart' show binomial;

const importText = '''
Pokémon: 15
3 Budew PRE 148
3 Frillish WHF 32
3 Jellicent ex WHF 33
3 Eevee SFA 51
3 Espeon ex PRE 62

Trainer: 31
4 Boss's Orders MEG 114
3 Xerosic's Machinations SFA 64
3 Eri TEF 146
4 Lillie's Determination MEG 128
3 Judge POR 74
3 Ultra Ball MEG 131
3 Poke Pad ASC 209
4 Buddy-Buddy Poffin TEF 144
4 Night Stretcher SFA 61

Energy: 14
14 Basic Psychic Energy

Total Cards: 60
''';

void main() {
  final lookupJson =
      File('assets/card_categories.json').readAsStringSync();
  final lookup = parseCategoryLookup(lookupJson);
  print('Loaded ${lookup.length} card->category entries');

  final parsed = parseDecklist(importText);
  print('Parsed ${parsed.totalCards} cards, warnings: ${parsed.warnings}');
  if (parsed.totalCards != 60) throw Exception('Parse count FAILED');

  final catCounts = categorize(parsed, lookup);
  print('\nCategory breakdown:');
  catCounts.forEach((k, v) => print('  $k: $v'));
  final catTotal = catCounts.values.fold(0, (a, b) => a + b);
  if (catTotal != 60) throw Exception('Category total FAILED: $catTotal');

  // "Poke Pad" (deliberately typed without the accent, unlike the real
  // "Poké Pad") should still resolve via diacritic-insensitive matching,
  // not fall into the unspecified bucket.
  if (catCounts.containsKey(unknownTrainerCategory) ||
      catCounts.containsKey(unknownCategory)) {
    throw Exception('Unexpected fallback category -- accent matching failed');
  }

  final result = computeCategoryMode(parsed, lookup, 7, 5);
  print('\nTop 5 category compositions (7-card hand):');
  for (final h in result.topCompositions) {
    final desc =
        h.composition.entries.map((e) => '${e.value}x ${e.key}').join(', ');
    print('  ${(h.probability * 100).toStringAsFixed(2)}%  $desc');
  }

  final topSum =
      result.topCompositions.fold(0.0, (s, h) => s + h.probability);
  print('\nSum of top 5 probabilities: ${(topSum * 100).toStringAsFixed(1)}%'
      ' (should be a meaningful chunk, not near-tied slivers)');

  print('\nMarginal distributions (P(exactly k of category)):');
  result.marginals.forEach((category, dist) {
    final atLeast1 = atLeastProbability(dist, 1);
    print('  $category: P(>=1) = ${(atLeast1 * 100).toStringAsFixed(1)}%'
        '   dist=${dist.map((p) => '${p.count}:${(p.probability * 100).toStringAsFixed(1)}%').join(', ')}');
  });

  // Sanity: marginal distribution for each category should sum to 1.0.
  for (final entry in result.marginals.entries) {
    final sum = entry.value.fold(0.0, (s, p) => s + p.probability);
    if ((sum - 1.0).abs() > 0.0001) {
      throw Exception('Marginal for ${entry.key} does not sum to 1: $sum');
    }
  }

  // --- Type-split test: a Dark/Psychic deck should split the Pokemon
  // category by type instead of lumping it into one "Pokemon" bucket. ---
  const dualTypeDeck = '''
Pokémon: 12
4 Sandile BLK 57
4 Krookodile BLK 59
4 Frillish WHF 32

Trainer: 34
34 Boss's Orders MEG 114

Energy: 14
7 Basic Darkness Energy
7 Basic Psychic Energy
''';
  final dualParsed = parseDecklist(dualTypeDeck);
  final dualCats = categorize(dualParsed, lookup);
  print('\nDual-type deck category breakdown:');
  dualCats.forEach((k, v) => print('  $k: $v'));
  if (!dualCats.containsKey('Pokemon (Darkness)') || !dualCats.containsKey('Pokemon (Psychic)')) {
    throw Exception('Pokemon type-split FAILED: $dualCats');
  }
  if (!dualCats.containsKey('Energy (Darkness)') || !dualCats.containsKey('Energy (Psychic)')) {
    throw Exception('Energy type-split FAILED: $dualCats');
  }
  if (dualCats.containsKey('Pokemon') || dualCats.containsKey('Energy')) {
    throw Exception('Expected no lumped Pokemon/Energy bucket once split: $dualCats');
  }
  print('Type-split PASSED');

  // The main sample deck's Energy is genuinely mono-type (all Basic Psychic
  // Energy) and should NOT split, even though its Pokemon legitimately do
  // split (Budew is Grass, Eevee is Colorless, the rest are Psychic -- a
  // real 3-type Pokemon mix, correctly caught above).
  if (!catCounts.containsKey('Energy')) {
    throw Exception('Mono-type Energy incorrectly split: $catCounts');
  }
  print('Mono-type Energy non-split PASSED');

  // A deck that's genuinely mono-type for BOTH Pokemon and Energy should
  // keep single "Pokemon"/"Energy" buckets.
  const monoTypeDeck = '''
Pokémon: 12
4 Sandile BLK 57
4 Krokorok BLK 58
4 Krookodile BLK 59

Trainer: 34
34 Boss's Orders MEG 114

Energy: 14
14 Basic Darkness Energy
''';
  final monoParsed = parseDecklist(monoTypeDeck);
  final monoCats = categorize(monoParsed, lookup);
  print('\nMono-type deck category breakdown:');
  monoCats.forEach((k, v) => print('  $k: $v'));
  if (!monoCats.containsKey('Pokemon') || !monoCats.containsKey('Energy')) {
    throw Exception('Fully mono-type deck incorrectly split: $monoCats');
  }
  print('Fully mono-type non-split PASSED');

  // --- Confidence calculator test ---
  // 15 Pokemon in 60 cards, 7-card hand: verify the returned count actually
  // clears the requested threshold, and one fewer copy would not.
  for (final target in [0.80, 0.90, 0.95, 0.99]) {
    final needed = minimumCountForConfidence(60, 7, target);
    if (needed == null) throw Exception('minimumCountForConfidence returned null for $target');
    final distAt = marginalDistribution(60, needed, 7);
    final probAt = atLeastProbability(distAt, 1);
    if (probAt < target) {
      throw Exception('minimumCountForConfidence($target) = $needed but only gives ${probAt * 100}%');
    }
    if (needed > 1) {
      final distBelow = marginalDistribution(60, needed - 1, 7);
      final probBelow = atLeastProbability(distBelow, 1);
      if (probBelow >= target) {
        throw Exception('minimumCountForConfidence($target) = $needed is not actually minimal '
            '(needed - 1 = ${needed - 1} already gives ${probBelow * 100}%)');
      }
    }
    print('Need $needed copies (of 60) for ${(target * 100).round()}% confidence '
        '(actual: ${(probAt * 100).toStringAsFixed(1)}%)');
  }
  print('Confidence calculator PASSED');

  // --- Composition probability test ---
  // Uses the fully mono-type deck (clean flat 'Pokemon'/'Supporter'/
  // 'Energy' keys, no type-split, no Item bucket). The probability of a
  // specific target composition should be <= the top composition's
  // probability (top is defined as the maximum), and should match
  // hand-computed hypergeometric math directly.
  final monoResult = computeCategoryMode(monoParsed, lookup, 7, 5);
  final target = <String, int>{'Pokemon': 2, 'Supporter': 4, 'Energy': 1};
  final targetProb = compositionProbability(monoCats, target, 7);
  final expectedWays = binomial(monoCats['Pokemon']!, 2) *
      binomial(monoCats['Supporter']!, 4) *
      binomial(monoCats['Energy']!, 1);
  final expectedProb = expectedWays / binomial(60, 7);
  if ((targetProb - expectedProb).abs() > 1e-12) {
    throw Exception('compositionProbability mismatch: $targetProb vs $expectedProb');
  }
  if (monoResult.topCompositions.isNotEmpty &&
      targetProb > monoResult.topCompositions.first.probability + 1e-12) {
    throw Exception('A specific composition probability exceeded the enumerated maximum');
  }
  print('Composition probability: ${(targetProb * 100).toStringAsFixed(3)}% '
      '(top composition: ${(monoResult.topCompositions.first.probability * 100).toStringAsFixed(3)}%)');
  print('Composition probability PASSED');

  print('\nALL CHECKS PASSED');
}
