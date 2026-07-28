/// Parses a Pokemon TCG Live decklist import block into a card-name -> count
/// map. Handles the standard export format:
///
/// ```
/// Pokémon: 14
/// 2 Sandile BLK 57
/// 1 Krokorok BLK 58
///
/// Trainer: 34
/// 4 Boss's Orders MEG 114
///
/// Energy: 12
/// 12 Basic Darkness Energy
/// ```
///
/// Set-code + number suffixes (e.g. "BLK 57") are stripped since only the
/// card name and count matter for hand-odds math. Lines that don't start
/// with a leading integer count (section headers, blank lines) are skipped.
library deck_parser;

class ParsedDeck {
  final Map<String, int> cardCounts;
  final List<String> warnings;

  ParsedDeck(this.cardCounts, this.warnings);

  int get totalCards => cardCounts.values.fold(0, (a, b) => a + b);
}

final RegExp _cardLine = RegExp(r'^(\d+)\s+(.+)$');
// Matches a trailing "SETCODE NUMBER" suffix, e.g. " BLK 57" or " MEG 114".
final RegExp _setSuffix = RegExp(r'\s+[A-Za-z0-9]{2,6}\s+\d+[a-zA-Z]?$');

ParsedDeck parseDecklist(String text) {
  final counts = <String, int>{};
  final warnings = <String>[];

  for (final rawLine in text.split('\n')) {
    final line = rawLine.trim();
    if (line.isEmpty) continue;

    final match = _cardLine.firstMatch(line);
    if (match == null) continue; // header/section line, skip

    final count = int.parse(match.group(1)!);
    var name = match.group(2)!.trim();

    // Strip a trailing set code + number if present (e.g. "Sandile BLK 57" -> "Sandile").
    final suffixMatch = _setSuffix.firstMatch(name);
    if (suffixMatch != null) {
      name = name.substring(0, suffixMatch.start).trim();
    }

    if (name.isEmpty) {
      warnings.add('Could not parse card name from line: "$line"');
      continue;
    }

    counts[name] = (counts[name] ?? 0) + count;
  }

  final deck = ParsedDeck(counts, warnings);
  if (deck.totalCards != 60) {
    deck.warnings.add(
        'Deck has ${deck.totalCards} cards, expected 60.');
  }
  return deck;
}
