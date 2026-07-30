import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;

import 'card_categories.dart';
import 'deck_builder.dart';
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

enum DeckSource {
  ptcgLive('Pokémon TCG Live'),
  pokemonCardIo('PokemonCard.io'),
  limitless('Limitless TCG'),
  loadSample('Load Sample Deck');

  final String label;
  const DeckSource(this.label);
}

// Short reference examples shown below the format dropdown so you know what
// to paste. The parser itself tries every known suffix pattern regardless
// of which source is selected, so this is just a helper, not a strict mode.
const Map<DeckSource, String> _formatExamples = {
  DeckSource.ptcgLive: 'Pokémon: 14\n2 Sandile BLK 57\n1 Krokorok BLK 58\n\n'
      "Trainer: 34\n4 Boss's Orders MEG 114\n\nEnergy: 12\n12 Basic Darkness Energy",
  DeckSource.pokemonCardIo: '// PokemonCard.io Deck List\n'
      '1 Arven sv1-166\n5 Basic Darkness Energy sve-7',
  // Limitless's "Share > Copy as Text" export uses the same space-separated
  // "SETCODE NUMBER" shape as PTCG Live (confirmed from a public example:
  // "2 Pikachu A1 94"), so it should already parse correctly -- this is
  // lower-confidence than the other two since their docs page couldn't be
  // fetched directly to fully confirm section headers. If a real Limitless
  // export doesn't parse, paste it here and it can be fixed.
  DeckSource.limitless: '2 Sandile BLK 57\n1 Krokorok BLK 58\n1 Krookodile BLK 59',
};

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

_CategoryModeResponse _computeCategoryMode(_CategoryModeRequest req) {
  final result = computeCategoryMode(req.deck, req.lookup, req.handSize, req.n,
      splitByType: req.splitByType);
  final recommendations = generateRecommendations(req.deck, req.lookup);
  return _CategoryModeResponse(result, recommendations);
}

class _CategoryModeResponse {
  final CategoryModeResult result;
  final List<Recommendation> recommendations;
  _CategoryModeResponse(this.result, this.recommendations);
}

class _CategoryModeRequest {
  final ParsedDeck deck;
  final Map<String, CardInfo> lookup;
  final int handSize;
  final int n;
  final bool splitByType;
  _CategoryModeRequest(this.deck, this.lookup, this.handSize, this.n, this.splitByType);
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final _controller = TextEditingController();
  OddsMode _mode = OddsMode.byCategory;
  DeckSource _source = DeckSource.ptcgLive;
  bool _splitByType = true;

  ParsedDeck? _parsedDeck;
  List<HandResult>? _exactTopHands;
  CategoryModeResult? _categoryResult;
  List<Recommendation>? _recommendations;
  Map<String, CardInfo>? _categoryLookup;

  bool _calculating = false;
  String? _error;

  // Confidence calculator: "how many copies do I need for X% chance of at
  // least 1 in my opening hand?"
  double _confidenceTarget = 0.90;

  // Optimal-hand comparison: user types a target count per category, we
  // show the exact probability of that specific composition and compare it
  // to the single most likely shape.
  final Map<String, TextEditingController> _targetControllers = {};
  double? _targetProbability;
  String? _targetError;

  // "Build a deck around one Pokemon" section.
  final _pokemonNameController = TextEditingController();
  Map<String, PokemonCardInfo>? _cardPool;
  bool _buildingDeck = false;
  String? _deckBuilderError;
  List<String>? _deckBuilderSuggestions;
  List<String>? _deckBuilderNotes;

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

  @override
  void dispose() {
    _controller.dispose();
    _pokemonNameController.dispose();
    for (final c in _targetControllers.values) {
      c.dispose();
    }
    super.dispose();
  }

  Future<Map<String, PokemonCardInfo>> _loadCardPool() async {
    if (_cardPool != null) return _cardPool!;
    final jsonText = await rootBundle.loadString('assets/card_pool.json');
    _cardPool = parseCardPool(jsonText);
    return _cardPool!;
  }

  Future<void> _buildDeckFromPokemon() async {
    final query = _pokemonNameController.text.trim();
    if (query.isEmpty) return;

    setState(() {
      _buildingDeck = true;
      _deckBuilderError = null;
      _deckBuilderSuggestions = null;
      _deckBuilderNotes = null;
    });

    final pool = await _loadCardPool();
    final generated = buildDeckForPokemon(query, pool);

    if (generated == null) {
      setState(() {
        _buildingDeck = false;
        _deckBuilderError = 'No Pokemon named "$query" found in the Standard-legal pool.';
        _deckBuilderSuggestions = suggestNames(query, pool);
      });
      return;
    }

    setState(() {
      _controller.text = generated.toDecklistText();
      _deckBuilderNotes = generated.notes;
      _buildingDeck = false;
      _mode = OddsMode.byCategory;
    });
    await _calculate();
  }

  void _resetTargetControllers(Iterable<String> categories, {Map<String, int>? prefill}) {
    for (final c in _targetControllers.values) {
      c.dispose();
    }
    _targetControllers.clear();
    for (final category in categories) {
      final startValue = prefill?[category];
      _targetControllers[category] =
          TextEditingController(text: startValue != null && startValue > 0 ? '$startValue' : '');
    }
    _targetProbability = null;
    _targetError = null;
  }

