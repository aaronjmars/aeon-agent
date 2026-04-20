# Repo Action Ideas — 2026-04-20

**Repos:** aaronjmars/aeon (198 stars, 32 forks, 93 skills) | aaronjmars/aeon-agent
**Context:** Massive two-week sprint closed: A2A gateway, MCP adaptor, Memory Search API (#41), fork-contributor-leaderboard (#42), MIT License, three-layer dedup stack, Opus 4.7. The infrastructure layer is dense but adoption hasn't followed — 32 forks, ~26 active, zero confirmed A2A/MCP external integrations observed. Token at +1,180% 30d, community engagement rising (12 tweets logged Apr 20, whale buys, gem-hunter mentions). Pipeline ideas that are tracked but unbuilt: Dashboard Live Feed, Public Status Page, Webhook-to-Skill Bridge, Skill Template Library, Skill Run Analytics Widget. This run goes to fresh territory: adoption surface, operator DX, community feedback loops, and growth distribution.

---

### 1. A2A / MCP Client Integration Examples
**Type:** Community / DX
**Effort:** Small (hours)
**Impact:** The A2A Gateway and MCP adaptor have been live for weeks with zero observed external integrations. The barrier isn't protocol complexity — it's that operators face a blank page after "install the server." A working `examples/` directory with four copy-paste client scripts (LangChain, AutoGen, CrewAI, OpenAI Agents SDK) each calling a real Aeon skill collapses adoption time from "read the spec" to "change the URL." The fork-contributor-leaderboard rewards contributors; this rewards early integrators by making the first integration trivially easy. At 198 stars, even 2–3 confirmed integrations in external agent stacks would be worth a tweet thread.
**How:**
1. Create `examples/a2a/` with four self-contained scripts: `langchain_client.py` (calls `fetch-tweets` skill via A2A JSON-RPC), `autogen_workflow.py` (calls `deep-research`), `crewai_task.py` (calls `pr-review`), `openai_agents_client.py` (calls `token-report`). Each script is <80 lines, includes a one-paragraph setup comment, and uses only the public `A2A_GATEWAY_URL` env var — no Aeon-internal secrets needed.
2. Create `examples/mcp/` with a `claude_desktop_config.json` snippet and a minimal `test_connection.py` that lists all `aeon-*` tools and invokes one. Add a `README.md` in `examples/` linking both directories with expected outputs.
3. Add an "Integration Examples" section to the main README (after the MCP/A2A table) pointing to `examples/` — so every visitor who reads about the gateway has a clickable path to running it in under 5 minutes.

---

### 2. Operator Onboarding Validator
**Type:** DX
**Effort:** Small (hours)
**Impact:** 32 forks exist, ~26 are active. The delta (6 silent forks) and the setup drop-off rate from new forks represent recoverable growth — operators who forked but never got Aeon running. A one-shot `onboard` skill that validates the full setup (secrets present, Actions enabled, notification channel reachable, memory/ writable, first skill run logged) and sends a step-by-step checklist notification with exact fix instructions for each gap turns "fork and hope" into a guided 10-minute onboarding. This is especially valuable as the fork count grows: at 100 forks, even 20% abandonment is 20 lost community members.
**How:**
1. Create `skills/onboard/SKILL.md` — a one-shot skill (not scheduled; run via manual dispatch or added to `add-skill` flow). It checks: `ANTHROPIC_API_KEY` or `CLAUDE_CODE_OAUTH_TOKEN` present in secrets (via `gh secret list`), at least one notification channel configured (`TELEGRAM_BOT_TOKEN` or `DISCORD_WEBHOOK_URL` or `SLACK_WEBHOOK_URL`), `memory/MEMORY.md` exists and is writable (write a temp timestamp, delete it), `aeon.yml` has at least one skill enabled with a valid schedule.
2. For each check, produce a pass/fail result with a one-line fix instruction ("Set ANTHROPIC_API_KEY in Settings → Secrets → Actions → New repository secret"). Compile into a single Markdown checklist notification via `./notify`.
3. Add a `./onboard` CLI entry point (or extend `./aeon` setup wizard) that runs `gh workflow run` with `skill: onboard` — so the command is discoverable alongside `./aeon` and `./add-skill` in the README Quick Start section.

---

### 3. Reactive Inbound Commands (Telegram / Discord)
**Type:** Integration
**Effort:** Medium (1–2 days)
**Impact:** Operators can read Aeon's notifications but can't direct it without opening GitHub Actions. The inbound message infrastructure already exists (Telegram offset-polling, Discord reaction-based ack). Extend it to parse free-form commands — "run fetch-tweets", "show token price", "what did you do today?" — and dispatch the matching skill via `workflow_dispatch`. This turns every configured notification channel into a natural-language remote control. The use case is real: mobile operators who see a crypto spike want to trigger `token-report` immediately, not wait for the next hourly cron. For Aeon's autonomy narrative, "the agent that responds to you" is a stronger story than "the agent that ignores you."
**How:**
1. Extend the inbound message polling (in `scripts/` or a new `skills/command-gateway/SKILL.md`) to parse message text against a command table: exact-match skill names (e.g. "fetch-tweets" → dispatch `fetch-tweets` skill), keyword aliases ("token price" → `token-report`, "today's log" → read today's `memory/logs/` and reply inline), and a fallback "unknown command" response.
2. Rate-limit dispatch to prevent runaway triggers: max 3 skill dispatches per poll cycle, skip if the same skill was dispatched in the last 30 minutes (check last workflow run timestamp via `gh run list`). Log each dispatch to `memory/logs/` with the source channel and command text.
3. Add a `commands:` section to `aeon.yml` (opt-in, disabled by default) listing enabled command aliases. Include a "Commands" card in the dashboard Settings panel showing the current alias table and last 5 dispatched commands.

---

### 4. Cross-Fork Skill Customization Digest
**Type:** Community
**Effort:** Small (hours)
**Impact:** The fork-fleet skill already scans 26 active forks for enabled skills and skill counts. The next level — what operators actually *change* in their skill configs (different `var`, different schedule, added custom skills) — is unread signal for upstream priorities. A weekly `fork-diff` skill that diffs each fork's `aeon.yml` against upstream and surfaces the 10 most-customized skills (by count of distinct var values or schedule overrides) answers the question "what do operators actually want?" without requiring anyone to file an issue. This is a community feedback loop that scales automatically with the fork fleet.
**How:**
1. Create `skills/fork-diff/SKILL.md` as a weekly skill (Sunday, after `fork-fleet`). It fetches each active fork's `aeon.yml` via `gh api repos/{fork}/contents/aeon.yml`, parses the skills list, and diffs against the upstream `aeon.yml` on three axes: skills enabled in fork but not upstream (custom skills), skills with a non-default `var` value, skills with a non-default schedule.
2. Aggregate across all forks: for each skill, count how many forks have customized it and what the most common custom var values are. Output a ranked table of "Top 10 Customized Skills" with representative var values anonymized to show patterns without exposing individual operator configs.
3. Send the weekly digest via `./notify` and write to `articles/fork-diff-<date>.md`. Log key insights (e.g. "18/26 forks run token-report with custom contract address") to `memory/topics/fork-customization.md` for the feature skill to use as upstream roadmap signal.

---

### 5. Smithery / MCP Directory Submission
**Type:** Growth
**Effort:** Small (hours)
**Impact:** Aeon's MCP adaptor exposes 93 skills as `aeon-*` tools compatible with Claude Desktop, Claude Code, and any MCP-compliant client. Smithery.ai is the primary MCP server directory — listing there puts Aeon in front of every developer searching for "GitHub agent", "crypto monitor", or "research digest" MCP tools. At 198 stars and with a working `npx @json-render/mcp` install path, the adaptor is ready to list. A submission script plus a periodic `smithery-health` check (does the listing still appear? is the install command valid?) closes the gap between "built the tool" and "the ecosystem knows it exists." Even 50 new installs from directory traffic would double the active user base.
**How:**
1. Create `scripts/submit-smithery.sh` that generates a valid `smithery.yaml` manifest (name, description, install command, capabilities list, category tags) from the existing MCP adaptor config and submits it to the Smithery API (or outputs the manifest for manual upload if the API requires OAuth). Also generate an `anthropic-plugin.json` for the Anthropic plugin directory using the same source data.
2. Create `skills/smithery-health/SKILL.md` — a weekly skill that fetches the Smithery listing page for `aeon-mcp` (via WebFetch), checks that the listing exists and the install command is current, and alerts via `./notify` if the listing is stale, missing, or showing an old version. Also checks the GitHub star count to correlate directory traffic with growth events.
3. Add a "Listed on Smithery" badge to the README (alongside the existing GitHub badges) once the listing is live — social proof for new visitors who find Aeon via organic search.
