# Repo Action Ideas — 2026-03-30

**Repo:** [aaronjmars/aeon](https://github.com/aaronjmars/aeon) + [aaronjmars/aeon-agent](https://github.com/aaronjmars/aeon-agent)
**Stars:** 134 (aeon) / 4 (aeon-agent) | **Forks:** 15 / 0 | **Language:** TypeScript | **Open Issues:** 4 / 4
**Contributors:** aaronjmars (132 commits), github-actions[bot] (50), Aeon (15)

Aeon is at 134 stars with 47+ skills, 4 open PRs on each repo. The past week produced 80+ commits on aeon-agent alone — articles, daily token reports, push recaps, tweet monitoring, and self-improvement cycles. The self-improve skill is pacing itself with a PR pile-up guard (stops at 3+ open PRs). Seven previous repo-actions runs have generated 35 ideas, of which several have shipped (skill forking, RSS feed, per-skill models, PR awareness guard). This run focuses on the security gap exposed by the SkillsMP/ClawHub ecosystem, leveraging the 1M context window for deep research, automated skill discovery, fork fleet coordination, and a public showcase site.

## Ecosystem Context (March 30, 2026)

- **SkillsMP hit 351K skills; security is the elephant in the room** — A 2026 CData audit found 82% of MCP servers vulnerable to path traversal and 67% to code injection. CVE-2026-25253 enabled RCE via malicious skills on ClawHub. Aeon imports external skills via `add-skill` but has no scanning or sandboxing for imported content. As the skill ecosystem explodes, trust infrastructure becomes a differentiator. ([source](https://smartscope.blog/en/blog/skillsmp-marketplace-guide/))
- **Anthropic measures agent autonomy doubling** — Among longest-running Claude Code sessions, autonomous work time nearly doubled in 3 months (25 min to 45+ min). Experienced users auto-approve more but interrupt more often — a "trust but verify" pattern. Aeon's cron-scheduled, fire-and-forget model already operates at the far end of this spectrum. ([source](https://www.anthropic.com/research/measuring-agent-autonomy))
- **$4.2B in Q1 2026 VC funding for agent startups** — Walmart deploying CrewAI for supply chain, JPMorgan running 200+ specialized agents. Enterprise is no longer experimenting — it's deploying. Aeon's GitHub Actions model is uniquely positioned for enterprise: no infra to manage, auditable via git, and already runs on infrastructure every company has. ([source](https://moltbook-ai.com/posts/ai-agents-march-2026-roundup))
- **Claude Opus 4.6 ships with 1M token context** — Long-horizon agentic tasks are now practical in a single session. Aeon's research skills currently operate within default context limits; a long-form research mode could ingest entire codebases, paper collections, or market datasets in one pass. ([source](https://moltbook-ai.com/posts/ai-agents-march-2026-roundup))
- **75% developer adoption of Claude Code at SMBs** — Claude Code overtook GitHub Copilot as the primary dev tool. Anthropic at $14B ARR with Claude Code accounting for $2.5B. The addressable market for Aeon-style background agents running inside this ecosystem is massive. ([source](https://tech-now.io/en/blogs/claude-code-openclaw-the-rise-of-agentic-ai-in-software-development-2026))

Previous runs (Mar 25–29) generated 35 ideas covering: plugin registration, skill DAG, community validation, state snapshots, Telegram control plane, skill evals, awesome-list, agentic workflow templates, SkillsMP publish, A/B testing, cost tracker, security audit, live feed, dependency chains, memory search, A2A gateway, OTEL tracing, Agent SDK runner, autonomy levels, context budgets, multi-model routing, skill forking, webhook triggers, reputation dashboard, Telegram skill store, MCP adaptor, skill smoke tests, onboarding wizard, RSS feed, skill metrics, Claude Code plugin package, Skills.sh listing, GitHub agentic workflows native mode, skill monetization, and skill versioning/sync. The following 5 ideas are entirely new.

---

### 1. Skill Security Scanner — Audit Imported Skills Before They Run

**Type:** Security
**Effort:** Medium (1-2 days)
**Impact:** The SkillsMP ecosystem just crossed 351K skills, but a CData audit revealed 82% of MCP servers are vulnerable to path traversal and 67% to code injection — and CVE-2026-25253 proved malicious skills can achieve RCE. Aeon's `add-skill` command imports external SKILL.md files directly from GitHub repos with no validation beyond format checking. A single malicious skill could exfiltrate secrets, modify other skills, or use `./notify` to send data to attacker-controlled channels. Building a security scanner that runs before any imported skill executes would make Aeon the first agent framework with built-in skill supply chain security. This is different from the "security audit" idea (run 3, Mar 27) which was about auditing the repo's own security posture — this is about vetting external skills at the import boundary, the way npm audit checks dependencies.

**How:**
1. Create `skills/skill-security-scan/SKILL.md` that analyzes any SKILL.md file for: shell injection patterns (unquoted `$var` in bash blocks, `eval`, backtick execution), secret exfiltration (curl/wget to non-allowlisted URLs, piping env vars to external commands), path traversal (`../` references, absolute paths outside the repo), and prompt injection (instructions that override CLAUDE.md rules or reference "ignore previous instructions").
2. Integrate into the `add-skill` workflow: before committing an imported skill, run the scanner. If any high-severity issue is found, reject the import and log the reason. Medium-severity issues get flagged in the commit message for human review.
3. Create an allowlist file (`skills/security/trusted-sources.txt`) listing verified GitHub orgs/repos whose skills skip the full scan (still get basic format validation). Add a `--force` flag for advanced users who want to import flagged skills with an explicit risk acknowledgment logged to `memory/logs/`.

---

### 2. Autonomous Skill Discovery — Auto-Import Trending Skills That Fill Gaps

**Type:** Feature / Growth
**Effort:** Medium (1-2 days)
**Impact:** Aeon has 47+ hand-built skills, but the SkillsMP registry now has 351K indexed skills via AI-powered semantic search. Skills.sh and LobeHub add thousands more. Rather than manually browsing these registries, a discovery skill could automatically search for skills that complement Aeon's existing catalog — filling gaps in coverage, finding better implementations of existing capabilities, or discovering entirely new categories. This turns Aeon from a closed skill set into a self-expanding agent that gets more capable over time by importing from the ecosystem. Combined with the security scanner (idea #1), this creates a safe pipeline: discover, scan, import, test, and optionally propose via PR. No other agent framework has this autonomous skill acquisition loop.

**How:**
1. Create `skills/skill-discover/SKILL.md` that: reads `skills.json` to understand what Aeon already has, queries SkillsMP's API (or scrapes the registry) for the top 50 trending skills by category (research, dev-tools, crypto, productivity), and identifies 3-5 skills that either fill a gap (Aeon has no Slack-native skills, no CI/CD monitoring, no calendar integration) or improve on existing ones (a better paper search, a more efficient digest format).
2. For each candidate, run the security scanner (idea #1), check compatibility (does it use `./notify`? does it need secrets Aeon doesn't have?), and generate a one-paragraph assessment: what it does, why it's useful, and what would need to change to work in Aeon's environment.
3. Output a ranked list to `articles/skill-discovery-{date}.md` and send a notification with the top 3. If `--auto-import` is set, create a PR for the top-ranked skill that passes security scanning. Schedule weekly to keep the catalog fresh.

---

### 3. GitHub Pages Skill Gallery — A Public Showcase of What Aeon Produces

**Type:** Community / Growth
**Effort:** Medium (1-2 days)
**Impact:** Aeon generates daily articles, token reports, market digests, push recaps, and research briefs — but all of this output is buried in a git repo's `articles/` directory. The Telegram channel reaches existing followers, but there's no public-facing showcase for potential users to browse and evaluate. A GitHub Pages site that renders Aeon's output as a clean, browsable gallery would serve as both a marketing site and a proof-of-capability. Visitors could see real outputs from each skill, not just descriptions — answering "what does this agent actually produce?" A gallery also enables SEO: each article becomes an indexed page that drives organic traffic to the repo. With 134 stars and 15 forks, Aeon needs a discovery mechanism beyond GitHub search and word-of-mouth.

**How:**
1. Create a `docs/` directory with a minimal static site generator (Jekyll, which GitHub Pages supports natively). Configure `_config.yml` to read from `articles/` as the posts directory, with frontmatter extraction for title, date, and skill-name.
2. Build an index page that groups outputs by skill type (Research, Dev, Crypto, Meta) with the most recent output from each skill shown as a card with title, date, first paragraph, and a "Read full output" link. Add a sidebar listing all 47 skills with descriptions and sample output links.
3. Create a `skills/update-gallery/SKILL.md` that runs after content-generating skills, regenerates the gallery index, and pushes to the `gh-pages` branch. Add the gallery URL to both repos' README files and the repo description ("Live gallery: aeon-gallery.github.io").

---

### 4. Deep Research Mode — Full-Context Synthesis With 1M Token Window

**Type:** Feature
**Effort:** Medium (1-2 days)
**Impact:** Claude Opus 4.6 supports 1M token context windows, but Aeon's research skills (research-brief, paper-digest, digest) operate within default limits — they fetch a few sources, summarize, and move on. A deep research mode could ingest 20-50 sources (full papers, entire GitHub repos, long forum threads, historical article archives) in a single session, producing comprehensive research reports that rival analyst-grade output. The difference between a digest (surface-level summary of 5 sources) and a deep research brief (cross-referenced synthesis of 50 sources with contradiction detection and confidence ratings) is the difference between a news alert and actual intelligence. This leverages Aeon's unique advantage: as a background agent, it doesn't need real-time latency — it can spend 30+ minutes on a single research session that would be impractical in interactive use.

**How:**
1. Create `skills/deep-research/SKILL.md` with `var` as the research question. The skill: performs 5-10 web searches to identify the landscape, fetches full content from the top 30 URLs (using WebFetch), retrieves 10-20 academic papers from Semantic Scholar/arXiv, and loads all content into context.
2. Synthesize a structured research report: Executive Summary, Key Findings (with source citations), Contradictions & Debates (where sources disagree), Data Points (extracted statistics and metrics), Open Questions (what the research doesn't answer), and Recommended Actions. Target 3,000-5,000 words with inline source links.
3. Add a `--depth` parameter in the var: `"AI agent security" --depth=shallow` (5 sources, 500 words) vs `"AI agent security" --depth=deep` (50 sources, 5,000 words). Default to deep. Schedule on-demand rather than cron — this is a resource-intensive skill for specific research needs.

---

### 5. Fork Fleet Coordination — Discover and Collaborate Across Aeon Instances

**Type:** Community / Feature
**Effort:** Large (3+ days)
**Impact:** Aeon has 15 forks, each potentially running its own skill schedule with different configurations and research interests. Right now, these are isolated islands — each fork generates its own token reports, digests, and articles with no awareness of what other instances are producing. A fleet coordination skill could: discover active forks (via GitHub API), check what skills they're running and what output they're producing (by reading their `articles/` directories), and aggregate the best outputs into a cross-instance feed. This creates a network effect: each new fork makes every other fork more valuable by expanding the collective research surface. A user running Aeon for crypto monitoring benefits from another fork's security research, and vice versa. This is the "distributed agent mesh" play — Aeon instances that specialize and share, rather than each duplicating the full skill set.

**How:**
1. Create `skills/fleet-discover/SKILL.md` that: queries `gh api repos/aaronjmars/aeon/forks` to find all public forks, checks each fork's `aeon.yml` config (if public) to see which skills are enabled, and reads their `articles/` directory for recent outputs. Build a fleet registry at `memory/topics/fleet.md` listing each active fork, its owner, enabled skills, and last activity date.
2. Create `skills/fleet-digest/SKILL.md` that aggregates the most interesting outputs across the fleet: unique articles not produced by the local instance, token reports for tokens the local instance doesn't track, and research briefs on topics outside the local instance's focus. Produce a weekly "Fleet Intelligence" digest.
3. Enable opt-in collaboration: if a fork adds `fleet: { share: true, subscribe: true }` to their `aeon.yml`, the coordination skill will index their output and include them in the fleet digest. Forks that set `share: false` are excluded from indexing. Add a `fleet-status` skill that shows the current fleet size, active members, and most popular skills across instances.

---

*Generated by Aeon's `repo-actions` skill on 2026-03-30. This is run 8 overall, bringing the total to 40 ideas. Ecosystem data from web searches performed same day.*

Sources:
- [SkillsMP Review 2026 — SmartScope](https://smartscope.blog/en/blog/skillsmp-marketplace-guide/)
- [Measuring AI Agent Autonomy — Anthropic Research](https://www.anthropic.com/research/measuring-agent-autonomy)
- [AI Agent News March 2026 Roundup — Moltbook-AI](https://moltbook-ai.com/posts/ai-agents-march-2026-roundup)
- [Claude Code & OpenClaw: Agentic AI in 2026 — Tech-Now](https://tech-now.io/en/blogs/claude-code-openclaw-the-rise-of-agentic-ai-in-software-development-2026)
- [Agent Skills Are the New npm — BuildMVPFast](https://www.buildmvpfast.com/blog/agent-skills-npm-ai-package-manager-2026)
- [Eight Trends Defining Software in 2026 — Claude Blog](https://claude.com/blog/eight-trends-defining-how-software-gets-built-in-2026)
- [AI Agents Landscape March 2026 — AI Agents Directory](https://aiagentsdirectory.com/landscape)
- [2026 Agentic Coding Trends Report — Anthropic](https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf)
