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
/// with a leading integer count (section headers, blank lines) are skipped
/// as card entries, but the "Pokémon:" / "Trainer:" / "Energy:" section
/// headers are tracked per card as a fallback category (see
/// card_categories.dart), used when a card name isn't in the bundled
/// name -> category lookup.
library deck_parser;

class ParsedDeck {
  final Map<String, int> cardCounts;
  // Section a card name was found under in the pasted list (Pokemon/Trainer/
  // Energy), used as a fallback category when the name isn't recognized.
  final Map<String, String> sectionOf;
  final List<String> warnings;

  ParsedDeck(this.cardCounts, this.sectionOf, this.warnings);

  int get totalCards => cardCounts.values.fold(0, (a, b) => a + b);
}

// Count may be a decimal (e.g. Limitless TCG's "archetype average" export
// shows fractional counts like "1.89" or "0.01" -- see the rounding/warning
// handling below).
final RegExp _cardLine = RegExp(r'^(\d+(?:\.\d+)?)\s+(.+)$');
final RegExp _commentLine = RegExp(r'^//');
// Matches "Pokémon: 14" (PTCG Live) and "Pokémon (17.48)" (Limitless TCG).
final RegExp _sectionHeader =
    RegExp(r'^(Pok[eé]mon|Trainer(\s+Cards)?|Energy)\s*[:(]', caseSensitive: false);

// Trailing set-code/number suffixes to strip, tried in order. Different
// sites format these differently:
//   PTCG Live:      "Sandile BLK 57"      -> code and number space-separated
//   PokemonCard.io: "Allister swsh4-146"  -> code-number as one hyphenated token
final List<RegExp> _setSuffixPatterns = [
  RegExp(r'\s+[A-Za-z0-9]{2,8}\s+\d+[a-zA-Z]?$'),
  RegExp(r'\s+[A-Za-z0-9]+-[A-Za-z0-9]+$'),
];

String? _normalizeSection(String raw) {
  final lower = raw.toLowerCase();
  if (lower.startsWith('pok')) return 'Pokemon';
  if (lower.startsWith('trainer')) return 'Trainer';
  if (lower.startsWith('energy')) return 'Energy';
  return null;
}

ParsedDeck parseDecklist(String text) {
  final counts = <String, int>{};
  final sectionOf = <String, String>{};
  final warnings = <String>[];
  String? currentSection;
  var roundedCount = 0;

  for (final rawLine in text.split('\n')) {
    final line = rawLine.trim();
    if (line.isEmpty || _commentLine.hasMatch(line)) continue;

    final headerMatch = _sectionHeader.firstMatch(line);
    if (headerMatch != null) {
      currentSection = _normalizeSection(headerMatch.group(1)!);
      continue;
    }

    final match = _cardLine.firstMatch(line);
    if (match == null) continue; // unrecognized line (e.g. "Total Cards: 60"), skip

    final rawCount = double.parse(match.group(1)!);
    final count = rawCount.round();
    if (rawCount != count) roundedCount++;
    if (count == 0) continue; // rounds to nothing, e.g. a 0.01 "average" entry
    var name = match.group(2)!.trim();

    // Strip a trailing set code + number if present, e.g. "Sandile BLK 57"
    // or "Allister swsh4-146" both become just the card name.
    for (final pattern in _setSuffixPatterns) {
      final suffixMatch = pattern.firstMatch(name);
      if (suffixMatch != null) {
        name = name.substring(0, suffixMatch.start).trim();
        break;
      }
    }

    if (name.isEmpty) {
      warnings.add('Could not parse card name from line: "$line"');
      continue;
    }

    counts[name] = (counts[name] ?? 0) + count;
    if (currentSection != null) {
      sectionOf[name] = currentSection;
    }
  }

  if (roundedCount > 0) {
    warnings.add('$roundedCount card count(s) were not whole numbers and got '
        'rounded -- this looks like a statistical/average decklist (e.g. a '
        "Limitless \"archetype average\" view), not one player's actual "
        'deck. Results below are only meaningful for a real single 60-card '
        'decklist.');
  }

  final deck = ParsedDeck(counts, sectionOf, warnings);
  if (deck.totalCards != 60) {
    deck.warnings.add('Deck has ${deck.totalCards} cards, expected 60.');
  }
  return deck;
}
