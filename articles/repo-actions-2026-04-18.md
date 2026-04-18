# Repo Action Ideas — 2026-04-18

**Repos:** aaronjmars/aeon (189 stars, 28 forks, 92 skills, 2 open PRs) | aaronjmars/aeon-agent

**Context:** MIT License landed today — first commit in the log. Two PRs still open: star-milestone (#39) and Farcaster syndication (#40). Token at +901% 30d, 7 new stars today, 28 forks with at least one proven upstream backport (miroshark, Apr 17). The A2A gateway and MCP adaptor are live with zero observed external integrations yet — adoption is the strategic gap. Distribution infrastructure is complete; the work now is converting infrastructure into observable community traction.

---

### 1. Contributor Auto-Reward
**Type:** Integration
**Effort:** Small (hours)
**Impact:** The fork-to-upstream flywheel exists on paper (miroshark proved it Apr 17) but there's no incentive loop closing it. When a PR from a fork maintainer merges into upstream, automatically distribute $AEON to the contributor's wallet — detected via GitHub PR merge event, wallet resolved via Bankr handle lookup. This turns a one-time event into a repeatable pattern: fork, improve, get paid. It's the only missing link between the tweet-allocator rewards model and the dev community.
**How:**
1. Create `skills/contributor-reward/SKILL.md` as `workflow_dispatch` with optional `var: "PR number"`. Skill reads merged PRs from the last 24h via `gh api repos/aaronjmars/aeon/pulls?state=closed`, filters for PRs from non-org forks, extracts the author's GitHub handle, looks up their wallet via `.bankr-cache/`, and writes a reward plan to `.pending-distribute/contributor-reward-<date>.json`.
2. `postprocess-distribute-tokens.sh` (or extend existing distribute-tokens skill) reads the pending file and executes the on-chain transfer via the AEON contract on Base.
3. Log the payment to `memory/logs/YYYY-MM-DD.md` and send a notification tagging the contributor — a public thank-you that encourages the next fork maintainer.

---

### 2. Dashboard Live Feed
**Type:** Feature
**Effort:** Medium (1–2 days)
**Impact:** Skills write json-render specs to `dashboard/outputs/` after every run, but the dashboard has no live update mechanism — operators reload manually or miss runs entirely. A real-time feed turns the dashboard from a static report viewer into an active ops center. With 189 stars and a growing operator base, making the dashboard feel alive is the difference between a tool people check and a tool people keep open.
**How:**
1. Add a `/api/feed` Server-Sent Events endpoint to the Next.js dashboard that uses `fs.watch` on `dashboard/outputs/` and streams new file events as they land.
2. Wire the dashboard front page to this SSE stream: new skill outputs animate into the top of the feed without a page reload.
3. Add a pulsing "Live" indicator to the dashboard header that activates when a skill run is detected — matching the real-time feel of the token and notification panels already in place.

---

### 3. A2A Gateway Client Examples
**Type:** DX / Community
**Effort:** Medium (1 day)
**Impact:** The A2A gateway (PR #35) has been live since Apr 15 with zero observed external integrations. The technical barrier isn't the protocol — it's "show me working code." A `examples/a2a/` directory with copy-paste snippets for LangChain, AutoGen, CrewAI, and OpenAI Agents SDK drops onboarding friction from "figure it out" to "run this." Each example is a natural share artifact for the framework communities where Aeon needs discovery.
**How:**
1. Create `examples/a2a/langchain_example.py`, `autogen_example.py`, `crewai_example.py`, `openai_agents_example.py` — each ~50 lines, calling a real Aeon skill (e.g. `deep-research`) via the JSON-RPC endpoint with SSE streaming. Include a `requirements.txt` per example.
2. Create `examples/a2a/README.md` with a quickstart section and links to the A2A gateway docs in the main README.
3. PR to aaronjmars/aeon and link from the A2A section in the README — immediately gives every LangChain/AutoGen community member working code to try.

---

### 4. Public Status Page
**Type:** Community / DX
**Effort:** Small (hours)
**Impact:** 189 stars and 28 forks means there are operators running Aeon instances that new visitors can't see. A GitHub Pages status page at `aaronjmars.github.io/aeon/status` showing 30-day skill health (green/yellow/red per skill, success rates, last run time) builds credibility — "yes, this runs reliably in production" — and gives operators a URL to share when explaining their setup. All data is already in `memory/logs/`; this is a rendering layer on existing output.
**How:**
1. Extend `update-gallery` (already runs weekly) to also generate `docs/status.md` by parsing the last 30 days of heartbeat log entries. Extract per-skill status mentions, compute 30-day success rates, and format as a table with ✅/⚠️/❌ indicators.
2. Add "Status" to the GitHub Pages gallery navigation alongside the existing Articles and Skills pages.
3. Link from the README under the Skills section: "Live status across all 92 skills."

---

### 5. Skill Marketplace Listing (Smithery / MCP Registry)
**Type:** Growth
**Effort:** Small (hours)
**Impact:** The MCP adaptor wraps 92 skills as `aeon-<slug>` tools, but discovery requires cloning the repo. Smithery and the emerging MCP tool registries are where Claude Code users browse for new tools — Aeon belongs there. A listing puts 92 skills in front of every developer who opens Claude Code looking for automation tools, with zero ongoing maintenance cost once the listing is live.
**How:**
1. Generate a `smithery.yaml` manifest from `skills.json` — maps each skill's name, description, tags, and MCP tool signature to Smithery's schema. The `generate-skills-json` script already has all fields needed; add a `--smithery` flag that outputs the registry format.
2. Submit to Smithery's registry via their GitHub PR-based submission process (`smithery-ai/registry`). The submission is a single JSON/YAML file pointing to the `npx @aeon/skill-mcp` package.
3. Add a "Available on Smithery" badge to the README's MCP section — surfaces discovery from within the repo for operators who missed the listing.
