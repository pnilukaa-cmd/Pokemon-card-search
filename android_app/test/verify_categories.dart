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

  // --- Limitless TCG "archetype average" format test ---
  // Real export has parenthetical section headers ("Pokémon (17.48)", not
  // "Pokémon: 14") and fractional counts (statistical averages across many
  // tournament decks, not one buildable deck). Confirm: headers parse
  // without producing "Unrecognized"/no-section fallback noise, counts
  // round to sensible integers, entries that round to 0 are dropped, and a
  // clear warning fires flagging this as non-integer/likely-aggregate data.
  const limitlessAverageText = '''
Pokémon (5.48)
4.00 N's Zorua JTG 97
1.10 Pecharunt ex SFA 39
0.29 Budew ASC 16
0.01 Snorunt ASC 46
0.09 Purrloin WHT 55

Trainer (2.6)
2.42 Ultra Ball MEG 131
0.14 Judge POR 76
0.04 Ruffian JTG 157

Energy (7.87)
7.86 Darkness Energy MEE 7
0.01 Prism Energy ASC 216
''';
  final limitlessParsed = parseDecklist(limitlessAverageText);
  print('\nLimitless average-format parse:');
  print('  Total: ${limitlessParsed.totalCards}, entries: ${limitlessParsed.cardCounts}');
  print('  Warnings: ${limitlessParsed.warnings}');

  if (limitlessParsed.cardCounts["N's Zorua"] != 4) {
    throw Exception("Expected N's Zorua to round to 4, got ${limitlessParsed.cardCounts["N's Zorua"]}");
  }
  if (limitlessParsed.cardCounts['Pecharunt ex'] != 1) {
    throw Exception('Expected Pecharunt ex to round to 1, got ${limitlessParsed.cardCounts['Pecharunt ex']}');
  }
  if (limitlessParsed.cardCounts.containsKey('Snorunt')) {
    throw Exception('Expected Snorunt (0.01, rounds to 0) to be dropped entirely');
  }
  if (limitlessParsed.cardCounts.containsKey('Budew')) {
    throw Exception('Expected Budew (0.29, rounds to 0) to be dropped entirely');
  }
  if (!limitlessParsed.warnings.any((w) => w.contains('not whole numbers'))) {
    throw Exception('Expected a warning about non-integer counts, got: ${limitlessParsed.warnings}');
  }
  // The section headers (with parens, not colons) must still be recognized
  // -- confirmed indirectly since Pecharunt ex/Ultra Ball/Darkness Energy
  // all round to nonzero and correctly land under their real sections,
  // which categorize() would need for any unrecognized-name fallback.
  if (limitlessParsed.sectionOf['Ultra Ball'] != 'Trainer') {
    throw Exception('Parenthetical Trainer header not recognized: ${limitlessParsed.sectionOf}');
  }
  if (limitlessParsed.sectionOf["N's Zorua"] != 'Pokemon') {
    throw Exception('Parenthetical Pokemon header not recognized: ${limitlessParsed.sectionOf}');
  }
  print('Limitless average-format handling PASSED');

  // --- PTCG Live {X} type-letter shorthand test ---
  // Some PTCG Live exports use "Basic {P} Energy" instead of "Basic
  // Psychic Energy", and for Special Energy the letter code replaces the
  // type word inside the real name itself ("Telepathic {P} Energy" whose
  // real card is "Telepathic Psychic Energy"). Both must expand correctly.
  const letterCodeText = '''
Pokémon: 4
4 Poltchageist PBL 5

Trainer: 47
47 Boss's Orders MEG 114

Energy: 9
8 Basic {P} Energy MEE 5
1 Telepathic {P} Energy POR 88
''';
  final letterParsed = parseDecklist(letterCodeText);
  print('\n{X} type-letter shorthand parse: ${letterParsed.cardCounts}');
  if (letterParsed.cardCounts['Basic Psychic Energy'] != 8) {
    throw Exception('Basic {P} Energy did not expand correctly: ${letterParsed.cardCounts}');
  }
  if (letterParsed.cardCounts['Telepathic Psychic Energy'] != 1) {
    throw Exception('Telepathic {P} Energy did not expand correctly: ${letterParsed.cardCounts}');
  }
  if (!lookup.containsKey('Telepathic Psychic Energy')) {
    throw Exception('Sanity check failed: real card "Telepathic Psychic Energy" not in lookup');
  }
  print('{X} type-letter shorthand PASSED');

  print('\nALL CHECKS PASSED');
}
