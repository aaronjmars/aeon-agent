# Repo Action Ideas — 2026-04-10

**Repo:** [aaronjmars/aeon](https://github.com/aaronjmars/aeon) + [aaronjmars/aeon-agent](https://github.com/aaronjmars/aeon-agent)
**Stars:** 151 (aeon) / 7 (aeon-agent) | **Forks:** 16 / 0 | **Language:** TypeScript | **Open Issues:** 0 / 0
**Contributors:** aaronjmars (187), Aeon (5), aeonframework (4), github-actions[bot] (3)
**Open PRs:** [#28 MCP Skill Adaptor](https://github.com/aaronjmars/aeon/pull/28)

Aeon has reached 151 stars and 68 skill directories — a substantial jump from the 54 in skills.json. The past two weeks have been the most productive in the project's history: skill-chaining, spawn-instance, fleet-control, auto-workflow, create-skill, autoresearch, skill-quality-metrics, distribute-tokens, bankr-gateway, treasury-info, cost-report, skill-evals, and fork-fleet were all merged. The MCP Skill Adaptor (PR #28) is open and about to unlock Claude Desktop as a distribution surface.

Previous runs (Mar 25–Apr 9) generated 45+ ideas and built: skill forking, RSS feed, skill security scanner, autonomous skill discovery, GitHub Pages gallery, deep research, skill smoke tests, cost-report, fork-fleet, skill-evals, MCP adaptor. Unbuilt from earlier ideation: **Workflow Security Audit**, **Dashboard Live Feed**, **Skill Dependency Chain**, **Memory Search API**, **A2A Gateway**.

This run focuses on what comes after the MCP moment: security hardening the expanded surface, opening Aeon to the broader AI agent ecosystem, making multi-instance operation visible, and growing the community through skill discovery and a wider notification reach.

---

### 1. Workflow Security Audit — Harden .github/workflows Before the Fleet Scales

**Type:** Security
**Effort:** Small (hours)
**Impact:** Aeon's skill security scanner (PR #5, merged) audits *imported* SKILL.md files for prompt injection. But the `.github/workflows/` directory itself remains unaudited — and it has grown significantly: aeon.yml now runs 68 skills, messages.yml polls Telegram/Discord/Slack, fleet-control and spawn-instance coordinate multi-agent execution, and distribute-tokens moves on-chain assets. Each new surface is a potential injection point. Common GitHub Actions vulnerabilities — interpolating `${{ github.event.* }}` directly in `run:` blocks, `permissions: write-all` on jobs that need read-only, unverified third-party actions at branch refs — could let an attacker hijack the GitHub token, exfiltrate secrets, or push malicious commits. With 16 forks copying the same aeon.yml patterns, a single unaddressed vulnerability propagates to the fleet. A one-time audit skill surfaces and auto-fixes these before the MCP adaptor (PR #28) expands the execution surface further.

**How:**
1. Create `skills/workflow-security-audit/SKILL.md` that reads every `.yml` file in `.github/workflows/` and checks for: (a) script injection — `${{ github.event.* }}` or `${{ inputs.* }}` used directly in `run:` blocks without intermediary env var assignment; (b) overly broad permissions — `permissions: write-all` or `contents: write` on jobs that only need `contents: read`; (c) unverified third-party actions — `uses: owner/action@branch` instead of `@sha`; (d) secret exposure — `echo ${{ secrets.* }}` in `run:` blocks; (e) fleet-specific risks — spawn-instance or fleet-control jobs that pass unvalidated user inputs.
2. For each finding, generate a concrete fix: replace direct interpolation with `env:` assignment, scope permissions to minimum required (check actual API calls made in each job), pin actions to their current commit SHAs. For critical findings, open a PR with fixes applied automatically.
3. Output a report to `articles/workflow-security-audit-{date}.md` with severity (critical/high/medium), exact file and line references, and a fix status (auto-fixed / manual required). Send notification with finding count and highest-severity issue found.

---

### 2. A2A Protocol Gateway — Open Aeon to Any AI Agent Framework

**Type:** Integration
**Effort:** Medium (1-2 days)
**Impact:** The MCP adaptor (PR #28) exposes Aeon skills to Claude Desktop users. But MCP is Claude-specific. Google's Agent-to-Agent (A2A) protocol — published in April 2025 and now supported by OpenAI Agents SDK, LangChain, AutoGen, CrewAI, and Vertex AI — is the emerging standard for *framework-agnostic* agent interoperability. An A2A gateway would let any compliant agent (GPT-4 via OpenAI Agents, Gemini via Vertex, a LangChain workflow) invoke Aeon skills by POSTing to a `/tasks/send` endpoint. Where MCP requires Claude, A2A requires nothing specific — it's just HTTP. With 16 forks and 68 skills, Aeon is now substantial enough to be a useful "background intelligence" module that other agents delegate to. A research pipeline could call `aeon:deep-research`, a trading bot could call `aeon:token-report`, a content scheduler could call `aeon:article`. This is the natural complement to MCP: same skills, double the addressable agent ecosystem.

**How:**
1. Create `a2a-server/` directory with a minimal A2A-compliant server in TypeScript. Implement the A2A `agent-card` endpoint (`GET /.well-known/agent.json`) that advertises all 68 Aeon skills as callable tasks with their input schemas (`var` string parameter). Implement `POST /tasks/send` to receive an A2A task payload, map it to the corresponding SKILL.md, and invoke the skill locally via `claude` CLI.
2. Implement the A2A `tasks/get` polling endpoint so calling agents can check task status and retrieve output. Each skill invocation writes its output to `articles/{skill}-{date}.md` — the A2A response body is this file's content. Support SSE streaming via `tasks/sendSubscribe` for long-running skills like `deep-research`.
3. Add `./add-a2a` install script (parallel to `./add-mcp`) that starts the A2A server and optionally deploys it to a public endpoint (Cloudflare Workers or fly.io) for remote access. Update README with "Use with any AI agent" section. Submit to the [A2A protocol directory](https://github.com/google-a2a/A2A).

---

### 3. Dashboard Live Feed — Real-Time Skill Run Visibility

**Type:** Feature / DX
**Effort:** Medium (1-2 days)
**Impact:** The dashboard has a Hyperstitions/Evangelion aesthetic and per-skill analytics — but it's entirely historical. When a skill is running *right now* (fleet-control spawning instances, deep-research pulling 50 sources, MCP adaptor responding to a Claude query), the dashboard is silent until the output file lands. With fleet-control and spawn-instance enabling concurrent multi-skill runs, and the MCP adaptor adding externally-triggered invocations, the gap between "what's running?" and "what can I see?" is widening. A live feed closes this by showing: which skills are currently executing, elapsed time, the last few log lines, and recent completions with preview text. This transforms the dashboard from a skill gallery into an operational control plane — and gives new users immediate confirmation that their setup works without requiring them to open GitHub Actions. The file-based json-render infrastructure (`dashboard/outputs/`) is already in place; this extends it with running-state stubs.

**How:**
1. Create `dashboard/components/live-feed/` component that polls `dashboard/outputs/` every 30 seconds for JSON files. Add a `./notify-running "skill-name"` script that writes a minimal running-state stub to `dashboard/outputs/{skill}-running.json` (`{status: "running", skill, started_at, pid}`). The scheduler calls this at invocation start; `./notify` overwrites it on completion.
2. The live feed component distinguishes "running" stubs (amber dot, elapsed time counter, last log line from `memory/logs/today.md`) from "completed" entries (green dot, duration, output preview). Display the last 10 events — mix of running and completed — as a sidebar panel in the dashboard layout.
3. Wire a "Skills running: N" badge into the dashboard header. Add a "Trigger skill" button per running entry that opens the workflow_dispatch UI for that skill. For MCP-triggered runs, show the invoking agent name in the feed entry (passed via a `$AEON_CALLER` env var set by the MCP server).

---

### 4. Skill Analytics Leaderboard — Surface the Most Popular Skills Across All Forks

**Type:** Community / Growth
**Effort:** Small (hours)
**Impact:** Aeon has 16 forks — each running some subset of the 68 skills. Right now, fork data exists (fork-fleet inventories it weekly) but there's no aggregated view of which skills are most commonly enabled across the fleet. A leaderboard would: read each active fork's `aeon.yml` to detect enabled skills, aggregate across all forks, and publish a ranked "Top 10 skills in the wild" list. This creates a discovery signal that benefits three audiences: new users (see which skills others find valuable), skill authors (see adoption of skills they built), and the project (a "trending skills" widget on GitHub Pages or the README drives attention to popular capabilities). The data is already accessible via `gh api repos/{fork}/contents/aeon.yml` — fork-fleet already fetches fork metadata. The leaderboard is a lightweight aggregation layer on top of existing infrastructure.

**How:**
1. Create `skills/skill-leaderboard/SKILL.md` that: fetches all active forks via `gh api repos/aaronjmars/aeon/forks` (filtered to pushed_at within 30 days), reads each fork's `aeon.yml` via `gh api repos/{fork}/contents/aeon.yml`, extracts all skill entries where `enabled: true`, and aggregates counts across all forks.
2. Rank skills by fork-enable frequency. Output a table: skill name, enable count, percentage of forks, category, and a "trend" column (compare to last week's leaderboard output if it exists in `articles/`). Identify any skills enabled in >50% of forks (consensus skills) and any skills with zero fork enables (adoption gap candidates for documentation improvement).
3. Write to `articles/skill-leaderboard-{date}.md` and update the GitHub Pages gallery (`docs/_posts/`) so the leaderboard appears as a browsable post. Add a `## Community Picks` section to the README that auto-updates weekly by reading the latest leaderboard article. Send notification with the top 5 skills and the week-over-week change.

---

### 5. Email Notification Channel — Reach Users Beyond Messaging Apps

**Type:** Integration
**Effort:** Small (hours)
**Impact:** Aeon currently notifies via Telegram, Discord, and Slack — all real-time messaging apps. A meaningful segment of potential users (and all corporate environments) prefer or require email. Adding SMTP/SendGrid as a fourth notification channel would: unblock users in environments that don't allow Telegram bots or Discord webhooks, enable digest-style emails (one email per skill run with full article content, not just a summary), and expand the addressable install base to everyone with an email address. The `./notify` fan-out architecture already handles multiple channels gracefully — adding email is a new channel implementation, not an architectural change. SendGrid's free tier (100 emails/day) covers Aeon's typical usage. The only required secrets are `SENDGRID_API_KEY` and `NOTIFY_EMAIL_TO` — two env vars, consistent with how Telegram and Discord channels work.

**How:**
1. Add `notify-email` to the `./notify` fan-out script: if `SENDGRID_API_KEY` and `NOTIFY_EMAIL_TO` are set, POST the message to `https://api.sendgrid.com/v3/mail/send` with the skill output as the email body. Support HTML rendering: convert the markdown notification to HTML using a minimal template (skill name as subject, markdown body rendered to HTML, Aeon logo as header image).
2. Add `NOTIFY_EMAIL_FROM` (default: `aeon@notifications.aaronjmars.com`) and `NOTIFY_EMAIL_SUBJECT_PREFIX` (default: `[Aeon]`) as optional config vars. For skills that write full articles (`article`, `deep-research`, `digest`), attach the full markdown file as a `.md` attachment alongside the summary body.
3. Update the `./aeon` local dashboard to include an Email setup tab (alongside the existing Telegram/Discord/Slack tabs): input field for recipient email, SendGrid API key, and a "Send test email" button that triggers a sample notification. Document in the README's Notifications section with the same table format as existing channels.

---

## Summary

These 5 ideas reflect Aeon's current inflection point: 68 skills and 16 forks is fleet scale, not prototype scale. Workflow Security Audit hardens the expanded attack surface before it compounds further. The A2A Gateway doubles the addressable agent ecosystem beyond Claude Desktop to every A2A-compatible framework. The Dashboard Live Feed makes multi-agent, multi-trigger operation visible without requiring GitHub Actions access. The Skill Analytics Leaderboard turns fork data into community discovery and gives adoption signals back to skill builders. Email channel expansion reaches the large segment of users for whom Telegram and Discord aren't options. All five are scoped for autonomous `feature` skill implementation — clear inputs, outputs, no external approvals, no ambiguous design decisions — and can be completed within 1-3 days of focused work.
