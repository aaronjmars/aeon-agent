# Repo Actions — aaronjmars/aeon — 2026-06-18

**Top pick for tomorrow:** #1 — Add A2A server quickstart guide to `apps/a2a-server/` and README (DX, Small)
**Verdict:** Five documentation gaps anchored to unreferenced root scripts and undocumented sub-apps — all new ecosystem surface shipped without entry-point docs; Top pick bridges A2A interop for the four major agent frameworks already waiting in `examples/a2a/` with no path from the README.

## Actions

### 1. Add A2A server quickstart guide to `apps/a2a-server/` and main README
**Priority:** HIGH
**Type:** DX
**Effort:** Small (hours)
**Anchor:** FILE:apps/a2a-server/src/index.ts (no README; `examples/a2a/` has 4 framework clients — autogen, crewai, langchain, openai-agents — with no parent documentation linking them)
**Score:** L=4 C=4 N=5 (total 13/15)
**Impact:** Every developer evaluating Aeon from AutoGen, LangChain, CrewAI, or OpenAI Agents SDK lands on `apps/a2a-server/` as their entry point — right now they find source code with no README, no quickstart, and no link from the main README. A two-minute read that shows "run the server, paste this config, call Aeon as a task" converts evaluators who already have agent infra into fork-and-deploy operators.
**How:**
1. Read `apps/a2a-server/src/index.ts` and `apps/a2a-server/package.json` to establish the server's protocol (A2A spec version, exposed endpoints, required env vars, default port).
2. Create `apps/a2a-server/README.md` with four sections: **What it is** (Aeon exposed as an A2A-compatible agent — call any skill as a task from any framework), **Quickstart** (`npm install && node src/index.ts`, required env: `GITHUB_TOKEN` + `ANTHROPIC_API_KEY`), **Framework examples** (link to `examples/a2a/autogen_workflow.py`, `crewai_task.py`, `langchain_client.py`, `openai_agents_client.py`), and **Protocol** (the A2A task/agent card schema Aeon implements).
3. Add a two-line "A2A / Agent interop" entry to the main `README.md` under the integrations or quickstart section: "Call any Aeon skill from AutoGen, CrewAI, LangChain, or OpenAI Agents via the A2A server — see `apps/a2a-server/README.md`."
**Definition of done:** `gh api repos/aaronjmars/aeon/contents/apps/a2a-server/README.md --jq .size` returns non-null; a developer familiar with any of the four example frameworks can start the server and fire a skill call from a cold read without opening `src/index.ts`.

---

