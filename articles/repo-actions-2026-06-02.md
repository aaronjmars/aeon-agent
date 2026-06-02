# Repo Action Ideas — 2026-06-02

*Generated from analysis of aaronjmars/aeon (475⭐, 153 forks, 0 open issues), aaronjmars/aeon-agent, and aaronjmars/minitor.*

---

## Context

**aeon** had a productive morning. PR #322 (Phase 1 capabilities frontmatter for high-blast-radius skills) merged, locking `capabilities:` declarations onto the ~30 most consequential skills in the repo. PR #316 closed the "aeon x atrium" integration. Two ecosystem PRs arrived within 90 seconds of each other — HivemindOS (#320) and EchoOracle (#321) — bringing the ECOSYSTEM.md project count to its highest point yet. HoundFlow's 6 keyless onchain investigation skills (approval-audit, honeypot-check, lp-lock-check, linked-wallets, fund-flow, investigation-report) have now been live for 72 hours with zero downstream consumers. All May-30 ideas fully burned.

**aeon-agent** completed its 19th consecutive same-day-after backport today (follow-up-patrol, PR #76). The upstream-gap skill (PR #72) now surfaces the pending queue every Monday. Three PR #272 skills remain unbackported: narrative-convergence, mcp-pulse, fleet-scorecard. And today's upstream build — pr-merge-queue (aeon PR #318) — is the natural 20th.

**minitor** shipped per-column quick-search (PR #58) as the fourth feature in the per-column UX density axis (tab groups → collapse → JSON export → quick-search). 49 column types now live. The per-column UX axis has been building around view-state features (no DB schema, no migration). The next layer — persistence and sharing improvements — is where the remaining friction lives.

---

### 1. `ecosystem-entrants` skill (aeon)
**Type:** Feature
**Effort:** Small (hours)
**Impact:** Two ecosystem PRs landed today within minutes of each other (HivemindOS #320, EchoOracle #321). Currently `ecosystem-pulse` tracks liveness of projects already in ECOSYSTEM.md, but nothing surfaces new arrivals as a discrete weekly signal. Every new entrant is a potential co-marketing partner, integration target, or community member worth following up with — and at the current contribution velocity they're arriving faster than a human scanning the PR queue would catch. A weekly skill that diffs the git history of `docs/ECOSYSTEM.md` and surfaces newly-added project rows closes that gap.

**How:**
1. New `skills/ecosystem-entrants/SKILL.md` — weekly Monday schedule (e.g. 11:45 UTC, after ecosystem-pulse at 11:00). Use `git log --diff-filter=M --follow --since={7d ago} -- docs/ECOSYSTEM.md --format=%H` to find merge SHAs touching the file in the last 7 days; for each SHA, run `git show {sha}:docs/ECOSYSTEM.md | diff <(git show {sha}^:docs/ECOSYSTEM.md) -` to extract added rows.
2. Parse each new row: project name, URL, description column if present. Write to `memory/topics/ecosystem-entrants-state.json` keyed by project URL so re-runs don't re-notify stale entries.
3. Notify (always, when ≥1 new entrant) — list of new projects with their description and PR link. Silent when no new entries. Article always written for the record.

---

### 2. `wallet-risk-weekly` skill (aeon)
**Type:** Integration
**Effort:** Medium (1-2 days)
**Impact:** HoundFlow's 6 keyless onchain investigation skills (approval-audit, honeypot-check, lp-lock-check, linked-wallets, fund-flow, investigation-report) have been live for 72 hours with zero downstream consumers. The skills exist, the wallet addresses exist (`.x402books/wallets.json`, merged PR #273), and the Base RPC calls are free — the only missing piece is an orchestration layer. A weekly skill that pipes each treasury + deployer wallet through approval-audit + honeypot-check and surfaces a risk summary is the first meaningful consumer of the HoundFlow pack. The `token-report` skill covers price; the `treasury-info` skill (if present) covers ETH balance. Neither covers wallet risk posture — whether the agent's own addresses hold dangerous approvals or exposure to LP honeypots.

**How:**
1. New `skills/wallet-risk-weekly/SKILL.md` — reads `.x402books/wallets.json` to get wallet addresses and roles (treasury / deployer / other). For each Base wallet: inline-execute `skills/approval-audit` logic (or read its SKILL.md and call the same Base RPC endpoints: `eth_call` to ERC20 `allowance(owner, spender)` for known DEX routers). For each token held by the wallet, check honeypot-check patterns via `skills/honeypot-check` logic.
2. Bucket findings by severity: HIGH (active approval to unverified contract / honeypot detected), MEDIUM (large approval to verified contract), LOW (stale approvals). Write weekly article `articles/wallet-risk-{today}.md`.
3. Notify always when HIGH findings present; silent (article only) when LOW/MEDIUM or CLEAR. State written to `memory/topics/wallet-risk-state.json` for WoW delta on approval counts.

---

### 3. `pr-merge-queue` backport (aeon-agent)
**Type:** DX
**Effort:** Small (hours)
**Impact:** Upstream aeon PR #318 (pr-merge-queue, merged 2026-06-02) is the natural 20th consecutive same-day-after backport. The skill provides a daily 09:45 UTC operator-facing digest of every open PR on aaronjmars/aeon-agent, bucketed by touched-file risk tier — CORE_REVIEW (touches aeon.yml / CLAUDE.md / core scripts) > INFRA_REVIEW (.github/workflows) > SKILL_WARN_OR_BLOCK > SKILL_PASS > FAST_TRACK > UNKNOWN. Currently aeon-agent has pr-triage and pr-skill-triage but no skill that surveys the full open queue and surfaces the safest merge candidates first. As external contributor PRs increase (follow-up-patrol, the new ecosystem skills), the merge decision layer will matter more.

**How:**
1. Verbatim copy of `skills/pr-merge-queue/SKILL.md` from upstream aeon with a backport-note block at top citing PR #318.
2. Two adaptations: (a) all `aaronjmars/aeon` → `aaronjmars/aeon-agent` in `gh api` paths and PR URL templates; (b) `./notify` call rewritten as inline heredoc passed as `$1` (aeon-agent's single-positional-arg style, confirmed at root `notify` line 3 `MSG="$1"`).
3. Register in aeon.yml at schedule `45 9 * * *` between pr-tracker and repo-revive. Add to skills.json (total 97→98, category dev).

---

### 4. Column pinning to top (minitor)
**Type:** Feature
**Effort:** Small (hours)
**Impact:** Operators running 10–15 column decks frequently have 2–3 "always visible" columns (e.g. their main token price, primary GitHub repo, primary news feed) that they need at the start of the column grid regardless of topic. The DnD reorder (existing) fixes position only for that session — a page reload restores the DB-saved order. A per-column "pin to first" toggle that writes a `pinned: boolean` to the DB keeps priority columns at the left edge permanently. Pairs with tab groups (which filter columns by group) and collapse (which folds secondary columns to 48px strips) as the third layer of the deck-density axis: tab = "which group", collapse = "how prominent", pin = "always visible regardless of active tab".

**How:**
1. New migration `drizzle/0007_column_pinned.sql` — additive nullable `pinned` boolean column on `columns` table (DEFAULT false). Add `pinned?: boolean` to `lib/columns/types.ts` Column shape and `lib/db/schema.ts`.
2. New `updateColumnPinned` server action in `app/actions.ts` (boolean toggle, same pattern as updateColumnTabGroup / updateColumnRefreshInterval). Pin toggle added to the Configure Column dialog (`components/column/configure-column-dialog.tsx`) — a "Pin to front" checkbox near the top of the form.
3. In `components/deck/deck-board.tsx`, sort visible columns so `pinned === true` columns always appear first (stable sort preserves relative order within pinned and unpinned groups). Pinned columns show a small pin icon badge in the header (lucide `Pin`, same pattern as the refresh interval `Clock` badge). Export/import/share-link round-trips the field backward-compatibly.

---

### 5. `skill-health-digest` skill (aeon)
**Type:** Feature
**Effort:** Medium (1-2 days)
**Impact:** `operator-scorecard` gives a composite health verdict (HEALTHY / DEGRADED / CRITICAL) but doesn't name which specific skills are quietly failing. The issue tracker (`memory/issues/`) captures filed issues but requires a human to notice degradation first. `memory/cron-state.json` carries per-skill `consecutive_failures`, `success_rate`, `last_status`, and `last_run` for every skill that has run — the data for a per-skill health ranking already exists and is just unread. A weekly skill that reads cron-state.json and surfaces RED / YELLOW / GREEN buckets gives the operator a 30-second scan to catch silent degradation before it warrants filing an issue. Complements operator-scorecard (aggregate) and the issue tracker (reactive) with a proactive per-skill weekly signal.

**How:**
1. New `skills/skill-health-digest/SKILL.md` — reads `memory/cron-state.json`. For each skill entry: compute `consecutive_failures` (if ≥3 → RED), `success_rate` (if <80% over lifetime → YELLOW), otherwise GREEN. Sort RED entries by consecutive_failures desc, YELLOW by success_rate asc.
2. Write `articles/skill-health-{today}.md` — markdown table with three sections (RED / YELLOW / GREEN), each row: skill name, last_status, consecutive_failures, success_rate (%), last_run date. Add a "no RED entries" short-circuit note when healthy.
3. Notify only when RED bucket is non-empty (≥1 skill with consecutive_failures ≥3). Silent + article-only when all YELLOW/GREEN. Write state to `memory/topics/skill-health-state.json` for WoW delta (track when a skill moves tier so the notification calls out "newly degraded" vs "ongoing" entries).
