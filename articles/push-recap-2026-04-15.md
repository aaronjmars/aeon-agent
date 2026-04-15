# Push Recap — 2026-04-15

## Overview
4 significant commits across aaronjmars/aeon and aaronjmars/aeon-agent today, by @aaronjmars and aeonframework. The day's work split cleanly across two themes: a massive new interoperability layer opening Aeon's skill ecosystem to any AI framework, and a targeted security tightening that removes the one auto-trust assumption in the supply chain tooling built yesterday.

**Stats:** ~15 files changed, +1,002 / -8 lines across 4 substantive commits (plus 4 operational auto-commits)

---

## aaronjmars/aeon

### New Feature: A2A Protocol Gateway

**Summary:** Aeon's skills are now reachable by any AI agent framework on the planet. A new zero-dependency TypeScript HTTP server implements Google's Agent-to-Agent (A2A) protocol — the open standard for agent interoperability — and exposes every Aeon skill as a first-class A2A task endpoint. LangChain, AutoGen, CrewAI, OpenAI Agents SDK, and Vertex AI agents can now invoke Aeon skills directly via HTTP + JSON-RPC without needing Claude Desktop or the MCP client.

**Commits:**
- `9a680fb` — feat: A2A Protocol Gateway — expose all Aeon skills to any AI agent framework *(PR #35, open)*
  - New file `a2a-server/src/index.ts` (+536 lines): Zero-dependency TypeScript server using Node.js built-ins only. Implements three endpoints: `GET /.well-known/agent.json` returns an agent card advertising all Aeon skills with metadata (name, description, accepted inputs); `POST /` is the JSON-RPC hub handling `tasks/send`, `tasks/get`, `tasks/cancel`; `POST /tasks/sendSubscribe` streams live SSE events for long-running skills. Skills are invoked by spawning `claude -p -` identically to how GitHub Actions runs them. Tasks are tracked in-memory with a full state machine: submitted → working → completed/failed/canceled.
  - New file `add-a2a` (+181 lines): One-command install script, mirroring the existing `add-mcp` pattern. Supports `--port`, `--build-only`, and `--print-config` (prints ready-to-paste LangChain tool wrapper + Python polling example).
  - Modified `README.md` (+64 lines): New "Use with any AI agent (A2A)" section with endpoint reference, Python usage example, and SSE curl snippet.
  - New files `a2a-server/package.json`, `a2a-server/tsconfig.json`, `a2a-server/.gitignore`: TypeScript ESM build config with zero runtime dependencies (only devDep is `@types/node`).

**Impact:** MCP covers Claude Desktop/Code users; A2A now covers everyone else. The two protocols together mean Aeon's growing library of 68+ skills is usable from any major AI orchestration layer without custom integration work. For the ecosystem, this is the difference between Aeon being a Claude-specific tool and being a general-purpose skill infrastructure layer.

---

### Security Fix: skills.lock Auto-Advance Gated Behind Human Confirmation

**Summary:** The `skill-update-check` skill introduced yesterday (PR #32) had one trust assumption baked in: when a security scan returned PASS, it would automatically advance the locked SHA in `skills.lock`. This was a supply-chain risk — automatic trust elevation on a security verdict, with no human in the loop. PR #34 removes it. The lock no longer advances automatically under any circumstances.

**Commits:**
- `dec432c` — fix(security): gate skills.lock auto-advance behind human confirmation *(PR #34, merged)*
  - Changed `skills/skill-update-check/SKILL.md` (+7/-7 lines): Step 9 rewritten — instead of `jq ... .commit_sha = $sha ...`, the skill now only updates `last_checked` timestamps across all entries. The auto-SHA advancement block is replaced with a clear prohibition: *"Never auto-advance `commit_sha` in `skills.lock`, even when the security verdict is PASS. Advancing the lock is a supply-chain trust decision that requires explicit human approval."*
  - Step 10 notification extended: PASS outcomes now include `./add-skill <source_repo> <skill-name>` as the explicit opt-in command for the operator to advance the lock.
  - The recommendation text updated from "Safe to update" to "Safe to update — run `./add-skill` to accept."

**Impact:** Closes issue #33 (opened and merged same day). The lock file is now strictly an audit trail until a human consciously advances it. The self-improvement loop can still detect upstream changes, run security scans, and report — but can't execute trust elevation without operator action. This is the correct baseline for a supply-chain security feature.

---

## aaronjmars/aeon-agent

### New Skill: skill-leaderboard + Immediate Pagination Fix

**Summary:** A new weekly skill tracks which Aeon skills are most widely adopted across the fork ecosystem. It scans `aeon.yml` files across active forks, aggregates enabled skill counts, and surfaces both the consensus skills (adopted by most forks) and the adoption gaps (skills that exist but few forks have enabled). The skill shipped with a pagination bug that was caught and fixed same day.

**Commits:**
- `fea3531` — improve: add skill-leaderboard *(PR #9, merged)*
  - New file `skills/skill-leaderboard/SKILL.md` (+97 lines): Fetches all forks active in the last 30 days, reads each fork's `aeon.yml`, aggregates enabled skill counts, ranks by adoption frequency, identifies gaps, and outputs a weekly leaderboard article + notification.
  - Modified `aeon.yml` (+1 line): Scheduled Sundays at 17:00 UTC using Sonnet model.

- `65f511c` — fix(skill-leaderboard): add --paginate to forks API call *(PR #11, merged)*
  - Changed `skills/skill-leaderboard/SKILL.md` (+1/-1 line): Added `--paginate` flag to `gh api repos/${TARGET_REPO}/forks`. Without it, the GitHub API returns at most 30 forks per page — as the fork count grows past 30, the leaderboard would silently truncate and produce inaccurate rankings.

**Impact:** Aeon now has visibility into its own adoption. The leaderboard creates a feedback loop: skills that spread widely across forks are signaling community demand, and skills in the main repo that forks haven't adopted may need better documentation or discoverability. The pagination fix was caught before the first real run.

---

### Content & Memory

**Commits:**
- `56fcbe6` — feat(repo-article): "Locked, Tracked, Verified: Aeon Builds a Skills Lock File Before the Agent Supply Chain Implodes" (+47 lines article)
  - New file `articles/repo-article-2026-04-14.md`: Connects the skills.lock / skill-update-check build to the broader agent supply chain security narrative (ClawHavoc / OpenClaw attack, January 2026). Argues that lock-file discipline is the right baseline for production agents at 68+ skills.

- `a9aa30f` — chore(memory): log A2A gateway feature build — aeon PR #35 (+12 lines)
  - Updated `memory/MEMORY.md`: Added A2A gateway row to Skills Built table.
  - Updated `memory/logs/2026-04-15.md`: Logged feature details, files created, and PR link.

---

## Developer Notes

- **New dependencies:** None (a2a-server intentionally zero runtime deps — `@types/node` devDep only)
- **Breaking changes:** `skill-update-check` behavior change — operators who expected automatic SHA advancement must now run `./add-skill` manually. This is intentional and documented in the notification output.
- **Architecture shifts:** Aeon now has two interoperability layers: MCP (`add-mcp`) for Claude-native clients, A2A (`add-a2a`) for everything else. The skill invocation path is identical — both ultimately spawn `claude -p -`.
- **Tech debt:** A2A task state is in-memory only (no persistence across server restarts). Acceptable for v1 but worth noting as the server matures.

## What's Next

- **PR #35 (A2A gateway) needs review and merge** — no CI failures visible, the implementation follows the same pattern as the MCP adaptor. Likely to merge tomorrow.
- **skill-leaderboard first run Sunday** — will give the first real read on fork adoption patterns across the 17 active forks.
- **A2A + MCP docs** — the README has both sections now. A follow-up article or comparison guide could help developers pick the right integration path.
- **Pagination pattern** — the same `--paginate` omission could affect other skills that call list-type GitHub APIs. Worth auditing systematically.
