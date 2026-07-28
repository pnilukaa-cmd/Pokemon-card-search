import '../lib/hand_odds.dart';
import '../lib/deck_parser.dart';

void main() {
  final deck = <String, int>{
    'Budew': 3, 'Frillish': 3, 'Jellicent ex': 3, 'Eevee': 3, 'Espeon ex': 3,
    "Boss's Orders": 4, "Xerosic's Machinations": 3, 'Eri': 3,
    "Lillie's Determination": 4, 'Judge': 3,
    'Ultra Ball': 3, 'Poke Pad': 3, 'Buddy-Buddy Poffin': 4, 'Night Stretcher': 4,
    'Basic Psychic Energy': 14,
  };
  final deckSize = deck.values.fold(0, (a, b) => a + b);
  print('Deck size: $deckSize (expect 60)');

  final all = enumerateHandOdds(deck, 7);
  final totalProb = all.fold(0.0, (sum, h) => sum + h.probability);
  print('Distinct hand compositions: ${all.length} (expect 109000)');
  print('Total probability: ${totalProb.toStringAsFixed(6)} (expect 1.000000)');

  final top5 = topHands(deck, 7, 5);
  print('\nTop 5 most likely opening hands:');
  for (final h in top5) {
    final desc = h.composition.entries
        .map((e) => '${e.value}x ${e.key}')
        .join(', ');
    print('  ${(h.probability * 100).toStringAsFixed(3)}%  $desc');
  }

  // --- Parser test ---
  const importText = '''
Pokémon: 14
2 Sandile BLK 57
1 Krokorok BLK 58
2 Krookodile BLK 59

Trainer: 34
4 Boss's Orders MEG 114

Energy: 12
12 Basic Darkness Energy

Total Cards: 60
''';
  final parsed = parseDecklist(importText);
  print('\nParser test:');
  print('  Parsed counts: ${parsed.cardCounts}');
  print('  Total cards: ${parsed.totalCards} (expect 19 for this snippet)');
  print('  Warnings: ${parsed.warnings}');

  final sandileOk = parsed.cardCounts['Sandile'] == 2;
  final bossOk = parsed.cardCounts["Boss's Orders"] == 4;
  final energyOk = parsed.cardCounts['Basic Darkness Energy'] == 12;
  print('  Sandile parsed as name only (no BLK 57): $sandileOk');
  print("  Boss's Orders parsed correctly: $bossOk");
  print('  Basic Darkness Energy (no set code) parsed correctly: $energyOk');

  if (!sandileOk || !bossOk || !energyOk) {
    throw Exception('Parser test FAILED');
  }
  if ((totalProb - 1.0).abs() > 0.0001) {
    throw Exception('Probability sum FAILED');
  }
  print('\nALL CHECKS PASSED');
}
