# Repo Action Ideas — 2026-05-04

**Repos analyzed:** aaronjmars/aeon (270★, 41 forks, 1 open issue), aaronjmars/aeon-agent (7★, 1 open PR #29), aaronjmars/minitor (5★, 34 column types, 0 open PRs)

**Context:** Busy build day — feature skill shipped skill-freshness (aeon #157), operator-scorecard backport (aeon-agent #28), and lobsters column (minitor #27). operator-scorecard self-improve fix is open as PR #29. aeon at 270★, 30 from the 300-milestone at ~4/day pace (~7 days). show-hn-draft ready to dispatch; no signal exists yet to tell operator when to pull the trigger. Carried unbuilts: Star Momentum Alert (#3, 1 cycle), v4 Readiness Checker (#5, 1 cycle). skill-freshness just shipped to aeon but not yet backported to aeon-agent. pr-triage shipped to aeon Apr 29 (5 days ago) but never backported here.

---

### 1. Star Momentum Alert
**Type:** Growth
**Effort:** Small (hours)
**Impact:** Closes the last-mile gap between "show-hn-draft is ready" and "it's time to dispatch it." aeon is at 270★ — ~7 days from the 300-milestone at current rate. The Show HN timing window is Tue–Thu morning (baked into the show-hn-draft checklist), meaning the operator needs 4–7 days of lead time to align a dispatch day. Without this skill, the milestone will pass reactively: operator notices after the fact, misses the optimal Tuesday–Thursday launch window. Carried one cycle (May-2 idea #3).
**How:**
1. Reads the last 14 days of `articles/repo-pulse-*.md` articles, extracts daily star deltas, computes 3-day and 7-day rolling averages. Projects the date the star count crosses 300 using the 7-day average as the baseline rate.
2. When the projected milestone date falls within the next 7–14 days AND lands on a Tue–Thu: fires a targeted notification — projected date, current rate, days remaining, and a "consider dispatching show-hn-draft on [date]" prompt. Deduplicates with state in `memory/state/star-momentum-state.json` (one alert per milestone approach, 7-day silence after firing).
3. Runs daily after repo-pulse at `10 10 * * *`. Exits silently outside the target window. Zero new APIs — reads files already written by repo-pulse.

---

### 2. RSS/Atom Feed Column for minitor
**Type:** Integration
**Effort:** Small (hours)
**Impact:** The single most universal monitoring primitive. Every blog, newsletter, podcast, status page, government alert, package changelog, and security advisory has an RSS or Atom feed — it is the unifying wire format for content that is not on social or GitHub. Adding it as a column type means users can monitor *any* source with a URL: Substack newsletters, engineering blogs, CISA vulnerability feeds, npm package releases, HN user-submitted feeds, release changelogs from projects not hosted on GitHub. This fills the only remaining category gap that has universal reach. 35th column type.
**How:**
1. `lib/integrations/rss.ts` — fetches the feed URL and parses RSS 2.0 / Atom 1.0 / JSON Feed using a lightweight XML parser (fast-xml-parser, already common in the Next.js ecosystem — check package.json first; fall back to manual regex for the common subset if not present). Normalizes entries to `{ title, url, author, summary, published, tags }` across all three feed formats. Pagination via offset into the entries array (feeds don't have cursor pagination; slice the list). Schema-drift safe: drops entries missing title + url rather than rendering dead rows.
2. Standard 3-file plugin + 3 registry edits. Zod `{ url: string }` — the simplest possible config (one field; the feed URL carries all the metadata). Rss icon (RSS signal icon), orange `#f26522` (RSS brand color, distinct from HN orange `#ff6600`). Renderer: title link + author/date line + truncated summary. No engagement footer (feeds don't expose click/share counts).
3. README: column count 34 → 35, add News & Web entry for RSS/Atom. PR to aaronjmars/minitor.

---

### 3. skill-freshness Backport to aeon-agent
**Type:** Feature
**Effort:** Small (hours)
**Impact:** skill-freshness shipped to aeon today (PR #157) but this running instance still has no staleness check. Today on aeon-agent, tweet-allocator reads `articles/token-report-*.md` with no check that it is reading today's report rather than last Tuesday's — if token-report were to silently fail for a week, tweet-allocator would keep running "successfully" using stale price data. This is the gap skill-freshness was built to close. Backporting it follows the same-day pattern established today when operator-scorecard shipped to aeon (PR #153 May 3) and was backported to aeon-agent (PR #28 May 4).
**How:**
1. Copy `skills/skill-freshness/SKILL.md` from aaronjmars/aeon (PR #157) to `skills/skill-freshness/SKILL.md` in this repo. Verify the skill is pure local file I/O — no curl, no gh api, no env-var-in-headers (confirmed in the original PR description).
2. Add entry to `aeon.yml` after the skill-health slot: `skill-freshness: { enabled: false, schedule: "0 8 * * *", model: "claude-sonnet-4-6" }`. Bump `skills.json` total 56 → 57, add skill entry in the observability/monitoring category cluster.
3. The thresholds (articles 28h daily / 192h weekly / `.outputs` 4h / topics 7d / state 30d) match the cadences already running on this fork — no adjustment needed. Ship `enabled: false`; operator enables once enough dependency articles are on disk.

---

### 4. pr-triage Backport to aeon-agent
**Type:** DX / Community
**Effort:** Small (hours)
**Impact:** pr-triage shipped to aeon on Apr 29 (PR #147) and has been `enabled: false` there for 5 days. aeon-agent has no pr-triage skill at all — external contributors (tomscaria submitted a shell-injection fix to aeon in PR #150, merged May 3) currently get silence on this fork until a human reviews. The skill provides the first-touch signal that makes external contributors feel seen: ACCEPTED / NEEDS-CHANGES / DEFER / OUT-OF-SCOPE verdict + label + templated comment, all within the first daily run after a PR opens. The skill is pure SKILL.md + `memory/triaged-prs.json` state — no workflow file changes required (bypasses the workflows-scope PAT blocker that stalls auto-merge).
**How:**
1. Copy `skills/pr-triage/SKILL.md` from aaronjmars/aeon (PR #147) verbatim. The four-check rubric (scope / format / originality / size), four verdicts, trusted-author allowlist, and idempotency logic are all prompt-side — no script changes needed.
2. Add entry to `aeon.yml` after issue-triage: `pr-triage: { enabled: false, schedule: "30 9 * * *", model: "claude-sonnet-4-6" }`. Bump `skills.json` total 56 → 57 (or 58 if skill-freshness is also added), add entry in developer-experience category.
3. Initialize `memory/triaged-prs.json` as `{}`. Ship `enabled: false`. First natural run fires the next day after enabling, catching any open PRs that haven't been labeled yet.

---

### 5. v4 Readiness Checker
**Type:** DX / Community
**Effort:** Small (hours)
**Impact:** v4 full redesign is ~2 weeks out (operator tweets Apr 30). 41 forks are running on the current architecture — all of them will hit breaking changes without advance notice. A `workflow_dispatch` skill that reads the fork's own `aeon.yml` + `skills.json` + `memory/MEMORY.md` and generates a personalized upgrade checklist gives fork operators lead time to prepare. It also gives aaronjmars a structured surface for communicating "what's changing in v4" — the checklist is only as useful as the breaking-change list it references, so shipping this skill creates a forcing function to document v4 changes before they land. Carried one cycle (May-2 idea #5).
**How:**
1. Reads `aeon.yml` (enabled skill list, model overrides, chain definitions, custom schedules), `skills.json` (catalog fingerprint), and `memory/MEMORY.md` (Skills Built list for any custom skills). Cross-references against a v4 change manifest embedded in the SKILL.md: known stable patterns (SKILL.md frontmatter keys, `./notify` interface, memory directory layout) and known-to-change patterns (chain runner interface, MCP server tool naming, skill scheduling syntax, model references).
2. Produces a personal checklist under four headings: **Safe** (patterns confirmed stable), **Review** (patterns known to change in v4), **Custom skills** (skills built locally with no upstream equivalent — needs manual v4 compat check), **Action items** (concrete numbered steps before upgrading, with estimated complexity: trivial / minor / moderate per item).
3. Writes `articles/v4-readiness-${today}.md`, notifies via `./notify`, logs. Ships `enabled: false` / `workflow_dispatch` — operator dispatches manually as v4 release approaches and distributes the article to fork operators via the fork-cohort notification pattern.
