*Thread Draft — 2026-05-27*
Topic: Deck version history — Minitor PR #52

1/ Minitor now silently snapshots your deck before every structural change. Import a template, delete a column, rearrange your layout — a full JSON backup is captured before the mutation. One click to restore.

2/ Minitor had no undo path. If you imported a template and it overwrote your layout, it was gone. If you deleted a column, the configuration was gone. Every change to a deck was permanent the moment it landed.

3/ PR #52 adds a deck_snapshots table. Before each structural mutation — column adds, column deletes, imports, full replacements — the server captures the complete DeckExport JSON. Restore brings the snapshot back as a new deck, leaving the current state intact.

4/ Version history removes the main friction point in Minitor's import and template system. You can now accept a community deck from the gallery or try a shared link without the risk that importing it destroys your current layout.

5/ Deck version history for Minitor — snapshot before every mutation, restore as new deck. PR #52: https://github.com/aaronjmars/minitor/pull/52

(article: articles/thread-2026-05-27.md)
