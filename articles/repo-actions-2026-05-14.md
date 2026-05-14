# Repo Action Ideas — 2026-05-14

**Repos analyzed:** aaronjmars/aeon (313⭐, 50 forks), aaronjmars/aeon-agent (7⭐, 62 skills), aaronjmars/minitor (8⭐, 43 column types)

**Context:** Pipeline was starved after today's `feature` run consumed all May-12 ideas (webhook-bridge + crates.io column). aeon has no pending feature ideas; aeon-agent's May-12 backlog is fully cleared; minitor's registry trifecta (npm + pypi + crates) is complete. This run seeds tomorrow's `feature` with five new implementable ideas.

---

### 1. Product Hunt Launch Skill

**Type:** Content
**Effort:** Small (hours)
**Impact:** aeon has 313⭐, 50 forks, 117 skills, and a strong autonomy narrative — all the ingredients for a successful Product Hunt launch, but nobody's drafted the post. A `product-hunt-launch` skill writes the full launch asset package (tagline, description, first comment, maker comment, feature bullet list) from internal state — no external API needed. Surfaces it via `./notify` so the operator can review and submit. This is the fastest path from "project with traction" to "project with distribution."
**How:**
1. New `skills/product-hunt-launch/SKILL.md` — `workflow_dispatch`, `enabled: false`. Reads `gh api repos/aaronjmars/aeon` for current stats (stars, forks, open_issues), `skills.json` for skill count by category, and the three most recent `articles/repo-article-*.md` files for narrative hooks.
2. Generates five PH assets: tagline (≤60 chars), description (≤260 chars), first comment (the "why we built this" story, ≤500 chars), maker comment (technical differentiation, ≤500 chars), and a 6-item feature bullet list. Hard character limits enforced — PH rejects overlong fields.
3. Writes to `articles/product-hunt-launch-${today}.md`. Sends notification with the tagline + description + a note on what still needs operator action (gallery images, first-hunter outreach).

---

### 2. Skill Enabler

**Type:** Feature
**Effort:** Small (hours)
**Impact:** Four aeon announcement skills (star-milestone, star-momentum-alert, thread-formatter, show-hn-draft) have had all their conditions met since May 12 — 300⭐ crossed, ATH day scored 16+ on thread-formatter's signal table — and are still `enabled: false`. The same finding has appeared in three consecutive repo-articles and two heartbeat escalations. A `skill-enabler` skill closes this mechanically: operator passes `var` as a comma-separated slug list, skill validates each against `skills.json` and `aeon.yml`, patches the `enabled: false` → `enabled: true` lines, commits, and opens a PR. Explicit opt-in via `var` eliminates any ambiguity about which skills get flipped.
**How:**
1. New `skills/skill-enabler/SKILL.md` — `workflow_dispatch`, `enabled: false`. Reads `var` as comma-separated skill slugs. For each slug: verify `skills/` directory exists, verify `aeon.yml` contains `enabled: false` under that skill's entry (reject already-enabled skills with a warning), patch to `enabled: true`.
2. Commit the changed `aeon.yml` on a new `feat/enable-skills-${today}` branch and open a PR listing each enabled skill with a one-line rationale (drawn from MEMORY.md Next Priorities if present).
3. Send `./notify` with a summary: N skills enabled, PR link, reminder that the first cron run will fire on the next scheduled tick.

---

### 3. Fork Skill Gap

**Type:** Community
**Effort:** Medium (1-2 days)
**Impact:** Fork operators currently have no visibility into which upstream skills they haven't adopted. Fork-cohort tracks activation stage; fork-release-tracker tracks versioned releases; fork-skill-gap closes the missing layer — "here's what's in upstream that you don't have." Weekly Sunday run reads each POWER/ACTIVE fork's `skills.json` via `gh api`, diffs against upstream's list, and generates a per-fork gap table. The top 3 forks by gap size get a shout-out in the notification. Creates pull toward upstream adoption without requiring operator action on any fork.
**How:**
1. New `skills/fork-skill-gap/SKILL.md` — weekly Sunday 21:00 UTC (30 min after contributor-spotlight), `enabled: false`, sonnet-4-6. Reads fork-cohort state from `memory/topics/fork-cohort-state.json` to get the POWER+ACTIVE fork list. For each fork, `gh api repos/{fork}/contents/skills.json --jq '.skills | map(.slug)'` to get their skill list. Diff against upstream `skills.json`. Compute: missing count, missing slugs, categories with biggest gaps.
2. Sort forks by missing-skill count descending. Write `articles/fork-skill-gap-${today}.md` with a full table (fork | tier | total skills | missing | top missing slugs). Cap at 20 forks in the article.
3. Notification: top 3 forks by gap size + total gap across the POWER/ACTIVE tier. Link to article. If all POWER forks are within 5 skills of upstream, exit QUIET (no notify).

---

### 4. Column Keyword Alerts

**Type:** Feature
**Effort:** Medium (1-2 days)
**Impact:** Minitor's 43 column types are pure display — they fetch, you read. But the dominant monitoring use case is "tell me when X appears," not "show me everything." Adding an optional `alertKeywords` field to any column config lets the user specify comma-separated terms; when a fetched item matches, it gets a yellow highlight ring and the column header shows a badge count. Purely client-side — no new API, no new data source, works with all existing column types on day one.
**How:**
1. Add `alertKeywords?: string` to `BaseColumnConfig` in `lib/columns/schema.ts`. Parse it client-side in the column item renderer (`lib/columns/ColumnItem.tsx` or equivalent) into an array of lowercase terms; highlight any item whose title or description contains a match using a `ring-2 ring-yellow-400` Tailwind class.
2. Wire badge count into the column header component: count of matched items in the current page, shown as a red badge when > 0. Badge clears when the user clicks "Load more" or refreshes, so it only indicates unread matches in the visible window.
3. Surface `alertKeywords` in the Add/Edit column form as an optional text field with a placeholder like `aeon, anthropic, claude`. No server changes — filter is applied at render time. Write one Playwright/unit test asserting that a column with `alertKeywords="foo"` renders a highlight on a mocked item containing "foo."

---

### 5. Deck Export / Import

**Type:** DX improvement
**Effort:** Small (hours)
**Impact:** Minitor is local-first (PGlite) — which means every new install starts blank. Users have no way to share their "founder dashboard" or "crypto desk" setup. Deck export serializes the current deck's column list (type, config, order) to a JSON blob; import reads that blob and recreates the deck. Enables community sharing: someone posts their deck JSON on Discord or X, anyone can paste it into Minitor and start monitoring in seconds. Zero infrastructure change — purely a server-action pair + two ⌘K commands.
**How:**
1. Add `exportDeck(deckId)` server action: queries the deck's columns from PGlite, serializes to `{ deckName, columns: [{ type, config, order }] }`, returns the JSON string. Wire a "Export deck" command into the ⌘K palette (`lib/cmdk/commands.ts`) that calls this action and copies the result to clipboard with a `sonner` toast confirming "Deck JSON copied."
2. Add `importDeck(json)` server action: parses and validates the JSON (Zod schema matching the export shape), creates a new deck with a `(imported)` suffix on the name, inserts each column in order. Wire an "Import deck" ⌘K command that opens a small modal with a `<textarea>` for pasting the JSON blob.
3. Add a round-trip test: export a deck with 3 columns, import the JSON, assert the imported deck has the same column types and configs.
