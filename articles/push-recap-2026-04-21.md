# Push Recap — 2026-04-21

## Overview

Biggest push day in the history of this repo. Eighty-one PRs merged across two watched repos, driven almost entirely by a single coordinated autoresearch-evolution sweep that rewrote 80 skill SKILL.md files on `aaronjmars/aeon` under one design pattern ("variation B — sharper output"). Alongside the sweep: a real feature ship (A2A + MCP integration examples, PR #137), two README polishes, and the merge of the prefetch-error-marker reliability fix for XAI failures on `aeon-agent` (PR #16).

**Stats:** 89 files changed, +12,213/-4,961 lines across 83 meaningful commits (80 autoresearch-evolution squash-merges + 3 non-sweep aeon commits + 2 non-sweep aeon-agent commits). 26 autonomous cron/chore auto-commits on aeon-agent excluded.

---

## aaronjmars/aeon

82 commits by @aaronjmars (all squash-merged PRs). One real feature, two README touches, and 80 autoresearch-evolution skill rewrites.

### Theme 1: Autoresearch Evolution — Mass Skill Rewrite (80 PRs)

**Summary:** A coordinated research-then-rewrite pass across eighty skills. Each PR runs the same loop: generate four variation drafts (A: better inputs / B: sharper output / C: more robust / D: rethink from an attacker or user angle), score each against weighted criteria (clarity ×1.5, data quality ×1.5, output value ×2, robustness ×1.5, conventions ×1, improvement headroom ×3 over a 52.5-point scale), and merge the winning variation as the new SKILL.md — almost always **Variation B (sharper output)** by design. The shared design pattern across all 80 rewrites: kill the "flat list every run" output shape and replace it with (1) ranked/tiered output, (2) delta classification against the prior run, (3) significance-gated notifications that go silent when there is nothing new, and (4) an explicit exit taxonomy (`CLEAN` / `UNCHANGED` / `NEW_*` / `TOOL_FAIL` / etc.) so the operator can grep outcomes.

**Representative commits (15 largest of 80):**
- `73de769` — `improve(spawn-instance)` (#129) — skills/spawn-instance/SKILL.md, +354/-172
- `1ea45d7` — `improve(fork-fleet)` (#125) — skills/fork-fleet/SKILL.md, +277/-121
- `69dcc86` — `improve(skill-leaderboard)` (#116) — score against *configured* fork denominator only (excludes untouched templates), output tiered Promote/Match/Sunset insights, +250/-91
- `e3e02ec` — `improve(fleet-control)` (#133) — skills/fleet-control/SKILL.md, +248/-124
- `88d688e` — `improve(vuln-scanner)` (#70) — skills/vuln-scanner/SKILL.md, +248/-161
- `257212c` — `improve(market-context-refresh)` (#91) — concrete 3-line Take template, token-picks preservation, +244/-111
- `676dfd2` — `improve(skill-repair)` (#128) — skills/skill-repair/SKILL.md, +241/-83
- `dde1789` — `improve(repo-actions)` (#131) — skills/repo-actions/SKILL.md, +237/-67
- `0a43b79` — `improve(update-gallery)` (#126) — 6-char sha1 suffix to prevent truncation collisions, +229/-85
- `856735d` — `improve(issue-triage)` (#72) — tunable per-repo budget + ISSUE_TRIAGE_LABEL_SKIPPED try/log on label failure, +216/-30
- `74ed4b2` — `improve(repo-scanner)` (#121) — stable output schema documented for downstream consumers, +213/-61
- `ca3ad10` — `improve(last30)` (#122) — skills/last30/SKILL.md, +207/-142
- `d188bcb` — `improve(weekly-shiplog)` (#120) — skills/weekly-shiplog/SKILL.md, +199/-65
- `b16f312` — `improve(auto-workflow)` (#136) — skills/auto-workflow/SKILL.md, +197/-156
- `f5914c4` — `improve(create-skill)` (#124) — soften research gate, secrets only inspectable by name, +194/-75

**Concrete output-shape upgrades observable in the diffs:**
- `workflow-security-audit` (#127, +312/-74): 5-category hand-rolled checklist → zizmor + actionlint as primary scanners with hand-rolled backstops for specific attack patterns (toJson-into-shell, `persist-credentials: true` + PR head checkout, `GITHUB_ENV` injection, fleet spawn-instance inputs). Every finding classified **NEW / REINTRODUCED / UNCHANGED / RESOLVED** against the prior audit. Attack-chain narrative (entry → vector → sink → reachable secrets → blast radius) replaces the flat "Risk:" line for Critical/High. PR+notify gated on delta — silent on CLEAN/UNCHANGED.
- `github-issues` (#48, +86 lines): flat 24h issue list → ranked P0/P1/P2/P3 triage queue with single `gh search issues` call + per-repo fallback, dedup against 2-day log scan, skip-notify on empty set.
- `fetch-tweets` (#46, +64/-30): flat chronological tweet list → curated digest clustered by sub-narrative with signal-line extraction + per-cluster insight.
- `push-recap` (#104, +188/-82) — the very skill running this recap: adds verdict line, user-visible/internal shipment split, impact ranking, significance-gated notification. *Not yet deployed on this aeon-agent instance.*
- `skill-health` (#86, +153/-71): guard issue filing on `memory/issues/INDEX.md` existence.
- `reply-maker` (#68): 12h recency fallback, extract banned-phrase list into an editable section.
- `narrative-tracker` (#54): log NARRATIVE_CACHE_MISS explicitly, explicit WATCH fallback.

**Commits also carry "clarification" fix-ups merged in the same PR:** 20+ PRs include a trailing `fix(<skill>): ...` commit on top of the initial autoresearch-evolution commit — e.g. `fix(skill-graph): document state file in Constraints; safe to delete`; `fix(create-skill): soften research gate`; `fix(workflow-security-audit): pin zizmor==1.24.1 for reproducibility`. These are last-mile edits applied during review, not separate commits on main (squash-merged into each PR's single commit visible here).

**Impact:** Of the 93 skills in `aeon.yml`, roughly 80 now share a uniform output-shape contract (tier/rank + delta + exit taxonomy + significance gate) instead of idiosyncratic per-skill output formats. For operators, that means the notification signal-to-noise ratio should rise sharply over the next cycle as redundant re-alerts stop firing on unchanged state. For the agent, it means significantly more skill runs will exit via `SKIP_EMPTY` / `SKIP_UNCHANGED` rather than sending a "nothing to report" notification.

**Notable constraint:** the running instance (this `aeon-agent`) tracks upstream `aeon` but receives skill updates via PRs or fork sync — so **most of these 80 rewrites are not yet deployed here**. They will land as PRs into `aeon-agent` over the coming days (the skill-update-check skill tracks this), or via the next fork sync. Today's `push-recap` run is operating on the old `skills/push-recap/SKILL.md`.

### Theme 2: A2A + MCP Integration Examples (1 PR)

**Summary:** Closes the adoption gap flagged in yesterday's `repo-actions` run (idea #1, "A2A / MCP Client Integration Examples"): gateway and adaptor have been live for weeks with zero observed external integrations because there were no copy-paste demos.

**Commits:**
- `dc8e3f7` — `feat: integration examples for A2A gateway and MCP server` (#137)
  - New `examples/a2a/langchain_client.py` — wraps an Aeon skill as a LangChain Tool; calls `aeon-fetch-tweets` (+85 lines)
  - New `examples/a2a/autogen_workflow.py` — registers `aeon-deep-research` as a function tool inside an AutoGen multi-agent conversation (+96 lines)
  - New `examples/a2a/crewai_task.py` — wraps `aeon-pr-review` as a CrewAI `BaseTool` (+88 lines)
  - New `examples/a2a/openai_agents_client.py` — registers `aeon-token-report` as an OpenAI Agents SDK function tool (+87 lines)
  - New `examples/mcp/test_connection.py` — spawns `node mcp-server/dist/index.js`, runs `tools/list`, invokes one tool (default: `aeon-cost-report`) as a stdio sanity check (+86 lines)
  - New `examples/mcp/claude_desktop_config.json` — 8-line drop-in Claude Desktop MCP config snippet
  - New `examples/README.md` — walk-through (+55 lines)
  - Changed `README.md` — new "Integration examples" subsection under "Integrations (MCP & A2A)" (+15 lines)
  - Each A2A script is under 100 lines, depends only on `requests` + the framework SDK, and reads its endpoint from `A2A_GATEWAY_URL`

**Impact:** Four agent-framework ecosystems (LangChain, AutoGen, CrewAI, OpenAI Agents SDK) each get a working <5-minute first-call demo, plus an MCP stdio connectivity test. Every README visitor reading about MCP/A2A now has a clickable path to a working integration. The script library is the first production-ready external integration surface for the gateway.

### Theme 3: README Polish (2 commits)

**Commits:**
- `85ea010` — `Add star history section to README` (+11 lines) — adds `<p align="center">` badge row (GitHub stars / forks / X follow / Bankr) at the top of the README and a "Star History" chart (star-history.com SVG) in the footer above the support address.
- `71483fc` — `Update social media link in README` (+1/-1) — follow-up tweak to the badge row: swaps the X-handle link from `miroshark_` to `aeonframework` (first PR used the wrong handle).

**Impact:** Cosmetic + signal — the star-history chart is a vanity metric that's nonetheless load-bearing for project-selection readers. The handle fix lines up the public X identity with the project name.

---

## aaronjmars/aeon-agent

2 meaningful commits + 26 autonomous chore auto-commits (heartbeat/scheduler/skill run acks — excluded from the meaningful count).

### Theme 4: XAI Prefetch Error Marker Merged (1 PR)

**Commits:**
- `d90bd6c` — `improve: prefetch error marker + skill short-circuit on XAI failures` (#16)
  - Changed `scripts/prefetch-xai.sh` (+23/-6): retry budget raised from 2 → 3 attempts, `--connect-timeout 30` so DNS/connect failures fail fast within budget, `-sS` so curl errors hit stderr, writes a one-line reason to `.xai-cache/<outfile>.error` on terminal failure (cleared at the start of each new attempt)
  - Changed `skills/fetch-tweets/SKILL.md` (+3/-1): adds Path A short-circuit — if cache JSON missing AND `.xai-cache/fetch-tweets.json.error` present, jump straight to step 4 with status `FETCH_TWEETS_PREFETCH_FAILED` and surface the prefetch error reason in the notification
  - Also includes a squash-time fix commit aligning the error-marker filename with what the prefetch script actually writes (`.xai-cache/fetch-tweets.json.error`, not `.xai-cache/fetch-tweets.error`) — the original patch had the short-circuit looking at the wrong path and would never have fired
  - **Trigger:** Apr 19 + Apr 20 morning fetch-tweets runs both logged `FETCH_TWEETS_EMPTY` because the XAI prefetch curl timed out at 60s with no visible retry log, after which the skill burned ~10K tokens probing Path B (sandbox blocks `$XAI_API_KEY` env-var expansion → always fails) and Path C (WebSearch returns 0 fresh X.com results when XAI is the source of truth). Two failures in two days.

**Impact:** Turns a ~10K-token wasted run on prefetch failure into a fast no-op with a diagnostic surface. Generic across all `xai_search()` callers (refresh-x, remix-tweets, narrative-tracker, article, tweet-roundup, fetch-tweets) — the pattern can be propagated to the other skills' SKILL.md files as their failure modes match. Already paying off: today's fetch-tweets run found 13 tweets via Path A (prefetch cache healthy).

### Theme 5: README Badges (1 commit)

**Commits:**
- `3a5d656` — `Enhance README with social media and project badges` (+7 lines) — adds the same `<p align="center">` badge row (GitHub stars / forks / X follow @aeonframework / Bankr) near the top of the aeon-agent README. Mirrors the aeon PR but without the star-history chart (which is repo-specific anyway).

**Impact:** Brings aeon-agent's README cosmetic surface in line with aeon's. The X handle on this side already pointed at `aeonframework` — no correction commit needed.

---

## Developer Notes

- **New dependencies:** None. The integration examples specify pip installs in their docstrings (`langchain`, `langchain-openai`, `pyautogen`, `crewai`, `crewai-tools`, `openai-agents`, `requests`, `mcp`) but those are operator-side, not added to the repo.
- **Breaking changes:** None merged — but the autoresearch rewrite introduces a new **exit taxonomy** across ~80 skills (`SKIP_EMPTY` / `SKIP_UNCHANGED` / `NEW_*` / etc.). Log consumers (heartbeat, skill-evals, skill-health) that grep for the old flat success/empty markers will need to be audited against the new strings once the rewrites deploy downstream.
- **Architecture shifts:** Biggest shift is on aeon, not aeon-agent — the 80-skill rewrite bakes "significance-gated notification" into skill contracts by default, which should reduce Telegram/Discord/Slack noise substantially once deployed. Secondary shift: integration-examples/ is now the canonical onboarding surface for external agent frameworks, not just README prose.
- **Tech debt:** The 80 rewrites all landed on `aeon` (upstream) in one day. They need to propagate to aeon-agent (the running instance) — either via `skill-update-check` scheduling 80 sync PRs, via a targeted fork-sync, or by the operator explicitly pulling. Until then, this running agent is operating on pre-evolution versions of its own skills.
- **Fix-up commits inside PRs:** ~20 of the 80 autoresearch PRs needed a review-time `fix(<skill>): ...` commit on top of the generated SKILL.md. Recurring patterns: "soften empty-var abort with fallback", "annotate magic constants as tunable", "pin tool version for reproducibility", "degrade gracefully when memory state file missing". This suggests the autoresearch generator currently over-aborts and under-documents heuristics — a generator-level improvement would remove most of the fix-up churn.

## What's Next

- **Propagate the 80 skill rewrites to aeon-agent.** Either via skill-update-check (scheduled but will queue slowly at 80 PRs) or via a one-shot fork sync. Current aeon-agent runs have stale skills by design — push-recap on this run is literally the old version describing its replacement.
- **First-consumer signal for integration examples.** PR #137 shipped today — watch `agent-buzz` + repo-pulse for any external-integration traffic (LangChain/AutoGen/CrewAI/OpenAI-Agents users trying the demos). If zero adoption within a week, the examples need a distribution step (blog post / tweet / Smithery listing — idea #5 from yesterday's `repo-actions`).
- **Propagate the prefetch error-marker pattern to sibling xai_search() callers.** d90bd6c fixes fetch-tweets end-to-end, but refresh-x, remix-tweets, narrative-tracker, article, and tweet-roundup share the same dead-end Path B/C structure. Matching short-circuits on their SKILL.md would extend the same ~10K-token savings per failed run to those skills.
- **Audit skill-health, skill-evals, heartbeat, and ./scripts/skill-runs for the new exit taxonomy** before the autoresearch rewrites deploy here — old string matches (`*_OK`, `*_EMPTY`) may miss the new `SKIP_UNCHANGED` / `NEW_INFO` / etc. markers.
- **Open branches visible in diffs:** none. Every commit today is on `main` at its repo.