  void _calculateTargetOdds() {
    final result = _categoryResult;
    if (result == null) return;

    final composition = <String, int>{};
    var sum = 0;
    var anyInvalid = false;
    for (final entry in _targetControllers.entries) {
      final text = entry.value.text.trim();
      if (text.isEmpty) continue;
      final value = int.tryParse(text);
      if (value == null || value < 0) {
        anyInvalid = true;
        continue;
      }
      if (value > 0) composition[entry.key] = value;
      sum += value;
    }

    if (anyInvalid) {
      setState(() {
        _targetError = 'Enter whole numbers only.';
        _targetProbability = null;
      });
      return;
    }
    if (sum != 7) {
      setState(() {
        _targetError = 'Target counts must add up to 7 (currently $sum).';
        _targetProbability = null;
      });
      return;
    }

    final prob = compositionProbability(result.categoryCounts, composition, 7);
    setState(() {
      _targetError = null;
      _targetProbability = prob;
    });
  }

  Future<Map<String, CardInfo>> _loadLookup() async {
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
      _recommendations = null;
    });

    final parsed = parseDecklist(_controller.text);
    setState(() => _parsedDeck = parsed);

    if (parsed.cardCounts.isEmpty) {
      setState(() {
        _calculating = false;
        _error = 'No cards recognized. Paste a decklist export from Pokémon TCG '
            'Live, PokemonCard.io, or Limitless TCG (see the format examples '
            'below the dropdown).';
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
        final response = await compute(
          _computeCategoryMode,
          _CategoryModeRequest(parsed, lookup, 7, 5, _splitByType),
        );
        final result = response.result;
        setState(() {
          _categoryResult = result;
          _recommendations = response.recommendations;
          final topComposition =
              result.topCompositions.isNotEmpty ? result.topCompositions.first.composition : null;
          _resetTargetControllers(result.categoryCounts.keys, prefill: topComposition);
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
            _buildDeckGeneratorSection(),
            const Divider(),
            const Text(
              'Paste a decklist export below (Pokémon TCG Live, PokemonCard.io, or Limitless TCG).',
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
            if (_mode == OddsMode.byCategory)
              SwitchListTile(
                dense: true,
                contentPadding: EdgeInsets.zero,
                title: const Text('Split Pokemon/Energy by type',
                    style: TextStyle(fontSize: 13)),
                subtitle: const Text(
                  'When off, "Pokemon" and "Energy" stay as single buckets even in a multi-type deck.',
                  style: TextStyle(fontSize: 11),
                ),
                value: _splitByType,
                onChanged: (v) => setState(() => _splitByType = v),
              ),
            const SizedBox(height: 8),
            Row(
              children: [
                const Text('Format:'),
                const SizedBox(width: 8),
                DropdownButton<DeckSource>(
                  value: _source,
                  items: DeckSource.values
                      .map((s) => DropdownMenuItem(value: s, child: Text(s.label)))
                      .toList(),
                  onChanged: _calculating
                      ? null
                      : (s) {
                          if (s == null) return;
                          setState(() {
                            _source = s;
                            if (s == DeckSource.loadSample) {
                              _controller.text = _sampleDeck;
                            }
                          });
                        },
                ),
              ],
            ),
            if (_source != DeckSource.loadSample)
              Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Text(
                  'Example:\n${_formatExamples[_source]}',
                  style: const TextStyle(fontSize: 11, color: Colors.grey),
                ),
              ),
            const SizedBox(height: 8),
            ElevatedButton(
              onPressed: _calculating ? null : _calculate,
              child: Text(_calculating ? 'Calculating...' : 'Calculate Odds'),
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

  Widget _buildDeckGeneratorSection() {
    return ExpansionTile(
      tilePadding: EdgeInsets.zero,
      title: const Text('Build a deck around one Pokémon',
          style: TextStyle(fontWeight: FontWeight.w600)),
      subtitle: const Text(
        'Type a Pokémon name and generate a playable 60-card starting-point decklist.',
        style: TextStyle(fontSize: 11, color: Colors.grey),
      ),
      children: [
        Row(
          children: [
            Expanded(
              child: TextField(
                controller: _pokemonNameController,
                decoration: const InputDecoration(
                  isDense: true,
                  border: OutlineInputBorder(),
                  hintText: 'e.g. Feraligatr, Lurantis ex, Pikachu',
                ),
                onSubmitted: (_) => _buildingDeck ? null : _buildDeckFromPokemon(),
              ),
            ),
            const SizedBox(width: 8),
            ElevatedButton(
              onPressed: _buildingDeck ? null : _buildDeckFromPokemon,
              child: Text(_buildingDeck ? 'Building...' : 'Build Deck'),
            ),
          ],
        ),
        if (_deckBuilderError != null)
          Padding(
            padding: const EdgeInsets.only(top: 8),
            child: Text(_deckBuilderError!, style: const TextStyle(color: Colors.red)),
          ),
        if (_deckBuilderSuggestions != null && _deckBuilderSuggestions!.isNotEmpty)
          Padding(
            padding: const EdgeInsets.only(top: 4),
            child: Text('Did you mean: ${_deckBuilderSuggestions!.join(', ')}?',
                style: const TextStyle(fontSize: 12, color: Colors.grey)),
          ),
        if (_deckBuilderNotes != null) ...[
          const SizedBox(height: 8),
          const Align(
            alignment: Alignment.centerLeft,
            child: Text('Generated -- pasted below and calculated automatically:',
                style: TextStyle(fontSize: 12, fontWeight: FontWeight.w600)),
          ),
          ..._deckBuilderNotes!.map((n) => Padding(
                padding: const EdgeInsets.only(top: 2),
                child: Text('• $n', style: const TextStyle(fontSize: 11)),
              )),
        ],
        const SizedBox(height: 8),
      ],
    );
  }

  Widget _buildRecommendationTile(Recommendation r) {
    final IconData icon;
    final Color color;
    switch (r.level) {
      case RecommendationLevel.error:
        icon = Icons.error;
        color = Colors.red;
        break;
      case RecommendationLevel.warning:
        icon = Icons.warning_amber;
        color = Colors.orange;
        break;
      case RecommendationLevel.info:
        icon = Icons.info_outline;
        color = Colors.blueGrey;
        break;
    }
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: color, size: 18),
          const SizedBox(width: 6),
          Expanded(child: Text(r.message, style: TextStyle(fontSize: 12, color: color))),
        ],
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
    final deckSize = result.categoryCounts.values.fold(0, (a, b) => a + b);

    return ListView(
      children: [
        if (_recommendations != null && _recommendations!.isNotEmpty) ...[
          const Text('Deck-building recommendations:',
              style: TextStyle(fontWeight: FontWeight.bold)),
          ..._recommendations!.map((r) => _buildRecommendationTile(r)),
          const Divider(),
        ],
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text('At least 1 in opening hand:',
                style: TextStyle(fontWeight: FontWeight.bold)),
            Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text('Target confidence: ', style: TextStyle(fontSize: 12)),
                DropdownButton<double>(
                  value: _confidenceTarget,
                  items: const [0.80, 0.90, 0.95, 0.99]
                      .map((v) => DropdownMenuItem(
                          value: v, child: Text('${(v * 100).round()}%')))
                      .toList(),
                  onChanged: (v) {
                    if (v != null) setState(() => _confidenceTarget = v);
                  },
                ),
              ],
            ),
          ],
        ),
        ...result.marginals.entries.map((e) {
          final atLeast1 = atLeastProbability(e.value, 1);
          final currentCount = result.categoryCounts[e.key] ?? 0;
          final neededCount =
              minimumCountForConfidence(deckSize, 7, _confidenceTarget);
          final needMore = neededCount != null && neededCount > currentCount;
          return ListTile(
            dense: true,
            title: Text(e.key),
            subtitle: needMore
                ? Text(
                    'Have $currentCount -- need ~$neededCount for '
                    '${(_confidenceTarget * 100).round()}% confidence',
                    style: const TextStyle(fontSize: 11, color: Colors.orange))
                : Text('Have $currentCount -- already meets '
                    '${(_confidenceTarget * 100).round()}% target',
                    style: const TextStyle(fontSize: 11, color: Colors.green)),
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
        const Divider(),
        const Text('Set your optimal hand:', style: TextStyle(fontWeight: FontWeight.bold)),
        const Text(
          'Pre-filled with the #1 most likely shape as a starting point -- '
          'edit to set your own ideal 7-card opening hand (must add up to '
          '7), then compare its exact odds against the most likely shape above.',
          style: TextStyle(fontSize: 11, color: Colors.grey),
        ),
        const SizedBox(height: 4),
        Wrap(
          spacing: 12,
          runSpacing: 4,
          children: result.categoryCounts.keys.map((category) {
            return SizedBox(
              width: 140,
              child: TextField(
                controller: _targetControllers[category],
                keyboardType: TextInputType.number,
                decoration: InputDecoration(labelText: category, isDense: true),
              ),
            );
          }).toList(),
        ),
        const SizedBox(height: 8),
        ElevatedButton(
          onPressed: _calculateTargetOdds,
          child: const Text('Calculate My Target\'s Odds'),
        ),
        if (_targetError != null)
          Padding(
            padding: const EdgeInsets.only(top: 4),
            child: Text(_targetError!, style: const TextStyle(color: Colors.red)),
          ),
        if (_targetProbability != null)
          Padding(
            padding: const EdgeInsets.only(top: 4),
            child: Builder(builder: (context) {
              final best = result.topCompositions.isNotEmpty
                  ? result.topCompositions.first.probability
                  : null;
              final pctText = (_targetProbability! * 100).toStringAsFixed(3);
              final comparison = best != null
                  ? ' (the single most likely shape is ${(best * 100).toStringAsFixed(2)}%)'
                  : '';
              return Text(
                'Your target hand: $pctText% chance$comparison',
                style: const TextStyle(fontWeight: FontWeight.bold),
              );
            }),
          ),
      ],
    );
  }
}
