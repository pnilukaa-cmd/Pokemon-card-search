/// Category-mode hand odds: instead of exact card-for-card combinations
/// (which cluster into many near-tied, hard-to-read percentages -- see
/// hand_odds.dart), group cards into broad categories (Pokemon, Supporter,
/// Item, Tool, Stadium, Energy) and compute well-differentiated odds like
/// "72% chance of at least 1 Supporter in your opening hand".
///
/// When a deck has more than one Pokemon type (e.g. a Dark/Psychic deck) or
/// more than one Energy type, those two categories are further split by
/// type ("Pokemon (Darkness)", "Pokemon (Psychic)", etc.) instead of being
/// lumped together, since "how many Psychic Pokemon will I open with" is a
/// more useful question than "how many Pokemon" once type matters. A
/// mono-type deck keeps the simple single "Pokemon"/"Energy" bucket.
///
/// Categorization uses a bundled name -> {category, types} lookup built
/// from the real Standard-legal card pool (assets/card_categories.json).
/// Any card name not found there (homebrew, proxies, future sets, or Basic
/// Energy cards which aren't in the card database at all since they're
/// evergreen and not tied to a set) falls back to: a "Basic X Energy" /
/// "X Energy" name pattern match for typing energy, then the section it
/// was pasted under (Pokemon/Trainer/Energy from deck_parser.dart) for
/// anything else, with Trainer defaulting to a generic "Trainer
/// (unspecified)" bucket since the paste format alone can't tell Supporter
/// from Item.
library card_categories;

import 'dart:convert';

import 'deck_parser.dart';
import 'hand_odds.dart';

const unknownTrainerCategory = 'Trainer (unspecified)';
const unknownCategory = 'Unrecognized';

const List<String> pokemonTypes = [
  'Grass', 'Fire', 'Water', 'Lightning', 'Psychic', 'Fighting',
  'Darkness', 'Metal', 'Dragon', 'Colorless', 'Fairy',
];

class CardInfo {
  final String category;
  final List<String> types;
  // Basic / Stage 1 / Stage 2, Pokemon only -- null for Trainers/Energy and
  // for any Pokemon whose stage wasn't resolvable in the source data.
  final String? stage;
  const CardInfo(this.category, this.types, [this.stage]);
}

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

/// Parses the bundled JSON asset: {"CardName": {"category": ..., "types":
/// [...]}, ...} into a lookup table.
Map<String, CardInfo> parseCategoryLookup(String jsonText) {
  final decoded = jsonDecode(jsonText) as Map<String, dynamic>;
  return decoded.map((name, value) {
    final v = value as Map<String, dynamic>;
    final types = (v['types'] as List<dynamic>).map((t) => t as String).toList();
    return MapEntry(name, CardInfo(v['category'] as String, types, v['stage'] as String?));
  });
}

/// Builds a secondary index keyed by diacritic-stripped name, for matching
/// names typed/pasted without accents. If multiple real names collapse to
/// the same stripped form, the first one wins (rare in practice).
Map<String, CardInfo> buildNormalizedLookup(Map<String, CardInfo> lookup) {
  final normalized = <String, CardInfo>{};
  lookup.forEach((name, info) {
    final key = stripDiacritics(name).toLowerCase();
    normalized.putIfAbsent(key, () => info);
  });
  return normalized;
}

// Matches energy card names not in the lookup, e.g. "Basic Psychic Energy"
// (not in the card database at all -- Basic Energy is evergreen, not tied
// to a set) or a homebrew/future "Shadowy Fire Energy" -- pulls out the
// type keyword anywhere in the name.
String? _typeFromEnergyName(String name) {
  if (!name.toLowerCase().contains('energy')) return null;
  for (final type in pokemonTypes) {
    if (name.contains(type)) return type;
  }
  return null;
}

class ClassifiedCard {
  final String category;
  final String? type; // null when not Pokemon/Energy, or type unknown
  ClassifiedCard(this.category, this.type);
}

ClassifiedCard _classify(
    String name, ParsedDeck deck, Map<String, CardInfo> lookup, Map<String, CardInfo> normalized) {
  final normalizedKey = stripDiacritics(name).toLowerCase();
  CardInfo? info = lookup[name] ?? normalized[normalizedKey];

  if (info != null) {
    return ClassifiedCard(info.category, info.types.isNotEmpty ? info.types.first : null);
  }

  final energyType = _typeFromEnergyName(name);
  if (energyType != null) {
    return ClassifiedCard('Energy', energyType);
  }

  final section = deck.sectionOf[name];
  if (section == 'Pokemon') return ClassifiedCard('Pokemon', null);
  if (section == 'Energy') return ClassifiedCard('Energy', null);
  if (section == 'Trainer') return ClassifiedCard(unknownTrainerCategory, null);
  return ClassifiedCard(unknownCategory, null);
}

