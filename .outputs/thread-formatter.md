*Thread Draft — 2026-06-06*
Topic: per-deck color labels — visual organization at the deck level (minitor PR #62)

1/ Minitor shipped per-column color labels yesterday. Today it shipped per-deck color labels. Same 8 swatches, same hex normalizer, same server-side format enforcement. Visual organization is now a coherent system across both levels.

2/ A minitor deck running 15 columns has a visual scan problem. Operators mentally group columns — DeFi vs dev vs news vs social — but the UI had no in-app marker for it. You knew what your columns were; the UI just showed them all the same way.

3/ Per-deck color labels give each deck a 6-hex dot that appears in the sidebar and in the deck header. When a deck is active, the dot holds its operator-assigned color — not the brand accent. Inactive tagged decks drop to 65% opacity so the active deck still reads as primary.

4/ Eight consecutive UX features on minitor in nine days — tab groups, collapse, JSON export, quick-search, pin, duplicate, column colors, deck colors. Each is independent of the others. Each composes with the others. None required a DB schema rewrite.

5/ Per-deck color labels — the deck-level visual system that keeps columns, decks, and exports coherent. https://github.com/aaronjmars/minitor/pull/62

(article: articles/thread-2026-06-06.md)
