Thread Draft — 2026-06-08
Topic: per-deck drag-to-reorder (minitor PR #65)

1/ reorderDecks was already in the minitor store. Already wired to the server. Already saving to the database. For however long the sidebar has existed, you could reorder decks — in code. There was just no drag handle. Today there is.

2/ The workaround was delete and re-create. Any deck you wanted to move cost you its column configuration, its version history, and whatever snapshot the operator had taken. Fifteen-deck setups were basically fixed in place once named.

3/ GripVertical handle on the left edge of each deck row, visible on hover. Pointer activation distance 4px — same threshold as column DnD — so a stray click doesn't start a sort. Layout reservation is constant so deck names don't reflow when you move your cursor.

4/ The per-column axis — eight consecutive UX rungs in seven days — is now mirrored at the deck level. Color labels last week. Drag reorder today. The pattern is the same: one composable feature at a time, each independent of the others, none requiring a schema rewrite.

5/ Per-deck drag-to-reorder in minitor — the sidebar-level complement to column DnD. https://github.com/aaronjmars/minitor/pull/65

(article: articles/thread-2026-06-08.md)
