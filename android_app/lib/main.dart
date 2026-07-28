import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import 'deck_parser.dart';
import 'hand_odds.dart';

void main() => runApp(const DeckOddsApp());

class DeckOddsApp extends StatelessWidget {
  const DeckOddsApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Deck Hand Odds',
      theme: ThemeData(colorSchemeSeed: Colors.deepPurple, useMaterial3: true),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

// Runs in a background isolate via compute() so a large/unusual deck can't
// freeze the UI thread while enumerating hand compositions.
List<HandResult> _computeTopHands(_TopHandsRequest req) {
  return topHands(req.deck, req.handSize, req.n);
}

class _TopHandsRequest {
  final Map<String, int> deck;
  final int handSize;
  final int n;
  _TopHandsRequest(this.deck, this.handSize, this.n);
}

class _HomePageState extends State<HomePage> {
  final _controller = TextEditingController();
  ParsedDeck? _parsedDeck;
  List<HandResult>? _topHands;
  bool _calculating = false;
  String? _error;

  static const _sampleDeck = '''Pokémon: 15
3 Budew PRE 148
3 Frillish WHF 32
3 Jellicent ex WHF 33
3 Eevee SFA 51
3 Espeon ex PRE 62

Trainer: 33
4 Boss's Orders MEG 114
4 Xerosic's Machinations SFA 64
3 Eri TEF 146
3 Lillie's Determination MEG 128
3 Judge POR 74
3 Ultra Ball MEG 131
3 Poke Pad ASC 209
4 Buddy-Buddy Poffin TEF 144
4 Night Stretcher SFA 61

Energy: 12
12 Basic Psychic Energy

Total Cards: 60''';

  Future<void> _calculate() async {
    setState(() {
      _calculating = true;
      _error = null;
      _topHands = null;
    });

    final parsed = parseDecklist(_controller.text);
    setState(() => _parsedDeck = parsed);

    if (parsed.cardCounts.isEmpty) {
      setState(() {
        _calculating = false;
        _error = 'No cards recognized. Paste a Pokemon TCG Live decklist export.';
      });
      return;
    }

    try {
      final result = await compute(
        _computeTopHands,
        _TopHandsRequest(parsed.cardCounts, 7, 5),
      );
      setState(() {
        _topHands = result;
        _calculating = false;
      });
    } catch (e) {
      setState(() {
        _calculating = false;
        _error = 'Could not compute odds: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Deck Opening Hand Odds')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Paste your Pokemon TCG Live decklist export below.',
              style: TextStyle(fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 8),
            Expanded(
              flex: 2,
              child: TextField(
                controller: _controller,
                maxLines: null,
                expands: true,
                textAlignVertical: TextAlignVertical.top,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  hintText: 'Pokémon: 14\n2 Sandile BLK 57\n...',
                ),
              ),
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: _calculating ? null : _calculate,
                    child: Text(_calculating ? 'Calculating...' : 'Calculate Top 5 Opening Hands'),
                  ),
                ),
                const SizedBox(width: 8),
                OutlinedButton(
                  onPressed: _calculating
                      ? null
                      : () => setState(() => _controller.text = _sampleDeck),
                  child: const Text('Load Sample'),
                ),
              ],
            ),
            const SizedBox(height: 16),
            if (_error != null)
              Text(_error!, style: const TextStyle(color: Colors.red)),
            if (_parsedDeck != null && _parsedDeck!.warnings.isNotEmpty)
              ..._parsedDeck!.warnings.map(
                (w) => Text(w, style: const TextStyle(color: Colors.orange)),
              ),
            if (_parsedDeck != null)
              Text('Parsed ${_parsedDeck!.totalCards} cards, '
                  '${_parsedDeck!.cardCounts.length} unique names'),
            const SizedBox(height: 8),
            Expanded(
              flex: 3,
              child: _topHands == null
                  ? const Center(child: Text('Results will appear here.'))
                  : ListView.builder(
                      itemCount: _topHands!.length,
                      itemBuilder: (context, i) {
                        final h = _topHands![i];
                        final desc = h.composition.entries
                            .map((e) => '${e.value}x ${e.key}')
                            .join(', ');
                        return Card(
                          child: ListTile(
                            leading: CircleAvatar(child: Text('${i + 1}')),
                            title: Text('${(h.probability * 100).toStringAsFixed(3)}%'),
                            subtitle: Text(desc),
                          ),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
