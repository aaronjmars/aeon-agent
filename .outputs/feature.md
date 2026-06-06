*Feature Built — 2026-06-06 — aaronjmars/minitor*

Per-deck color labels
Decks in minitor can now be tagged with a color. The chosen color renders as the identity dot in the sidebar header (replacing the brand active/inactive dot) and as a small circular dot next to the deck name in the top bar of whichever deck is open. Operators can pick from 8 preset swatches (orange, green, blue, purple, pink, yellow, cyan, slate) or paste in any 6-digit hex. Same palette and same normalization as the per-column color labels shipped yesterday, so an operator who learned "DeFi = orange" from column tagging can apply the convention at the deck level and the two surfaces stay coherent.

Why this matters:
The per-column UX axis is now well-covered (tab groups → collapse → JSON export → quick-search → pin → duplicate → column color labels — seven rungs over the last two weeks). The next bottleneck — flagged in the Jun-04 repo-actions article — is visual organization at the deck level. At five or more decks per operator, the sidebar's identical-looking deck headers become a scan-time bottleneck; a Markets deck and a Dev deck should look different at a glance, not just by name. Color is the deck-level analog of the per-column work — the same affordance, one level up.

What was built:
- drizzle/0009_deck_color.sql + journal + 0009_snapshot.json: additive nullable text column on decks (no churn on existing rows, no migration risk).
- lib/db/schema.ts + lib/columns/types.ts: Deck.color?: string field with inline doc on sidebar and top-bar rendering.
- app/actions.ts: new updateDeckColor server action that reuses the column-level normalizeColumnColor (so case-folding and shorthand rejection can never drift between deck and column surfaces); exportDeck emits an optional deckColor field; importDeck re-validates through the same normalizer and propagates the persisted color back to the optimistic client store via ImportedDeckResult.deckColor.
- lib/store/use-deck-store.ts: updateDeckColor zustand action mirroring renameDeck's optimistic-then-server pattern; importedDeckPatch carries the color through deck imports.
- components/dialogs/deck-color-dialog.tsx: new dialog with the same 8 preset swatches + Clear button + freeform hex input + live invalid-hex error as the column picker. Save only enables when the value would actually change — opening and closing without touching anything is a no-op.
- components/sidebar-01/nav-decks.tsx: "Set color" / "Change color" menu item between Rename and Version history; tagged-deck dot renders in the operator's color (full opacity active, 65% inactive).
- components/deck/deck-view.tsx: 10px circular dot next to the deck name in the top bar when the active deck has a color.

How it works:
The 6-hex color is server-validated against the same /^#[0-9a-f]{6}$/i regex columns use, lowercased on persist. Old deck exports created before this feature simply omit the deckColor field and import as a deck with color=null — the Zod schema is additive, not a v2 bump. Operator color overrides the active-deck brand color on the sidebar dot: when a deck is tagged, the dot stays in its color even when active, because swapping to the brand color would erase the operator's intent. Inactive tagged decks dip to 65% opacity so the active deck still reads as primary. Renames and color changes deliberately don't snapshot the deck — they're metadata, not structural — version history continues to cover add/remove/reorder/duplicate/import/restore only.

What's next:
Could extend to deck icons (lucide names + emoji) for one more visual axis at the deck level — color and icon together make 5+ decks instantly distinguishable. Could also let starter templates ship pre-colored (the deckColor field is already in DeckTemplatePayload, just no templates use it yet).

PR: https://github.com/aaronjmars/minitor/pull/62
