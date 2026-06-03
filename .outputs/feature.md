*Feature Built — 2026-06-03 — aaronjmars/minitor*

Pin column to front
Minitor columns now have a "Pin to front" toggle. When pinned, a column always renders at the left edge of the deck regardless of how the columns were dragged into order, regardless of the active tab group, and across page reloads — pinning is DB-backed, not view-state. The expanded column header shows a small brand-coloured Pin badge, and the collapsed strip keeps the pin marker so a folded pinned column doesn't lose its visual priority. Toggle is in the Configure dialog as a checkbox.

Why this matters:
Operators running 10–15 column decks frequently have 2–3 "always visible" priority columns — their main token price, primary GitHub repo, primary news feed — that need to stay at the left edge regardless of topic. The existing DnD reorder fixes column position only for that session: a page reload restores the DB-saved order. Pinning makes priority columns sticky. Combined with tab groups (PR #53) and column collapse (PR #55), it completes the deck-density axis: tabs decide "which columns am I looking at"; pin decides "always visible regardless of active tab"; collapse decides "how prominent within the visible set".

What was built:
- drizzle/0007_column_pinned.sql + meta/_journal.json + meta/0007_snapshot.json: additive `pinned` boolean column on `columns` (DEFAULT false NOT NULL — existing rows backfill safely).
- lib/db/schema.ts + lib/columns/types.ts: schema field + Column shape with inline doc on the sort-order interaction.
- app/actions.ts: new `updateColumnPinned` server action; loadSnapshot mapping; Zod schema; importDeck coerces to a hard `=== true` so a hand-edited payload can't smuggle a truthy non-boolean; exportDeck emits the field only for pinned columns.
- lib/store/use-deck-store.ts: `updatePinned` action mirroring server normalization; importedDeckPatch round-trip.
- components/column/configure-column-dialog.tsx: Pin to front checkbox in a labeled card.
- components/deck/deck-board.tsx: stable two-pass partition in `visibleColumnIds` so pinned columns render first while DnD order within each group is preserved.
- components/column/column-card.tsx: Pin badge in expanded header and brand-coloured Pin icon in the collapsed-strip indicator stack.
- lib/deck-templates.ts: DeckTemplateColumn carries the field too so starter templates can ship pre-pinned.

How it works:
The deck-board sort is a two-pass partition (`[...pinned, ...unpinned]`) — Array.prototype.sort would also work, but a two-pass partition reads exactly as intended and is obviously O(n). DnD across the pin/unpin boundary is intentionally a no-op: the Pin checkbox is the explicit affordance for crossing the boundary, and auto-flipping the pinned flag on a drag would be confusing (either too eager or silently relocating the column). Pinned status is independent of tab group — a pinned column in tab "DeFi" still appears on every tab because pinning trumps grouping. Round-trip through export / import / share-link / version-history-snapshot all preserve the field.

What's next:
The deck-density axis (tabs / pin / collapse / search / JSON export) is the persistent UI work. Next-layer ideas in the backlog: pinning could later interact with a column-grouping or "primary deck" surface, but the persistence-and-sharing improvements are the natural follow-up.

PR: https://github.com/aaronjmars/minitor/pull/59
