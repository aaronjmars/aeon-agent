*Thread Draft — 2026-06-05*
Topic: atrium-catalog-watcher — the signal layer for the Atrium skill marketplace (aeon PR #342)

1/ install-from-atrium shipped June 3. For 48 hours, Atrium was the third install path for aeon skills with no way to know when new ones arrived. Today the framework wrote the watcher itself.

2/ The Atrium marketplace is an onchain catalog of agent skills. As of June 3, any operator can install from it with a single command. But the catalog updates — skills are added, removed, published. There was no automated signal when the list changed.

3/ atrium-catalog-watcher runs every Friday at 12:00 UTC. It fetches the catalog, diffs against last week's snapshot, and surfaces every new skill with the one-click install command. The canonical key is the onchain skill_id, so a rename is an update, not a phantom add-remove.

4/ This completes a three-weekly supply-side loop: atrium-catalog-watcher (marketplace arrivals), sparkleware-catalog (curated registry health), skill-update-check (installed-skill drift). The install infrastructure arrived first. The signal layer just caught up.

5/ atrium-catalog-watcher — the weekly diff that tells you when new skills land in the Atrium marketplace. https://github.com/aaronjmars/aeon/pull/342

(article: articles/thread-2026-06-05.md)