### 2. Add `./new-from-template` CLI and skill template catalog to README
**Priority:** MED
**Type:** DX
**Effort:** Small (hours)
**Anchor:** FILE:README.md (`new-from-template` root script is absent from README; `skill-templates/` has 6 community-contributed scaffolds — code-reviewer, community-manager, crypto-tracker, deploy-watcher, research-digest, social-monitor — none surfaced to contributors)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** Every fork contributor who wants to write a custom skill currently starts from a blank file or copies an existing skill — both are higher-friction than running `./new-from-template research-digest my-news-tracker`. The 6 templates represent the most common skill patterns; surfacing the CLI and the catalog directly in README turns a hidden developer tool into the default contribution path, which reduces first-skill friction for the 180-fork cohort.
**How:**
1. Read `new-from-template` to confirm its CLI interface (expected: `./new-from-template <template> <skill-slug>` where template is one of the `skill-templates/` directory names).
2. In `README.md`, add a "Create a skill from a template" subsection adjacent to the existing `./add-skill` docs: list available templates in a compact table (template name + one-line description from `skill-templates/<name>/SKILL.md`'s `description:` frontmatter), then the usage: `./new-from-template research-digest my-news-tracker` → scaffolds `skills/my-news-tracker/` from the template.
3. Add a `skill-templates/TEMPLATE.md` reference note: "To add a new template, open a PR adding a `skill-templates/<name>/SKILL.md` following the structure in `skill-templates/TEMPLATE.md`."
**Definition of done:** `curl -s https://raw.githubusercontent.com/aaronjmars/aeon/main/README.md | grep -c "new-from-template"` returns ≥1; a new contributor can find, pick, and run a template from the README without browsing the filesystem.

---

### 3. Document `./install-from-atrium` in README under community packs
**Priority:** MED
**Type:** Growth / DX
**Effort:** Small (hours)
**Anchor:** FILE:install-from-atrium (root script; absent from README; Atrium = onchain skill marketplace where `atrium-publish`/`atrium-scout`/`atrium-earnings` from `Atrium-Hermes/aeon-atrium-skills` operate)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** `install-skill-pack` (CLI and dashboard) covers community packs from GitHub repos. `install-from-atrium` is the entry point for pay-gated / monetized skills from the Atrium onchain marketplace — a distinct install surface that powers the x402 payments narrative Aeon has been building toward. Without a README mention, every operator who reads about the Atrium Skills pack in the community catalog has no documented path to actually install an Atrium-sourced skill outside of the pack wrapper.
**How:**
1. Read `install-from-atrium` to confirm its CLI interface (expected: `./install-from-atrium <atrium-skill-id>` with USDC-on-Base settlement via x402).
2. Add a brief "Pay-gated skills via Atrium" bullet under the existing Community skill packs section in `README.md`: "Skills listed on [Atrium](https://atriumhermes.tech): `./install-from-atrium <skill-id>` — settles the access fee via x402/USDC on Base, then installs the skill the same way as `./add-skill`."
3. Link the bullet to `apps/a2a-server` context if the Atrium server uses the A2A path; otherwise keep as a standalone bullet.
**Definition of done:** `curl -s https://raw.githubusercontent.com/aaronjmars/aeon/main/README.md | grep -c "install-from-atrium"` returns ≥1; an operator reading about Atrium Skills in the community packs table can immediately find the install path.

---

### 4. Add `apps/mcp-server/README.md` with quickstart and Claude Desktop config
**Priority:** MED
**Type:** DX
**Effort:** Small (hours)
**Anchor:** FILE:apps/mcp-server/src/index.ts (no README; `examples/mcp/claude_desktop_config.json` and `examples/mcp/test_connection.py` exist unreferenced; `.mcp.json.example` at root also lacks a parent doc)
**Score:** L=3 C=4 N=5 (total 12/15)
**Impact:** The MCP server makes all of Aeon's skills available as tools to Claude Desktop, Claude Code, and any MCP-compatible client — but there's no README connecting the server to its example config. Developers who want to drive Aeon's skills from within Claude Desktop currently have to infer the connection from `.mcp.json.example` and `examples/mcp/` without documentation. A one-page README and a link from the main README closes this gap and opens Aeon to the Claude Desktop user base.
**How:**
1. Read `apps/mcp-server/src/index.ts` and `apps/mcp-server/package.json` to confirm the server's exposed tool list, required env vars, and default port/transport.
2. Create `apps/mcp-server/README.md` with: **What it exposes** (each Aeon skill as an MCP tool, parameterized by `var`), **Quickstart** (`npm install && node src/index.ts`, env: `GITHUB_TOKEN` + `ANTHROPIC_API_KEY`), **Claude Desktop config** (paste from `examples/mcp/claude_desktop_config.json` with the server command pre-filled), and **Testing** (link to `examples/mcp/test_connection.py`).
3. Add a one-line "MCP server" entry to the main `README.md` under integrations: "Use any Aeon skill as an MCP tool in Claude Desktop or Claude Code — see `apps/mcp-server/README.md`."
**Definition of done:** `gh api repos/aaronjmars/aeon/contents/apps/mcp-server/README.md --jq .size` returns non-null; a user with Claude Desktop can connect to Aeon and run a skill as an MCP tool call from the README alone.

---

### 5. Update SHOWCASE.md with 2026-06-18 ecosystem snapshot
**Priority:** MED
**Type:** Community / Growth
**Effort:** Small (hours)
**Anchor:** FILE:SHOWCASE.md (525 stars, 180 forks, 24 community packs as of 2026-06-18; two new packs merged today — clawhunter-skills #498, Polymarket Trader by Simmer #499)
**Score:** L=3 C=3 N=5 (total 11/15)
**Impact:** SHOWCASE.md is the social-proof document potential contributors and forkers see when evaluating community health — at 525 stars and 24 community packs it's the repo's single most powerful "this is real" signal for builders on the fence. An outdated SHOWCASE undercuts the momentum that the pack velocity (6 new packs in the last 30 days) has built.
**How:**
1. Read `SHOWCASE.md` to understand its current structure (likely: live instances, featured packs, notable contributors).
2. Update the ecosystem numbers to: 525 stars, 180 forks, 24 community packs, `skill-packs.json` as the authoritative source; add the two newest packs — clawhunter-skills (Pump Fun GO bounty discovery, x402 on Solana/Base) and Polymarket Trader by Simmer (live Polymarket position-taking, simulate-by-default, bounded) — to the featured packs list.
3. If the SHOWCASE includes a "contributors this month" section, ensure the most recent external pack authors (clawhunter, SpartanLabsXyz/Simmer) are credited.
**Definition of done:** `gh api repos/aaronjmars/aeon/contents/SHOWCASE.md --jq .size` returns a size larger than before the commit; the two packs merged 2026-06-18 appear in the file; ecosystem numbers (stars, forks, packs) reflect the 2026-06-18 snapshot.

---

## Monitor

### A. PR #418 (BEAMR gateway) — rebase requires contributor action
**Why not yet:** The branch lives on SahilParikh03's fork (`feat/beamr-gateway`); rebasing requires either the contributor to rebase their own branch or a maintainer with push access to the fork. `external-feature` can post a comment guiding the rebase, but the actual git push must come from the contributor. Now 8 days stale (last updated 2026-06-16); the conflicts are in `scripts/llm-gateway.sh` and `apps/dashboard/lib/types.ts` from the chain of merges since 2026-06-10.
**Anchor:** PR:#418 "feat(gateway): add BEAMR as an LLM gateway"

### B. Smithery listing submission
**Why not yet:** `docs/smithery.yaml`, `docs/smithery-manifest.json`, and `docs/smithery-submission.md` exist but the current status (submitted, pending, or draft) is unknown without reading the submission doc. If submission requires creating an account on smithery.ai or opening a PR on their catalog repo, that may fall outside `external-feature`'s autonomous scope without verification. Read `docs/smithery-submission.md` first to determine if this is a one-click or review-gated action.
**Anchor:** FILE:docs/smithery-submission.md

---

## Fleet follow-ons

- aaronjmars/minitor: pushed 2026-06-18T13:27:48Z (11 stars, 1 fork) — MEMORY flags no remaining queued actions after #75 (CONTRIBUTING.md) merged; PR #76 (CI build workflow, contributor) was still open as of 2026-06-17. If #76 is unreviewed, a one-line CI trigger test note in the PR description (`npm run build` baseline) would reduce reviewer friction.

---

**Source status:** gh=ok (rate limit reached at end of run; primary data collected before limit) code_search=n/a memory_topics=missing articles_dir=ok watched_repos=2 parsed (aeon-agent skipped)
**Mode:** REPO_ACTIONS_OK
**Carried over from prior runs:** — (2026-06-16 top pick "Validate and merge PR #472" → MERGED as #472 2026-06-16)
