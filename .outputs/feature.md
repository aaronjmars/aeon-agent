*Feature Built — 2026-05-30 — aaronjmars/minitor*

Per-Column Collapse To A 48px Strip
Any column in a Minitor deck can now be folded down to a narrow 48-pixel vertical strip showing just the type icon, a rotated title, and small activity indicators — clicking the strip anywhere expands it back to the full 360px column. The collapse toggle is a chevron in the column header next to the refresh and options buttons. Auto-refresh and alert-keyword matching keep running in the background while a column is collapsed, so a column quietly accumulating matches isn't invisible — the yellow match-count badge surfaces on the strip the moment a fetch lands.

Why this matters:
Yesterday's tab-groups feature (PR #53) partitioned big decks into named sections so 8+ column decks stay navigable. But inside a single tab, operators often have two focus columns plus a handful of reference columns they want to glance at, not stare at. With collapse those reference columns reduce to thin strips that take 1/7 the horizontal space — letting an operator keep four columns visible where two used to fit, without the tradeoff of switching tabs or hiding columns. Tabs and collapse are the natural pair on the deck-density axis: tabs decide "which columns am I looking at right now"; collapse decides "which of these are primary vs secondary right now."

What was built:
- lib/store/use-deck-store.ts: new collapsedColumnIds Set<string> state (in-session only, NOT persisted — every deck opens with all columns expanded on a fresh page load, matching the autoFetchingIds and selectedTabByDeck precedent). New toggleColumnCollapsed action. removeColumn and deleteDeck now scrub deleted column ids from the set so it can't accumulate stale entries over a long-lived session.
- components/column/column-card.tsx: ChevronLeft and ChevronRight imports from lucide-react. Reads isCollapsed + toggleColumnCollapsed from the store. New collapsed-strip render: 48px wide card with brand accent line, type icon, rotated title (-rotate-90 with fixed 200px inline width so truncation works in inline space), refresh spinner when fetching, alert-match-count badge when matched, ChevronRight expand affordance. dnd-kit attributes spread onto the strip so dragging to reorder still works — the 4px activation threshold separates a click from a drag. Expanded-view header gets a new Collapse tooltip-button between Refresh and the More-options dropdown.

How it works:
collapsedColumnIds is a plain Set in zustand state, mirroring the existing autoFetchingIds shape the store already uses for transient view state. The toggle action does a copy-on-write new Set so React picks up the change. When the column's id is in the set, ColumnCard short-circuits to the strip render before the regular header + items layout. Auto-refresh, alert-keyword matching, and include/exclude filtering all keep running while collapsed — only the items list and the Configure/Rename/Delete dialogs are hidden. The moment the operator expands, they see live state with no re-fetch needed. No DB schema change, no migration, no plugin contract touched — purely UI + zustand. Decks export, import, and share-link fragments all continue to work unchanged because the collapsed state never leaves the browser session.

What's next:
The strip could also surface an unread-item count (delta since last expand) so it becomes a more general "what's happening here" indicator. A deck-level "collapse all / expand all" command would compose well with tab groups for operators who want a one-click switch between scan-mode and focus-mode.

PR: https://github.com/aaronjmars/minitor/pull/55
