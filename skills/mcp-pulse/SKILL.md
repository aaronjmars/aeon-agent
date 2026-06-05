---
name: mcp-pulse
description: Weekly tracker for the Model Context Protocol (MCP) ecosystem — new server implementations, adoption velocity, npm/GitHub signals, and protocol evolution. Thesis check — is MCP becoming the default tool-call rail for agents?
schedule: "0 10 * * 5"
commits: true
permissions:
  - contents:write
tags: [AI, MCP, agent-infra]
---
<!--
  Verbatim backport of upstream aeon `skills/mcp-pulse/SKILL.md`
  (originally shipped as part of upstream aeon PR #272, merged 2026-05-29 —
  the same general-ops batch as spend-monitor [aeon-agent PR #74, Jun-01],
  follow-up-patrol [aeon-agent PR #76, Jun-02], and narrative-convergence
  [aeon-agent PR #80, Jun-04]).

  PR #272 backport queue: spend-monitor + follow-up-patrol +
  narrative-convergence done; mcp-pulse (this PR) leaves only
  fleet-scorecard remaining (which depends on memory/instances.json +
  scripts/prefetch-fleet-scorecard.sh that aeon-agent does not currently
  maintain).

  Three adaptations vs upstream:
    (1) `./notify` call style: upstream uses `./notify -f .pending-notify-temp/<file>`,
        aeon-agent's `./notify` reads its argument as a single positional `$1`
        (confirmed in CLAUDE.md and the dynamically-generated notify script
        at workflow setup: `cat > ./notify` → `MSG="$1"` — same constraint
        that drove the spend-monitor, follow-up-patrol, and
        narrative-convergence adaptations). Step 8 rewrites the call as
        `./notify "$(cat .pending-notify-temp/<file>)"` — same temp-file
        contents, same gating, same body, single argv.

    (2) `$(date ...)` shell-substitution at step 3 (upstream line ~86)
        is replaced with a literal ISO cutoff the run computes from the
        injected `${today}` (write `${today}` minus 7 days as a literal
        date — there is no `${today_minus_7}` template var). The runner hook
        blocks `$(...)`/`$VAR` ("Contains simple_expansion") on aeon-agent —
        same fix applied in weekly-shiplog (PR #63), push-recap (PR #67),
        heartbeat (PR #71), repo-pulse (PR #77), and repo-article (PR #81).
        The semantic trade
        (exact 7×24h ago → midnight UTC of 7 days ago) is fine: this is a
        7-day momentum window for ecosystem signals, not a precision filter.

    (3) WebFetch fallback explicitly added on every external endpoint
        (npm registry, PyPI stats, GitHub API). On aeon-agent the sandbox
        blocks outbound curl from skill bash intermittently — WebFetch
        bypasses it per CLAUDE.md pattern 1. Upstream already calls this
        out under "Sandbox Note" but the skill body itself only mentions
        WebFetch for a couple of paths; this backport hardens the fallback
        across all external calls so the skill degrades gracefully on a
        sandboxed run.

  Source upstream commit: upstream `main` at the time of backport.
-->

Today is ${today}. Read `memory/MEMORY.md` before starting.

## Voice

If `soul/SOUL.md` and `soul/STYLE.md` exist and are populated, read them and match the operator's voice in the notification. Otherwise use a clear, direct, neutral tone — punchy, position-first, no fluff.

## Why this skill exists

MCP (Model Context Protocol) standardizes how agents make tool calls to external services — the way HTTP standardized transport. The bet: MCP becomes the default protocol layer connecting agents to every external service, and whoever controls the server-generation tooling controls the integration layer (Anthropic authored the spec and, via its 5/18/2026 Stainless acquisition, now owns SDK/server generation tooling too). For any agent framework, this is the single most load-bearing infra track. This skill tracks whether the thesis is advancing: new server implementations, adoption velocity, notable integrations, and ecosystem health.

## Steps

### 1. Load current context

Read:
- `memory/MEMORY.md` — overall ecosystem context and last-known MCP stats
- `memory/topics/mcp-ecosystem.md` — MCP-specific baseline (create with seed if missing — see end of this section)

Extract from the topic file:
- `npm_last_known` — last recorded `@modelcontextprotocol/sdk` weekly downloads
- `gh_repo_count_last` — last recorded count of MCP-related GitHub repos
- `known_servers` — list of known major MCP server implementations
- `last_run` — date of prior run

If `memory/topics/mcp-ecosystem.md` doesn't exist, create it:

```markdown
# MCP Ecosystem Tracker

*Last run: never*

## Seed Context (2026-05-18)
- Stainless acquired by Anthropic ~$300M+ (The Information, 5/18/2026). Stainless team now building MCP server generation tooling inside Anthropic. Previously generated SDKs for: OpenAI, Google, Cloudflare, Meta, Runway, Groq, Cerebras, Modern Treasury, and all official Anthropic SDKs.
- MCP (Model Context Protocol): open protocol Anthropic authored. Standardizes how agents make tool calls to external services. GitHub: modelcontextprotocol/modelcontextprotocol.
- Thesis: MCP becomes the default tool-call rail for agents. Anthropic owns the generation layer → controls the integration layer.

## Known Servers
- Official: filesystem, git, github, gitlab, google-maps, google-drive, postgres, sqlite, slack, brave-search, puppeteer, fetch, memory, sentry, time, sequential-thinking, everything (test server)
- Third-party high-quality: (populate from first run)

## Key Stats
- npm @modelcontextprotocol/sdk: unknown weekly downloads
- GitHub repos with MCP topic: unknown
- modelcontextprotocol org repos: unknown count

## Signal Log
- 2026-05-18: Anthropic acquires Stainless. Stainless team pointed at MCP server generation.
```

### 2. Check the modelcontextprotocol GitHub org

Fetch the list of repos in the `modelcontextprotocol` org:

```bash
gh api "orgs/modelcontextprotocol/repos?sort=updated&per_page=50" \
  --jq '.[] | {name, description, stargazers_count, updated_at, topics}'
```

From results:
- Note any repos created or updated in the last 7 days
- Record total org repo count (compare to `gh_repo_count_last` if it tracked org size)
- Flag new repos not seen before — these are official server or tooling additions
- Note star counts for `modelcontextprotocol/modelcontextprotocol`, `modelcontextprotocol/python-sdk`, `modelcontextprotocol/typescript-sdk`

If `gh api` fails, fall back to WebFetch:
```
https://api.github.com/orgs/modelcontextprotocol/repos?sort=updated&per_page=50
```

### 3. Search GitHub for new MCP server repos

**Compute the cutoff (`CUTOFF`) FIRST — this is critical.** The runner hook on aeon-agent blocks shell command/variable expansion (`$(...)`, `$VAR`) — do **not** use `$(date ...)`, and do **not** rely on an injected `${today_minus_7}` (no such variable exists). Instead, set `CUTOFF` to a literal ISO timestamp you compute from the injected `${today}` (UTC `YYYY-MM-DD`) minus 7 days — e.g. if today is `2026-06-04`, write `CUTOFF=2026-05-28T00:00:00Z`. Substitute the real date into the `YYYY-MM-DD` placeholder below **before running anything else** — never leave `YYYY-MM-DD` literal, or the search silently returns zero repos. This matches the pattern weekly-shiplog (PR #63), push-recap (PR #67), heartbeat (PR #71), repo-pulse (PR #77), and repo-article (PR #81) use for the same reason:

```bash
# Cutoff = midnight UTC of 7 days ago, computed from ${today} as a LITERAL
# (NOT $(date ...), NOT an injected var). Substitute the real date into
# YYYY-MM-DD before running — never leave it literal, or the jq filter below
# returns nothing. The semantic window is "updated since midnight UTC of 7
# days ago" (10-34h slightly wider than a strict 7×24h on a 10:00 UTC run);
# the same trade weekly-shiplog/push-recap/heartbeat/repo-pulse/repo-article
# accepted. The momentum scoring in step 6 is unaffected by the small overlap.
CUTOFF=YYYY-MM-DDT00:00:00Z

gh api "search/repositories?q=mcp-server+in:topics+OR+mcp-server+in:description&sort=updated&per_page=30" \
  --jq ".items[] | select(.updated_at > \"${CUTOFF}\") | {full_name, description, stargazers_count, updated_at, topics}"
```

Also search:
```bash
gh api "search/repositories?q=model-context-protocol+in:topics+OR+modelcontextprotocol+in:description&sort=updated&per_page=20" \
  --jq '.items[] | {full_name, description, stargazers_count, updated_at}'
```

If `gh api` fails, fall back to WebSearch: `"mcp-server" site:github.com after:YYYY-MM-DD` (use the same literal date as `CUTOFF` above — `${today}` minus 7 days)

From results:
- Filter to repos updated since the cutoff date — 7 days before `${today}` (in-jq filter above)
- Cross-check against `known_servers` — flag NEW implementations
- Note the service being wrapped (Stripe, Notion, Linear, Jira, etc.)
- Rank by stars descending

High-signal repo patterns to watch:
- Official company MCP servers (Stripe, Notion, Linear, Atlassian, etc.)
- Repos from major infrastructure players (AWS, GCP, Azure)
- Servers for high-demand services (databases, payments, CRMs, dev tools)
- Repos with 50+ stars — threshold for "real usage" signal

### 4. Fetch npm download trend

Use WebFetch (NOT curl — sandbox may block outbound HTTPS for npm):
```
https://api.npmjs.org/downloads/point/last-week/@modelcontextprotocol/sdk
```

Record `npm_weekly_downloads`. Compute delta vs `npm_last_known` if available. If 403 or no data, try:
```
https://www.npmjs.com/package/@modelcontextprotocol/sdk
```

Also check the Python SDK (WebFetch — same sandbox reasoning):
```
https://pypistats.org/api/packages/mcp/recent?period=week
```

If both fail, note in the log and skip the npm delta (the rest of the run still produces a useful digest — the npm delta is one of seven signal columns, not the floor).

### 5. WebSearch for MCP news this week

Run these searches:
```
WebSearch: "model context protocol MCP server release ${year}"
WebSearch: "MCP server anthropic stainless ${year}"
WebSearch: '"model context protocol" integration announcement ${year}'
```

From results:
- New official server launches (a company publishing its own MCP server)
- Protocol spec updates or new versions
- Stainless/Anthropic news on MCP server generation progress
- Developer tutorials/blog posts showing real implementations
- Enterprise adoptions (a Fortune 500 shipping an MCP server = high signal)

Flag any result from the last 7 days. Discard opinion/speculative pieces — keep launches, integrations, official announcements.

### 6. Synthesize momentum score

Rate ecosystem velocity this week:

| Signal | Points |
|--------|--------|
| New MCP server from a named company (Stripe, Notion, Linear, etc.) | +3 each |
| New MCP server repo with 50+ stars updated this week, not in baseline | +2 each |
| npm @modelcontextprotocol/sdk downloads up vs last known | +3 |
| New official modelcontextprotocol org repo | +2 each |
| Stainless/Anthropic MCP-related announcement | +3 |
| Notable blog post or tutorial (real implementation, not vaporware) | +1 each |
| MCP mentioned in mainstream dev context (HN, major tech blog) | +1 |

**Momentum levels:**
- 0–2: quiet week
- 3–6: building
- 7–10: accelerating
- 11+: breakout

**Thesis check:** After reviewing all data, answer in one sentence:
> **Thesis check:** MCP-as-default-tool-call-rail thesis [advancing / holding / stalling / reversing] — [one concrete data point].

### 7. Update memory/topics/mcp-ecosystem.md

Rewrite with:
- Updated `*Last run: ${today}*`
- Updated `Known Servers` list (add newly discovered)
- Updated `npm_last_known` with this week's count
- Updated `gh_repo_count_last` with current count
- Appended entry to `Signal Log`:
  ```
  - ${today}: [N new repos] / npm [downloads]/wk / momentum: [level] / [top signal]
  ```

### 8. Send notification

Write to `.pending-notify-temp/mcp-pulse-${today}.md` (create the dir if needed), then send via the aeon-agent positional-arg notify style:

```bash
mkdir -p .pending-notify-temp
# ... write the message body to .pending-notify-temp/mcp-pulse-${today}.md ...
./notify "$(cat .pending-notify-temp/mcp-pulse-${today}.md)"
```

aeon-agent's `./notify` reads its argument as `$1` (single positional, multiline-safe) — the same adaptation used by spend-monitor, follow-up-patrol, and narrative-convergence backports. The temp file is kept so the article surface still has a permanent on-disk record of what was sent.

**Format — match the operator's voice if soul files are populated, otherwise direct and neutral:**

```
mcp pulse — ${today}

momentum: {level} ({score} pts)

{IF new company servers}
new official servers ({count}):
- {company}: {service_described_one_line} ({stars}★)
{end}

{IF new repos}
new implementations ({count}):
- {full_name}: {description_one_line} ({stars}★)   [top 3]
{end}

{IF npm_delta known}
npm @modelcontextprotocol/sdk: {downloads}/wk ({delta:+N vs last week} or "first data point")
{end}

{IF notable news}
signals:
- {one-line summary}   [top 2]
{end}

thesis: {advancing/holding/stalling/reversing} — {one data point}

{IF quiet_week}
quiet week. ecosystem still compounding.
{end}
```

Keep total under 900 chars.

If momentum score is 0 and no new repos and no news: log `MCP_PULSE_OK: quiet` and skip notification.

### 9. Log to memory/logs/${today}.md

Append:
```markdown
## MCP Pulse
- **New repos (7d):** {count}
- **New company servers:** {count} ({names if any})
- **npm @modelcontextprotocol/sdk:** {downloads}/wk (delta: {delta})
- **Momentum score:** {score} ({level})
- **Thesis:** {advancing/holding/stalling/reversing} — {data point}
- **Notification:** sent / skipped (quiet)
- MCP_PULSE_OK
```

## Required Env Vars

None. Uses `gh` CLI (GITHUB_TOKEN via workflow), WebFetch, WebSearch. No additional auth needed.

## Sandbox Note

- `gh api` and `gh search` use gh CLI — handles auth internally, no env-var expansion in headers (CLAUDE.md sandbox pattern 2c).
- npm API (`api.npmjs.org`), PyPI stats (`pypistats.org`), and GitHub API fallbacks: use **WebFetch**, not curl. The sandbox may block outbound HTTPS from bash; WebFetch bypasses the sandbox per CLAUDE.md pattern 1.
- WebSearch: built-in tool, always available.
- `$(date ...)` shell substitution is blocked by the runner hook — every date computation in this skill is a literal the run derives from the injected `${today}` template variable (the 7-day cutoff = `${today}` minus 7 days, written as a literal ISO timestamp; there is no `${today_minus_7}` injected var).
- `./notify` reads its message as a single positional `$1` — pass the full body via `./notify "$(cat .pending-notify-temp/mcp-pulse-${today}.md)"`, not `-f file`.

## What to watch for (recurring signal classes)

- **Official company MCP servers** — Stripe, Notion, Linear, Atlassian, Salesforce, GitHub, Slack, Jira publishing their own MCP servers = protocol hitting mainstream.
- **Stainless/Anthropic server generation updates** — when the generation tooling ships, expect a spike in server-count that's automated rather than organic. That inflection point is the key event to catch.
- **npm download velocity** — `@modelcontextprotocol/sdk` installs measure developer adoption, more reliable than announcements.
- **Enterprise adoptions** — a Fortune 500 shipping an MCP server for internal use = institutional lock-in signal.
- **Protocol spec versions** — breaking changes or new capabilities (multi-step tool calls, resource subscriptions) that shift what agents can do.
- **Non-Anthropic framework integrations** — LangChain, AutoGen, LlamaIndex, CrewAI adopting MCP = protocol winning the inter-framework standard war.

## Output feeds

- `article` skill — MCP Pulse data feeds infrastructure/agent-tools articles
- `narrative-convergence` — MCP signal lane in the operator-editable category map (`memory/topics/signal-categories.md`) once the operator opts in
- `digest` — MCP developments slot into the agent-infra section
