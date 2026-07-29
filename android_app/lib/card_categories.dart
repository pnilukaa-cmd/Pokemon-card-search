/// Category-mode hand odds: instead of exact card-for-card combinations
/// (which cluster into many near-tied, hard-to-read percentages -- see
/// hand_odds.dart), group cards into broad categories (Pokemon, Supporter,
/// Item, Tool, Stadium, Energy) and compute well-differentiated odds like
/// "72% chance of at least 1 Supporter in your opening hand".
///
/// Categorization uses a bundled name -> category lookup built from the
/// real Standard-legal card pool (assets/card_categories.json). Any card
/// name not found there (homebrew, proxies, future sets not yet in the
/// lookup) falls back to the section it was pasted under (Pokemon/Trainer/
/// Energy from deck_parser.dart), with Trainer defaulting to a generic
/// "Trainer (unspecified)" bucket since the paste format alone can't tell
/// Supporter from Item.
library card_categories;

import 'dart:convert';

import 'deck_parser.dart';
import 'hand_odds.dart';

const unknownTrainerCategory = 'Trainer (unspecified)';
const unknownCategory = 'Unrecognized';

// Strips common Latin diacritics (é -> e, etc.) so a card name typed or
// pasted without accents -- e.g. "Poke Pad" instead of "Poké Pad" -- can
// still match the lookup. Covers the accented characters that actually
// show up in Pokemon card names; not a general Unicode normalizer.
const Map<String, String> _diacriticMap = {
  'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
  'á': 'a', 'à': 'a', 'â': 'a', 'ä': 'a',
  'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
  'ó': 'o', 'ò': 'o', 'ô': 'o', 'ö': 'o',
  'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
  'ñ': 'n', 'ç': 'c',
};

String stripDiacritics(String input) {
  final buffer = StringBuffer();
  for (final rune in input.runes) {
    final char = String.fromCharCode(rune);
    buffer.write(_diacriticMap[char] ?? char);
  }
  return buffer.toString();
}

/// Parses the bundled JSON asset (a flat {"CardName": "Category", ...} map)
/// into a lookup table.
Map<String, String> parseCategoryLookup(String jsonText) {
  final decoded = jsonDecode(jsonText) as Map<String, dynamic>;
  return decoded.map((k, v) => MapEntry(k, v as String));
}

/// Builds a secondary index keyed by diacritic-stripped name, for matching
/// names typed/pasted without accents. If multiple real names collapse to
/// the same stripped form, the first one wins (rare in practice).
Map<String, String> buildNormalizedLookup(Map<String, String> lookup) {
  final normalized = <String, String>{};
  lookup.forEach((name, category) {
    final key = stripDiacritics(name).toLowerCase();
    normalized.putIfAbsent(key, () => category);
  });
  return normalized;
}

/// Collapses a parsed deck's per-card-name counts into category counts,
/// using [lookup] first (exact match, then diacritic-insensitive match),
/// and falling back to the pasted section otherwise.
Map<String, int> categorize(ParsedDeck deck, Map<String, String> lookup,
    {Map<String, String>? normalizedLookup}) {
  final normalized = normalizedLookup ?? buildNormalizedLookup(lookup);
  final categoryCounts = <String, int>{};
  deck.cardCounts.forEach((name, count) {
    String category;
    final normalizedKey = stripDiacritics(name).toLowerCase();
    if (lookup.containsKey(name)) {
      category = lookup[name]!;
    } else if (normalized.containsKey(normalizedKey)) {
      category = normalized[normalizedKey]!;
    } else {
      final section = deck.sectionOf[name];
      if (section == 'Pokemon') {
        category = 'Pokemon';
      } else if (section == 'Energy') {
        category = 'Energy';
      } else if (section == 'Trainer') {
        category = unknownTrainerCategory;
      } else {
        category = unknownCategory;
      }
    }
    categoryCounts[category] = (categoryCounts[category] ?? 0) + count;
  });
  return categoryCounts;
}

class MarginalPoint {
  final int count; // number of this category in the hand
  final double probability;
  MarginalPoint(this.count, this.probability);
}

/// Exact distribution of "how many cards of this one category show up in
/// the hand" -- a single-category hypergeometric, independent of the other
/// categories. E.g. P(exactly k Supporters in a 7-card hand).
List<MarginalPoint> marginalDistribution(
    int deckSize, int categoryCount, int handSize) {
  final totalWays = binomial(deckSize, handSize);
  final points = <MarginalPoint>[];
  final maxK = categoryCount < handSize ? categoryCount : handSize;
  for (var k = 0; k <= maxK; k++) {
    final ways = binomial(categoryCount, k) *
        binomial(deckSize - categoryCount, handSize - k);
    points.add(MarginalPoint(k, ways / totalWays));
  }
  return points;
}

/// P(at least [atLeast] cards of this category in the hand).
double atLeastProbability(List<MarginalPoint> dist, int atLeast) {
  return dist
      .where((p) => p.count >= atLeast)
      .fold(0.0, (sum, p) => sum + p.probability);
}

class CategoryModeResult {
  final Map<String, int> categoryCounts;
  final List<HandResult> topCompositions;
  final Map<String, List<MarginalPoint>> marginals;

  CategoryModeResult(this.categoryCounts, this.topCompositions, this.marginals);
}

CategoryModeResult computeCategoryMode(
    ParsedDeck deck, Map<String, String> lookup, int handSize, int topN) {
  final categoryCounts = categorize(deck, lookup);
  final deckSize = categoryCounts.values.fold(0, (a, b) => a + b);

  final topCompositions = topHands(categoryCounts, handSize, topN);

  final marginals = <String, List<MarginalPoint>>{};
  categoryCounts.forEach((category, count) {
    marginals[category] = marginalDistribution(deckSize, count, handSize);
  });

  return CategoryModeResult(categoryCounts, topCompositions, marginals);
}
