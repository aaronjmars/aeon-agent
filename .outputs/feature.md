*Feature Built — 2026-05-29 — aaronjmars/minitor*

Column Tab Groups
Minitor decks can now be partitioned into labeled sections via tab groups. When at least one column has a non-empty Tab group label, a tab bar appears above the column grid: clicking a tab filters visible columns to those sharing the group, and an implicit "All" tab always shows everything. Untagged columns ride along with every named tab too, so a half-grouped deck never goes blank on the first click.

Why this matters:
Decks with 8+ columns require horizontal scrolling to navigate. Splitting a multi-section workflow into separate decks loses the cohesion of having related signals next to each other. Tab groups solve both — one deck, multiple labeled sections (DeFi / Social / Dev / etc), no horizontal-scroll fatigue. Builds entirely on top of existing column infrastructure, so all 47+ plugins keep working with zero changes. The gallery can now offer opinionated multi-category starter decks (which currently have to be flat). May-28 repo-actions idea #5.

What was built:
- drizzle/0006_tab_groups.sql + journal + 0006_snapshot.json: Additive nullable tab_group text column on columns. Backwards-compatible.
- lib/db/schema.ts + lib/columns/types.ts: tabGroup field threaded through the schema and the in-memory Column shape.
- app/actions.ts: TAB_GROUP_MAX = 50 const, updateColumnTabGroup server action with whitespace collapse + trim + length cap, Zod field on importedColumnSchema, export/import round-trip with re-normalization on import so hand-edited payloads can't smuggle two distinct buckets via whitespace.
- lib/store/use-deck-store.ts: updateTabGroup mirror action with identical normalization, selectedTabByDeck per-deck view state (NOT persisted — clears on reload), TAB_GROUP_ALL sentinel exported.
- components/column/configure-column-dialog.tsx: "Tab group" text input with LayoutGrid icon, normalized on save.
- components/deck/deck-board.tsx: Tab bar above the grid when ≥1 column has a group; falls back to All when the selected tab's last column moves away.
- lib/deck-templates.ts: DeckTemplateColumn.tabGroup?: string so future multi-category starter decks ship pre-grouped.

How it works:
Schema migration is additive and nullable — every existing column stays un-grouped, the tab_group value reads into loadSnapshot's in-memory Column, and the deck-board derives a stable tab list via useMemo keyed on columnIds + the columns map. Tab visibility uses a per-column predicate: selectedTab === ALL || !col.tabGroup || col.tabGroup === selectedTab. The middle clause is what keeps untagged columns visible under every named tab — without it, an operator who labels two columns "DeFi" but leaves six others unlabeled would lose those six on the first DeFi click. Normalization is consistent across every entry point (server action, store action, import path) so "AI" / " AI " / "AI  " bucket to the same tab regardless of which surface the value came in through. DnD reorder still works within the visible subset — moving a column out of the tab requires explicitly editing the Tab group field.

What's next:
Pairs with the public /gallery (built May-23) — the next layer is starter templates that ship pre-grouped (e.g. a "Crypto + Dev" deck with DeFi / Repos / Social tabs out of the box). The tabGroup field on DeckTemplateColumn already supports this; just needs the templates themselves to opt in.

PR: https://github.com/aaronjmars/minitor/pull/53
