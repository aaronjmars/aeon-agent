*Feature Built — 2026-06-02 — aaronjmars/minitor*

Per-Column Quick Search
Every column in minitor now has a built-in search bar. Click the new search icon in the column header, an input row drops beneath the header, and typing instantly narrows the visible items to substring matches. Esc clears and closes the input; the small × button clears in place. Pairs with tab groups (May 29) and column collapse (May 30) on the same UX axis — those decide which columns you see and how big; this decides what you're looking at inside each one.

Why this matters:
Minitor now ships 47+ column types and operators frequently keep deep-scrolling columns open — Hacker News, github-issues, github-discussions, npm/pypi/crates, polymarket, DeFiLlama TVL, etc. The existing include / exclude keyword filters (PR #51) are persistent column config: they survive reloads, travel with deck exports, fire webhooks on new matches. They are the right answer for "always keep this column tuned to X." They are the wrong shape for "I have 200 items in this column and I'm looking for the one mentioning postgres." That second case wants an ephemeral, view-only narrowing — the operator doesn't want to reconfigure the column, just find something in the current items. Quick-search is that view; until today the only path was Ctrl-F in the browser, which scrolls the entire deck and doesn't isolate one column.

What was built:
- lib/store/use-deck-store.ts: new searchByColumn record (NOT persisted — same lifetime as autoFetchingIds, selectedTabByDeck, collapsedColumnIds), setColumnSearch action with trim + 256-char cap + empty-string-deletes, cleanup hooks on deleteColumn and deleteDeck.
- lib/columns/keyword-match.ts: new itemMatchesSearchQuery helper, single literal substring (not a parsed keyword list — typing "rust foo" means the phrase, not OR-split terms), scans the same content + author + url haystack the alert-keyword highlighter uses.
- components/column/column-card.tsx: renamed the visibleItems flow into two stages (filteredItems after include/exclude, visibleItems after search). Search button in the header, input row below, auto-focus on open, Esc handler, SearchEmptyState rendered when search active and zero matches with a one-click clear button. Collapsed strip gets a small emerald Search icon when a search is active on that column — prevents the silent-undercount surprise where the alert badge would shrink under a hidden filter.

How it works:
Search runs AFTER include/exclude filters in the visible-items pipeline, so it narrows what's already filtered — never widens past what the persisted rules allow. An operator with `exclude: spam` set on a column who then searches for `discount` still won't see spam-with-the-word-discount; the persistent config wins. The implementation reuses the exact same haystack (content + author name + author handle + url) that itemMatchesAlertKeywords scans, so search rules are identical to the alert-highlight rules operators already know. The query lives entirely in zustand view-state — it doesn't survive a page reload, it doesn't export with the deck (the JSON export schema is unchanged), it doesn't fire webhooks. A useEffect auto-opens the search row when a column re-renders with a non-empty query already in store, so a cross-tab or cross-collapse round-trip preserves the search bar's visibility.

What's next:
Could add per-deck search (one query, all columns) if operators ask. CSV export was deliberately out of scope of PR #56 and remains so — could grow once a specific plugin has a concrete tabular use case. Next minitor PR slot is open.

PR: https://github.com/aaronjmars/minitor/pull/58