/// Collapses a parsed deck's per-card-name counts into category counts.
/// Pokemon and Energy are split by type ("Pokemon (Darkness)") only when
/// [splitByType] is true (default) AND more than one distinct type is
/// present in that category; otherwise they stay as a single
/// "Pokemon"/"Energy" bucket. Pass splitByType: false to always keep the
/// single lumped bucket regardless of type diversity.
Map<String, int> categorize(ParsedDeck deck, Map<String, CardInfo> lookup,
    {Map<String, CardInfo>? normalizedLookup, bool splitByType = true}) {
  final normalized = normalizedLookup ?? buildNormalizedLookup(lookup);

  // First pass: classify every card and bucket by (category, type).
  final byCategoryAndType = <String, Map<String?, int>>{};
  deck.cardCounts.forEach((name, count) {
    final classified = _classify(name, deck, lookup, normalized);
    final byType = byCategoryAndType.putIfAbsent(classified.category, () => {});
    byType[classified.type] = (byType[classified.type] ?? 0) + count;
  });

  // Second pass: only split Pokemon/Energy by type if the toggle is on and
  // >1 distinct type is present (excluding the "unknown type" bucket from
  // that count, since an unrecognized card doesn't tell us anything about
  // type diversity).
  final categoryCounts = <String, int>{};
  byCategoryAndType.forEach((category, byType) {
    final knownTypes = byType.keys.where((t) => t != null).toList();
    final shouldSplit =
        splitByType && (category == 'Pokemon' || category == 'Energy') && knownTypes.length > 1;
    if (shouldSplit) {
      byType.forEach((type, count) {
        final label = type != null ? '$category ($type)' : '$category (Other)';
        categoryCounts[label] = (categoryCounts[label] ?? 0) + count;
      });
    } else {
      final total = byType.values.fold(0, (a, b) => a + b);
      categoryCounts[category] = (categoryCounts[category] ?? 0) + total;
    }
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

/// The smallest number of copies of a category (out of [deckSize] total
/// cards) needed so that P(at least 1 in a [handSize]-card hand) reaches
/// [targetProbability]. Returns null if even all [deckSize] cards being
/// that category wouldn't be enough (impossible unless handSize > deckSize
/// in some degenerate case) or if targetProbability is unreachable below
/// deckSize copies of a single card (deck-building copy limits aside --
/// this is pure math, the UI is responsible for flagging unrealistic counts
/// like "you'd need 40 copies of a card, but only 4 are legal").
int? minimumCountForConfidence(
    int deckSize, int handSize, double targetProbability) {
  for (var count = 1; count <= deckSize; count++) {
    final dist = marginalDistribution(deckSize, count, handSize);
    if (atLeastProbability(dist, 1) >= targetProbability) {
      return count;
    }
  }
  return null;
}

/// Exact probability of a specific hand composition (e.g. a user-entered
/// "optimal" target), independent of enumerating every possible hand.
double compositionProbability(
    Map<String, int> deck, Map<String, int> composition, int handSize) {
  final deckSize = deck.values.fold(0, (a, b) => a + b);
  final totalWays = binomial(deckSize, handSize);
  var ways = 1;
  composition.forEach((category, count) {
    final available = deck[category] ?? 0;
    ways *= binomial(available, count);
  });
  return ways / totalWays;
}

class CategoryModeResult {
  final Map<String, int> categoryCounts;
  final List<HandResult> topCompositions;
  final Map<String, List<MarginalPoint>> marginals;

  CategoryModeResult(this.categoryCounts, this.topCompositions, this.marginals);
}

CategoryModeResult computeCategoryMode(
    ParsedDeck deck, Map<String, CardInfo> lookup, int handSize, int topN,
    {bool splitByType = true}) {
  final categoryCounts = categorize(deck, lookup, splitByType: splitByType);
  final deckSize = categoryCounts.values.fold(0, (a, b) => a + b);

  final topCompositions = topHands(categoryCounts, handSize, topN);

  final marginals = <String, List<MarginalPoint>>{};
  categoryCounts.forEach((category, count) {
    marginals[category] = marginalDistribution(deckSize, count, handSize);
  });

  return CategoryModeResult(categoryCounts, topCompositions, marginals);
}

/// How many Basic/Stage 1/Stage 2 Pokemon are in the deck. [unknown] counts
/// Pokemon-section cards whose stage couldn't be resolved (not in the
/// bundled lookup -- e.g. homebrew, or a future/older card not yet in the
/// Standard-legal pool this app ships with).
class StageBreakdown {
  final int basic;
  final int stage1;
  final int stage2;
  final int unknown;
  StageBreakdown(this.basic, this.stage1, this.stage2, this.unknown);
}

StageBreakdown pokemonStageBreakdown(
    ParsedDeck deck, Map<String, CardInfo> lookup,
    {Map<String, CardInfo>? normalizedLookup}) {
  final normalized = normalizedLookup ?? buildNormalizedLookup(lookup);
  var basic = 0, stage1 = 0, stage2 = 0, unknown = 0;

  deck.cardCounts.forEach((name, count) {
    final normalizedKey = stripDiacritics(name).toLowerCase();
    final info = lookup[name] ?? normalized[normalizedKey];

    if (info == null) {
      if (deck.sectionOf[name] == 'Pokemon') unknown += count;
      return;
    }
    if (info.category != 'Pokemon') return;

    switch (info.stage) {
      case 'Basic':
        basic += count;
        break;
      case 'Stage 1':
        stage1 += count;
        break;
      case 'Stage 2':
        stage2 += count;
        break;
      default:
        unknown += count;
    }
  });

  return StageBreakdown(basic, stage1, stage2, unknown);
}

enum RecommendationLevel { error, warning, info }

class Recommendation {
  final RecommendationLevel level;
  final String message;
  Recommendation(this.level, this.message);
}

// Grounded in commonly-cited Standard deck-building guidance: ~60 cards
// split roughly 12-20 Pokemon / 25-35 Trainer / 8-16 Energy, 6-8 Basic
// Pokemon so you reliably have something to open with, at least a few
// Supporter draw cards, max 4 copies of any one card except Basic Energy.
// These are heuristics, not hard rules (except the legality checks, which
// are marked as errors) -- a deck can reasonably break them for a specific
// strategy.
List<Recommendation> generateRecommendations(
    ParsedDeck deck, Map<String, CardInfo> lookup,
    {Map<String, CardInfo>? normalizedLookup}) {
  final normalized = normalizedLookup ?? buildNormalizedLookup(lookup);
  final lumped =
      categorize(deck, lookup, normalizedLookup: normalized, splitByType: false);

  final pokemonCount = lumped['Pokemon'] ?? 0;
  final energyCount = lumped['Energy'] ?? 0;
  final supporterCount = lumped['Supporter'] ?? 0;
  final trainerCount = (lumped['Supporter'] ?? 0) +
      (lumped['Item'] ?? 0) +
      (lumped['Tool'] ?? 0) +
      (lumped['Stadium'] ?? 0) +
      (lumped[unknownTrainerCategory] ?? 0);
  final deckSize = deck.totalCards;

  final recs = <Recommendation>[];

  if (deckSize != 60) {
    recs.add(Recommendation(RecommendationLevel.error,
        'Deck has $deckSize cards -- Standard decks must have exactly 60.'));
  }

  deck.cardCounts.forEach((name, count) {
    final isBasicEnergy =
        name.toLowerCase().startsWith('basic') && name.toLowerCase().contains('energy');
    if (count > 4 && !isBasicEnergy) {
      recs.add(Recommendation(RecommendationLevel.error,
          '$count copies of "$name" -- the format limit is 4 copies of any card except Basic Energy.'));
    }
  });

  final stages = pokemonStageBreakdown(deck, lookup, normalizedLookup: normalized);
  if (stages.basic == 0) {
    recs.add(Recommendation(RecommendationLevel.error,
        'No confirmed Basic Pokemon -- you need at least one Basic Pokemon to legally start a game.'));
  } else if (stages.basic < 6) {
    recs.add(Recommendation(RecommendationLevel.warning,
        'Only ${stages.basic} confirmed Basic Pokemon -- most decks run 6-8 so you reliably '
        'have something to open with and can rebuild your board after a knockout.'));
  }

  if (pokemonCount < 12) {
    recs.add(Recommendation(RecommendationLevel.warning,
        'Only $pokemonCount Pokemon -- most Standard decks run at least 12-15 so you don\'t '
        'get stranded without an attacker. Consider adding more.'));
  } else if (pokemonCount > 20) {
    recs.add(Recommendation(RecommendationLevel.info,
        '$pokemonCount Pokemon is on the high side -- decks this heavy on Pokemon often '
        'struggle to fit enough draw and search Trainers. Worth double-checking.'));
  }

  if (supporterCount == 0) {
    recs.add(Recommendation(RecommendationLevel.warning,
        'No Supporters recognized in this list -- competitive decks almost always run '
        'several Supporter draw cards to consistently hit their key cards each turn.'));
  }

  if (trainerCount < 22) {
    recs.add(Recommendation(RecommendationLevel.warning,
        'Only $trainerCount Trainer cards -- competitive decks typically run 25-35 (often '
        '30+) since draw and search power is usually what wins games. Consider adding more.'));
  } else if (trainerCount > 38) {
    recs.add(Recommendation(RecommendationLevel.info,
        '$trainerCount Trainer cards is unusually high -- double-check you still have enough '
        'Pokemon and Energy to actually attack.'));
  }

  if (energyCount < 6) {
    recs.add(Recommendation(RecommendationLevel.warning,
        'Only $energyCount Energy -- even decks with strong draw/search support usually want '
        'at least 8-12. Consider adding more.'));
  } else if (energyCount > 18) {
    recs.add(Recommendation(RecommendationLevel.info,
        '$energyCount Energy is on the high side -- most Standard decks run 8-16 and use the '
        'extra slots for Trainers instead.'));
  }

  if (stages.stage2 > 0 && stages.stage1 < (stages.stage2 * 2 - 1)) {
    recs.add(Recommendation(RecommendationLevel.info,
        '${stages.stage2} Stage 2 Pokemon but only ${stages.stage1} Stage 1 Pokemon -- '
        'thin evolution lines are a common source of inconsistency. Make sure each Stage 2 '
        'line has enough Stage 1s (and Basics) backing it up.'));
  }

  return recs;
}
