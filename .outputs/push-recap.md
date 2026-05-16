*Push Recap — 2026-05-16*
3 substantive commits, 1 per repo — all three close in-flight work rather than open new threads.

*Fork-intel quartet completes* (aeon PR #176): fork-skill-gap shipped — Sunday 21:00 UTC per-fork digest of unenabled upstream skills. Composes with fork-cohort state when fresh, falls back to live API otherwise. Article body includes inverse view (top-10 universally unadopted upstream slugs by fork-count) so upstream sees which shipments launch into silence. Closes the layer started May 9–12 (cohort/release/spotlight).

*Self-improve fixes a 5-day false-positive in its own daily report* (aeon-agent PR #48): token-report had been emitting "XAI_API_KEY not set" daily May 13–16 because curl can't expand $XAI_API_KEY in sandbox headers. Step 5 rewritten to read social signal from the most recent fetch-tweets log (today→yesterday fallback); section omitted entirely when no log exists. Third skill this week to convert silent sandbox failure into an explicit marker — pattern is congealing into a contract.

*First user-customizable signal layer in minitor* (PR #41): optional alertKeywords on every column, yellow ring on matched rows + Bell badge in header. Lives as column property (sibling to title), never sent to server fetchers, so all 43 plugins get the feature with zero plugin code changes. Wide match scope (author/handle/content/url), 16-term cap, 64-char-per-term cap, 512-char input clamp. Deck export/import round-trips with backward compat.

Key changes:
- aeon: skills/fork-skill-gap/SKILL.md (+304 new), skills.json 118→119, aeon.yml registry slot
- aeon-agent: skills/token-report/SKILL.md step 5+6 rewritten — no more "XAI_API_KEY not set" lie
- minitor: 10 files, additive migration 0001_alert_keywords (nullable text column), keyword-match.ts core, Bell-badge UI

Stats: ~15 files changed, +806/-21 lines across 3 author PRs
May-14 ideas fully consumed (5/5 shipped May-15–16).
Full recap: articles/push-recap-2026-05-16.md (in aeon-agent)
