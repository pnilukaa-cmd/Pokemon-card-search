/// Exact opening-hand odds via the multivariate hypergeometric distribution.
///
/// Given a deck as {card name: count}, computes the exact probability of
/// every possible hand *composition* (a multiset of card names, since two
/// physical copies of the same card are indistinguishable for this purpose)
/// and returns the most likely ones. This is exact math, not a simulation --
/// the probabilities are precise, not estimated.
library hand_odds;

class HandResult {
  final Map<String, int> composition;
  final double probability;

  HandResult(this.composition, this.probability);
}

/// n choose r, computed iteratively to avoid overflow for the ranges this
/// app deals with (deck sizes up to a few hundred, hand sizes up to ~10).
int binomial(int n, int r) {
  if (r < 0 || r > n) return 0;
  if (r > n - r) r = n - r;
  var result = 1;
  for (var i = 0; i < r; i++) {
    result = result * (n - i) ~/ (i + 1);
  }
  return result;
}

/// Enumerates every possible hand composition and its exact probability.
/// Returns the full list, unsorted. For a typical 60-card deck with 15-25
/// unique card names and a 7-card hand this runs in well under a second.
List<HandResult> enumerateHandOdds(Map<String, int> deck, int handSize) {
  final names = deck.keys.toList();
  final maxCounts = names.map((n) => deck[n]!).toList();
  final deckSize = maxCounts.fold(0, (a, b) => a + b);
  final totalWays = binomial(deckSize, handSize);

  // Suffix sums of max counts, for pruning: suffixCapacity[i] = sum of
  // maxCounts[i..end].
  final suffixCapacity = List<int>.filled(names.length + 1, 0);
  for (var i = names.length - 1; i >= 0; i--) {
    suffixCapacity[i] = suffixCapacity[i + 1] + maxCounts[i];
  }

  final results = <HandResult>[];
  final current = <String, int>{};

  void recurse(int idx, int remaining) {
    if (idx == names.length) {
      if (remaining == 0) {
        var ways = 1;
        current.forEach((name, k) {
          ways *= binomial(deck[name]!, k);
        });
        results.add(HandResult(Map.of(current), ways / totalWays));
      }
      return;
    }
    final maxTake = remaining < maxCounts[idx] ? remaining : maxCounts[idx];
    final remainingCapacity = suffixCapacity[idx + 1];
    final minTake = (remaining - remainingCapacity) > 0
        ? remaining - remainingCapacity
        : 0;
    for (var k = minTake; k <= maxTake; k++) {
      if (k > 0) current[names[idx]] = k;
      recurse(idx + 1, remaining - k);
      if (k > 0) current.remove(names[idx]);
    }
  }

  recurse(0, handSize);
  return results;
}

/// Returns the top [n] most probable hand compositions, sorted descending.
List<HandResult> topHands(Map<String, int> deck, int handSize, int n) {
  final all = enumerateHandOdds(deck, handSize);
  all.sort((a, b) => b.probability.compareTo(a.probability));
  return all.take(n).toList();
}
