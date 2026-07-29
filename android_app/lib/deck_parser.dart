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

final RegExp _cardLine = RegExp(r'^(\d+)\s+(.+)$');
// Matches a trailing "SETCODE NUMBER" suffix, e.g. " BLK 57" or " MEG 114".
final RegExp _setSuffix = RegExp(r'\s+[A-Za-z0-9]{2,6}\s+\d+[a-zA-Z]?$');
final RegExp _sectionHeader =
    RegExp(r'^(Pok[eé]mon|Trainer(\s+Cards)?|Energy)\s*:', caseSensitive: false);

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

  for (final rawLine in text.split('\n')) {
    final line = rawLine.trim();
    if (line.isEmpty) continue;

    final headerMatch = _sectionHeader.firstMatch(line);
    if (headerMatch != null) {
      currentSection = _normalizeSection(headerMatch.group(1)!);
      continue;
    }

    final match = _cardLine.firstMatch(line);
    if (match == null) continue; // unrecognized line (e.g. "Total Cards: 60"), skip

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
    if (currentSection != null) {
      sectionOf[name] = currentSection;
    }
  }

  final deck = ParsedDeck(counts, sectionOf, warnings);
  if (deck.totalCards != 60) {
    deck.warnings.add('Deck has ${deck.totalCards} cards, expected 60.');
  }
  return deck;
}
