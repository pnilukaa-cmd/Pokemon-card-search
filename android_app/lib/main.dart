import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;

import 'card_categories.dart';
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

enum OddsMode { exactHands, byCategory }

// --- Background-isolate work, kept as free functions + plain-data request
// objects so compute() can run them off the UI thread. ---

List<HandResult> _computeExactHands(_ExactHandsRequest req) {
  return topHands(req.deck, req.handSize, req.n);
}

class _ExactHandsRequest {
  final Map<String, int> deck;
  final int handSize;
  final int n;
  _ExactHandsRequest(this.deck, this.handSize, this.n);
}

CategoryModeResult _computeCategoryMode(_CategoryModeRequest req) {
  return computeCategoryMode(req.deck, req.lookup, req.handSize, req.n);
}

class _CategoryModeRequest {
  final ParsedDeck deck;
  final Map<String, String> lookup;
  final int handSize;
  final int n;
  _CategoryModeRequest(this.deck, this.lookup, this.handSize, this.n);
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final _controller = TextEditingController();
  OddsMode _mode = OddsMode.byCategory;

  ParsedDeck? _parsedDeck;
  List<HandResult>? _exactTopHands;
  CategoryModeResult? _categoryResult;
  Map<String, String>? _categoryLookup;

  bool _calculating = false;
  String? _error;

  static const _sampleDeck = '''Pokémon: 15
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
3 Poké Pad ASC 209
4 Buddy-Buddy Poffin TEF 144
4 Night Stretcher SFA 61

Energy: 14
14 Basic Psychic Energy

Total Cards: 60''';

  Future<Map<String, String>> _loadLookup() async {
    if (_categoryLookup != null) return _categoryLookup!;
    final jsonText = await rootBundle.loadString('assets/card_categories.json');
    _categoryLookup = parseCategoryLookup(jsonText);
    return _categoryLookup!;
  }

  Future<void> _calculate() async {
    setState(() {
      _calculating = true;
      _error = null;
      _exactTopHands = null;
      _categoryResult = null;
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
      if (_mode == OddsMode.exactHands) {
        final result = await compute(
          _computeExactHands,
          _ExactHandsRequest(parsed.cardCounts, 7, 5),
        );
        setState(() {
          _exactTopHands = result;
          _calculating = false;
        });
      } else {
        final lookup = await _loadLookup();
        final result = await compute(
          _computeCategoryMode,
          _CategoryModeRequest(parsed, lookup, 7, 5),
        );
        setState(() {
          _categoryResult = result;
          _calculating = false;
        });
      }
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
            SegmentedButton<OddsMode>(
              segments: const [
                ButtonSegment(
                    value: OddsMode.byCategory,
                    label: Text('By Category'),
                    icon: Icon(Icons.pie_chart)),
                ButtonSegment(
                    value: OddsMode.exactHands,
                    label: Text('Exact Hands'),
                    icon: Icon(Icons.grid_view)),
              ],
              selected: {_mode},
              onSelectionChanged: (s) => setState(() => _mode = s.first),
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: _calculating ? null : _calculate,
                    child: Text(_calculating ? 'Calculating...' : 'Calculate Odds'),
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
            Expanded(flex: 4, child: _buildResults()),
          ],
        ),
      ),
    );
  }

  Widget _buildResults() {
    if (_mode == OddsMode.exactHands) {
      final hands = _exactTopHands;
      if (hands == null) {
        return const Center(child: Text('Results will appear here.'));
      }
      return ListView.builder(
        itemCount: hands.length,
        itemBuilder: (context, i) {
          final h = hands[i];
          final desc =
              h.composition.entries.map((e) => '${e.value}x ${e.key}').join(', ');
          return Card(
            child: ListTile(
              leading: CircleAvatar(child: Text('${i + 1}')),
              title: Text('${(h.probability * 100).toStringAsFixed(3)}%'),
              subtitle: Text(desc),
            ),
          );
        },
      );
    }

    final result = _categoryResult;
    if (result == null) {
      return const Center(child: Text('Results will appear here.'));
    }

    return ListView(
      children: [
        const Text('At least 1 in opening hand:', style: TextStyle(fontWeight: FontWeight.bold)),
        ...result.marginals.entries.map((e) {
          final atLeast1 = atLeastProbability(e.value, 1);
          return ListTile(
            dense: true,
            title: Text(e.key),
            trailing: Text('${(atLeast1 * 100).toStringAsFixed(1)}%'),
          );
        }),
        const Divider(),
        const Text('Top 5 most likely hand shapes:', style: TextStyle(fontWeight: FontWeight.bold)),
        ...result.topCompositions.asMap().entries.map((entry) {
          final i = entry.key;
          final h = entry.value;
          final desc =
              h.composition.entries.map((e) => '${e.value}x ${e.key}').join(', ');
          return Card(
            child: ListTile(
              leading: CircleAvatar(child: Text('${i + 1}')),
              title: Text('${(h.probability * 100).toStringAsFixed(2)}%'),
              subtitle: Text(desc),
            ),
          );
        }),
      ],
    );
  }
}
