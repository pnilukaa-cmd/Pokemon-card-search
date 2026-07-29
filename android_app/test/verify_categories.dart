import 'dart:io';

import '../lib/card_categories.dart';
import '../lib/deck_parser.dart';

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

  print('\nALL CHECKS PASSED');
}
