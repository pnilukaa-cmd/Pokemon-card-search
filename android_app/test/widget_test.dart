// Basic smoke test: the app launches and shows its main UI elements.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:pokemon_deck_odds/main.dart';

void main() {
  testWidgets('App launches and shows the paste box and calculate button',
      (WidgetTester tester) async {
    await tester.pumpWidget(const DeckOddsApp());

    expect(find.text('Deck Opening Hand Odds'), findsOneWidget);
    expect(find.byType(TextField), findsOneWidget);
    expect(find.text('Calculate Odds'), findsOneWidget);
    expect(find.byType(DropdownButton<DeckSource>), findsOneWidget);
  });

  testWidgets('Loading the sample deck and calculating shows results',
      (WidgetTester tester) async {
    // The results list is long (marginals + top-5 compositions + the target
    // comparison section). Widen the test surface so ListView doesn't cull
    // off-screen items out of the element tree before we assert on them.
    tester.view.physicalSize = const Size(800, 6000);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(const DeckOddsApp());

    // Open the format dropdown and select "Load Sample Deck" to fill the
    // paste box with a real example.
    await tester.tap(find.byType(DropdownButton<DeckSource>));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Load Sample Deck').last);
    await tester.pump();

    // compute() spawns a real isolate; testWidgets runs in a fake-async
    // zone by default that a real isolate's work won't advance, so
    // pumpAndSettle alone hangs waiting on it forever. runAsync() steps
    // outside the fake zone to let real async/isolate work actually finish.
    await tester.runAsync(() async {
      await tester.tap(find.text('Calculate Odds'));
      await Future<void>.delayed(const Duration(seconds: 2));
    });
    await tester.pump();

    expect(find.text('At least 1 in opening hand:'), findsOneWidget);
    expect(find.text('Top 5 most likely hand shapes:'), findsOneWidget);
  });

  testWidgets(
      'Type-split categories, confidence hints, and optimal-hand comparison work',
      (WidgetTester tester) async {
    tester.view.physicalSize = const Size(800, 6000);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(const DeckOddsApp());

    await tester.tap(find.byType(DropdownButton<DeckSource>));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Load Sample Deck').last);
    await tester.pump();

    await tester.runAsync(() async {
      await tester.tap(find.text('Calculate Odds'));
      await Future<void>.delayed(const Duration(seconds: 2));
    });
    await tester.pump();

    // The sample deck has 3 Pokemon types (Budew=Grass, Eevee=Colorless,
    // the rest Psychic), so Pokemon should type-split; Energy is genuinely
    // mono-Psychic so it should NOT split.
    expect(find.text('Pokemon (Psychic)'), findsWidgets);
    expect(find.text('Pokemon (Grass)'), findsWidgets);
    expect(find.text('Pokemon (Colorless)'), findsWidgets);
    expect(find.text('Energy'), findsWidgets);
    expect(find.text('Pokemon'), findsNothing); // lumped bucket shouldn't exist once split

    // Confidence calculator section is present with its dropdown.
    expect(find.text('Target confidence: '), findsOneWidget);

    // Optimal-hand section: pre-filled from the #1 most likely composition,
    // then editable and computable.
    expect(find.text('Set your optimal hand:'), findsOneWidget);
    expect(find.text('Calculate My Target\'s Odds'), findsOneWidget);

    await tester.tap(find.text('Calculate My Target\'s Odds'));
    await tester.pump();

    // Pre-filled values come straight from the #1 composition, so they
    // should already sum to 7 and produce a result with no error.
    expect(find.textContaining('Your target hand:'), findsOneWidget);
    // "currently" only appears in the error message (e.g. "currently 5"),
    // not the static instructional text, so this confirms no error fired.
    expect(find.textContaining('currently'), findsNothing);
  });

  testWidgets('Deck-building recommendations flag a genuinely bad decklist',
      (WidgetTester tester) async {
    tester.view.physicalSize = const Size(800, 6000);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(const DeckOddsApp());

    // A deliberately bad decklist: 5 copies of a card (illegal), no
    // Supporters, too few Trainers, too few Basic Pokemon.
    const badDeck = '''Pokémon: 24
2 Dreepy TWM 130
1 Drakloak TWM 131
4 Dragapult ex TWM 132
4 Snorunt TWM 60
4 Froslass TWM 61
9 Munkidori TWM 125

Trainer: 21
5 Ultra Ball MEG 131
4 Nest Ball SVI 181
4 Buddy-Buddy Poffin TEF 144
4 Rare Candy SSP 189
4 Counter Catcher PAR 160

Energy: 15
15 Basic Fire Energy''';

    await tester.enterText(find.byType(TextField).first, badDeck);
    await tester.runAsync(() async {
      await tester.tap(find.text('Calculate Odds'));
      await Future<void>.delayed(const Duration(seconds: 2));
    });
    await tester.pump();

    expect(find.text('Deck-building recommendations:'), findsOneWidget);
    expect(
        find.textContaining('copies of "Ultra Ball"'), findsOneWidget);
    expect(find.textContaining('No Supporters recognized'), findsOneWidget);
  });

  testWidgets('A well-built sample deck shows no recommendations',
      (WidgetTester tester) async {
    tester.view.physicalSize = const Size(800, 6000);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(const DeckOddsApp());

    await tester.tap(find.byType(DropdownButton<DeckSource>));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Load Sample Deck').last);
    await tester.pump();

    await tester.runAsync(() async {
      await tester.tap(find.text('Calculate Odds'));
      await Future<void>.delayed(const Duration(seconds: 2));
    });
    await tester.pump();

    expect(find.text('Deck-building recommendations:'), findsNothing);
  });

  testWidgets('Type-split toggle off keeps a single lumped Pokemon/Energy bucket',
      (WidgetTester tester) async {
    tester.view.physicalSize = const Size(800, 6000);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    await tester.pumpWidget(const DeckOddsApp());

    await tester.tap(find.byType(DropdownButton<DeckSource>));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Load Sample Deck').last);
    await tester.pump();

    // Turn the type-split toggle off before calculating.
    expect(find.text('Split Pokemon/Energy by type'), findsOneWidget);
    await tester.tap(find.byType(Switch));
    await tester.pump();

    await tester.runAsync(() async {
      await tester.tap(find.text('Calculate Odds'));
      await Future<void>.delayed(const Duration(seconds: 2));
    });
    await tester.pump();

    // With the toggle off, Pokemon should stay a single bucket even though
    // this deck genuinely has 3 Pokemon types.
    expect(find.text('Pokemon'), findsWidgets);
    expect(find.text('Pokemon (Psychic)'), findsNothing);
    expect(find.text('Pokemon (Grass)'), findsNothing);
    expect(find.text('Pokemon (Colorless)'), findsNothing);
  });
}
