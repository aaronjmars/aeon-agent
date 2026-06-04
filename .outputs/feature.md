*Feature Built — 2026-06-04 — aaronjmars/minitor*

Per-Column Duplicate

Every minitor column now has a "Duplicate" entry in its More-menu dropdown. Click it and a new column appears immediately to the right of the source, inheriting every persisted setting — same plugin, same filter rules, same refresh interval, same alert keywords, same tab group, same webhook. The new column is named "<original> (copy)" and the operator can tweak it from there.

Why this matters:
The common operator move on a 10–15 column deck is "I want two CoinGecko columns, one for BTC and one for ETH" or "two GitHub repo columns, two RSS feeds with different include filters." Before today, that meant adding a brand-new column from scratch and re-entering every config field manually. After today: one click, optionally adjust one or two fields in Configure, done. This is the 6th rung on the per-column UX axis the deck has been building over the last 7 days — tab groups (May 29), collapse (May 30), JSON export (May 31), quick-search (Jun 2), pin-to-front (Jun 3), and now duplicate (Jun 4). Each one answers a different "what am I doing with this column" question; duplicate answers "fork this column to view it twice."

What was built:
- app/actions.ts (+77): New `duplicateColumn(sourceId, newId, newTitle)` server action. Captures a deck snapshot before mutation (reversible from version history), shifts every column with `position > src.position` right by 1, inserts the duplicate at `src.position + 1`. Inherits every persisted field except `pinned`. Returns the `ImportedDeckColumn` shape that `importDeck` already emits — same type round-trip as every other column-create path.
- lib/store/use-deck-store.ts (+69): New `duplicateColumn(columnId)` zustand action. Reads source from state, locates the owning deck by scanning `decks[*].columnIds`, generates a new nanoid id and a title of `"<source> (copy)"` capped at 256 chars (matches the server cap), inserts optimistically right after the source in `columnIds[]` so visual order matches what the server will land. Fires the server action via the same `fireAndLog` pattern every other mutation uses.
- components/column/column-card.tsx (+14): "Duplicate" DropdownMenuItem between Rename and Download. Uses the lucide-react `Copy` icon imported alongside the existing pin/download/settings glyphs. Toast on success names the new column so the operator can spot which row appeared mid-deck.

How it works:
Three deliberate design decisions. (1) Insert after source not at end — appending to a 15-column deck would force the operator to drag-scroll to find their copy, which is the opposite of what a duplicate action is for. The one extra UPDATE is worth it. (2) Inherits `notifyWebhookUrl` — this is an in-install copy not an export, so the secret stays inside the trust boundary it was already configured within (the export path still strips it). (3) Drops `pinned` — pinning is the operator's explicit "this is a primary column" decision; mirroring PR #59's "DnD across pin/unpin no-op — Pin checkbox is the explicit boundary affordance" rule, crossing the pinned boundary always requires explicit operator action. No DB schema change, no migration, no version bump — round-trips through export/import/share-link/snapshot identically to any other column.

What's next:
The per-column UX axis is mature enough that a "bulk duplicate" or "column templates library" (save column config as a reusable template, apply across decks) would be the natural next layer. But the next push will probably go back to deck-level work — deck duplication, or per-deck refresh-all controls.

PR: https://github.com/aaronjmars/minitor/pull/60
