# Push Recap — 2026-05-01

## Overview
Two substantive commits on `aaronjmars/aeon` from aaronjmars: the new `smithery-manifest` skill ships (closing the longest-carried 6-week growth unbuilt — Apr-22 repo-actions idea #1), and a one-line README cleanup removes the agent-status badge added Apr 24. `aaronjmars/aeon-agent` saw zero human commits in the window — only the 25 routine bot auto-commits from cron skill runs (token-report, fetch-tweets, tweet-allocator, repo-pulse, push-recap, repo-article, project-lens, heartbeat, feature, plus scheduler state churn).

**Stats:** 7 files changed, +906 / -3 lines across 2 substantive commits (skill + README). 25 additional bot auto-commits on aeon-agent are routine skill-output side effects, not counted.

---

## aaronjmars/aeon

### Smithery + MCP Registry Submission Pipeline (the headline ship)
**Summary:** A new weekly skill auto-generates the three submission artifacts needed to list `aeon-mcp` on Smithery.ai and the Model Context Protocol Registry. The skill exists because `mcp-server/` has been live since Apr 21 (integration-examples ship) but Aeon was still not listed on either registry — the actual blocker was that nobody had written the manifest, deployment config, and submission body. This skill writes all three from `skills.json` + `mcp-server/package.json` + `README.md`, removing every text-authoring obstacle between "Aeon has an MCP server" and "Aeon is discoverable from inside Claude Desktop's Smithery picker."

**Commits:**
- `50eec0e` — feat: add smithery-manifest skill + initial Smithery / MCP Registry submission docs (#149)
  - New file `skills/smithery-manifest/SKILL.md` (+281 lines) — weekly Monday 06:00 UTC sonnet skill. Reads `skills.json` + `aeon.yml` + `mcp-server/package.json` + `README.md`, regenerates the three artifacts, byte-equality diff vs disk before notify (no-op silent re-run on stable input), exits taxonomy `OK | NO_INPUT | NO_CHANGE`.
  - New file `docs/smithery-manifest.json` (+420 lines) — `server.json` document compatible with the MCP Registry schema (`https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json`). Reverse-DNS name `io.github.aaronjmars/aeon-mcp` per registry convention. Full 95-tool catalog under `_meta.io.github.aaronjmars/aeon`, sorted alphabetically by name so diffs only churn when skills are added/removed/described. Tool naming `aeon-<slug>` matches `mcp-server/src/index.ts:skillToToolName()` 1:1.
  - New file `docs/smithery.yaml` (+29 lines) — Smithery deployment config. `startCommand: stdio` + `commandFunction` returning `{ command: 'node', args: [(config.repoPath || '.') + '/mcp-server/dist/index.js'], env: process.env }`. `configSchema` accepts a `repoPath` string (default empty) so listings without an explicit path still work — server walks up from the installed package.
  - New file `docs/smithery-submission.md` (+160 lines) — paste-ready submission body with field values, short/long descriptions, full 95-tool table, and macOS/Linux/Windows Claude Desktop install instructions.
  - Modified `skills.json` (+14, -2) — `total: 93 → 95`, `generated: 2026-04-18 → 2026-05-01`, new entry for `smithery-manifest` (productivity, weekly cron `0 6 1/7 * *`). The +2 (not +1) reflects an already-present-but-uncounted catch-up alongside the new skill.
  - Modified `aeon.yml` (+1) — registers `smithery-manifest: { enabled: false, schedule: "0 6 1/7 * *", model: "claude-sonnet-4-6" }` in the meta block. Shipped `enabled: false` because the initial generation has already been committed; the cron only matters once skills.json starts drifting.

**Impact:** This closes Apr-22 repo-actions idea #1, which has been the highest-priority growth unbuilt for six straight cycles (also Apr-24/26/28/30 carry-overs). The maintainer can now paste `docs/smithery.yaml` into [smithery.ai/server/new](https://smithery.ai/server/new) and open a PR at `modelcontextprotocol/registry` adding `servers/io.github.aaronjmars/aeon-mcp.json` from `docs/smithery-manifest.json`. Two manual prerequisites remain — publishing `aeon-mcp` to npm (the manifest's `packages[0].identifier` points at an unpublished name) and the listing PR/form submission itself — but the writing work is done. After this, every fork that adds a new skill triggers the cron, regenerates the manifest, and either ships a no-op or surfaces the diff for review.

### Visual Cleanup
**Summary:** Single-line removal of the agent-status badge from the README header. The badge (added Apr 24 alongside the public-status-page heartbeat ship) pointed at `aaronjmars.github.io/aeon/status/` — likely a deliberate trim of the badge row, not a status-page rollback (the status page itself still ships and the heartbeat skill that regenerates it remains intact in the Apr 28 token-pulse extension).

**Commits:**
- `c95478c` — Remove agent status badge from README
  - Modified `README.md` (-1) — drops the `<a href="https://aaronjmars.github.io/aeon/status/">` line and its shields.io badge from the centered `<p align="center">` block. Forks badge, X follow badge, and Bankr badge stay; no other content changed.

**Impact:** Cosmetic. The status page itself is still live and still regenerated by `heartbeat` every 3rd run — only the discoverability surface in the README header is reduced. Worth noting for fork operators who copied the badge row from upstream: a sync that pulls README will drop the badge for them too.

---

## aaronjmars/aeon-agent

No substantive human commits in the 24h window. All 25 commits are routine bot auto-commits from cron skill runs:

| Cluster | Count | Example commits |
|---------|-------|-----------------|
| Scheduler state churn | 6 | `chore(scheduler): update cron state` |
| Skill cron-success markers | 9 | `chore(cron): {skill} success` for token-report, fetch-tweets, tweet-allocator, repo-pulse, feature, push-recap, repo-article, project-lens, heartbeat |
| Skill auto-commits (memory/log/dashboard side effects) | 9 | `chore({skill}): auto-commit 2026-05-{01,30}` for the same nine skills, plus the build target |
| Feature build state | 1 | `chore(feature): auto-commit` (smithery-manifest build artifact mirror) |

The feature auto-commit (`ca58297`) is the only one with non-trivial content — it adds `dashboard/outputs/feature-2026-05-01T11-23-53Z.json` (+226 lines) capturing the smithery-manifest skill's output as a render spec, and updates `memory/logs/2026-05-01.md` with the feature log entry. Every other commit modifies `.build-target`, `cron-state.json`, `memory/logs/`, `memory/token-usage.csv`, or `.outputs/{skill}.md` — all expected side effects of cron skill runs, not standalone work.

---

## Developer Notes
- **New dependencies:** None.
- **Breaking changes:** None.
- **Architecture shifts:** First skill that writes pure outward-facing publication artifacts (manifest, deployment yaml, submission body) intended to be consumed by external registries rather than internal Aeon pipelines. The byte-equality diff before notify pattern (already used by `simulator-evolution` style skills) is now the standard for "regenerate, only act on change" cron skills — `smithery-manifest` is the cleanest example of it because three independent files all need to be byte-stable for a no-op.
- **Tech debt:** `aeon-mcp` package is not yet published to npm — the manifest's `packages[0].identifier` claims a registry slot that doesn't exist. The skill writes the right name; publishing the package is a manual prerequisite tracked in the PR body. Until then, Smithery's deployment path works (it clones the repo and runs `node mcp-server/dist/index.js`) but the MCP Registry's npm-resolution path will 404.

## What's Next
- **Maintainer next steps for the smithery-manifest ship:** publish `aeon-mcp` to npm; submit `docs/smithery.yaml` to `smithery.ai/server/new`; open a PR at `modelcontextprotocol/registry` adding the server.json contents from `docs/smithery-manifest.json`.
- **aeon.yml enable list growing:** `pr-triage` (Apr 29 #147), `thread-formatter` (Apr 30 #148), and now `smithery-manifest` (May 1 #149) all shipped `enabled: false`. Three fresh skills waiting for the maintainer's enable pass — that backlog is now visible enough to be its own follow-up.
- **No open feature branches** on aeon (all autoresearch/* branches predate the 24h window). On aeon-agent, `improve/fetch-tweets-spam-quarantine` and `improve/self-improve-skill-runs-check` are both pre-window — no new work-in-progress branches in this window.
- **Watch the next cycle's repo-actions list:** Auto-Merge Agent PRs (Apr-26 idea #1, blocked on workflows-scope PAT) is the only remaining "longest-carried highest-priority" unbuilt now that smithery-manifest closed.
