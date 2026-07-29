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
    // The results list is long (marginals + top-5 compositions). Widen the
    // test surface so ListView doesn't cull off-screen items out of the
    // element tree before we assert on them.
    tester.view.physicalSize = const Size(800, 2400);
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
}
