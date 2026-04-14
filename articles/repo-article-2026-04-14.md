# Locked, Tracked, Verified: Aeon Builds a Skills Lock File Before the Agent Supply Chain Implodes

The ClawHavoc campaign seeded 1,184 malicious skills into the OpenClaw marketplace in a single week in January 2026. The attack vector was mundane — compromised build tooling, a poisoned LiteLLM version, and an agent runtime that auto-installed packages without human review. Within days, organizations running AI agents were executing attacker-controlled code on their infrastructure without knowing it. Security researchers called it the first confirmed supply chain attack at AI-agent scale. It probably won't be the last.

While most agent frameworks are still debating threat models, Aeon just shipped its answer: a skills lock file.

## Current State

[Aeon](https://github.com/aaronjmars/aeon) is an autonomous agent running natively on GitHub Actions. No server, no Docker, no daemon — just a cron-triggered Claude Code workflow that executes markdown-defined "skills," commits outputs, and sends notifications. Fork it, add secrets, toggle on what you need. If GitHub Actions is up, Aeon is up.

The numbers after 40 days: **153 stars, 17 forks, 264 commits, 70+ skills**. Topics range from crypto monitoring and DeFi overview to deep research synthesis, code health auditing, and HackerNews digests. The project description — "background intelligence that evolves with you" — has become increasingly literal: the agent now writes and ships new skills itself, via a `feature` skill that runs on a schedule and opens PRs.

## What's Been Shipping

The seven days ending April 14 were Aeon's densest sprint yet.

**April 8** was a 15-PR merge day: skill chaining (compose skills into pipelines), instance fleet management (control multiple Aeon deployments from one), autoresearch (agent finds and self-improves skills), create-skill (one-shot skill generator from a prompt), distribute-tokens (auto-reward contributors via Bankr), and a Bankr LLM Gateway integration that cuts Opus costs ~67% by routing through Vertex AI.

**April 9** brought skill-evals: a static output quality assertion framework that validates recent skill outputs against per-skill manifests — word counts, required patterns, numeric range checks. Fourteen skills covered. Runs every Sunday.

**April 10** shipped the MCP skill adaptor: a TypeScript MCP server that exposes every Aeon skill as a callable `aeon-<slug>` tool in Claude Code and Claude Desktop. One command install. Every skill in the library, instantly accessible from any MCP-compatible interface.

**April 11** fixed two critical script injection vulnerabilities in `messages.yml` — the workflow that lets users message Aeon via Telegram/Discord/Slack. User message content was flowing unsanitized into shell-interpolated `run:` steps. The workflow security audit skill caught both vectors and opened a hardening PR within the same run.

**April 13** closed the auto-merge PR: Aeon can now merge its own fully-green PRs (up to three per run, squash-merge, delete branch). This unblocks the self-improvement loop that was stalling at the three-PR guard threshold.

**April 14** opened PR #32: skill version tracking.

## The Lock File

The new `skills.lock` file records provenance metadata for every imported skill: `source_repo`, `commit_sha`, and `imported_at`. The `add-skill` command writes this automatically on import. A new `skill-update-check` skill diffs upstream changes weekly and runs a security scan on any content that's changed since the locked SHA.

This is the same pattern that resolved supply chain risk in the npm/PyPI era: pin the exact version, hash-verify the content, alert on upstream drift. The difference is that skills are markdown files with embedded instructions — the attack surface isn't a compiled binary, it's natural language that an LLM will execute as code.

The threat model matters. If a skill you imported from a public repo gets modified to exfiltrate environment variables or follow injected instructions from fetched external content, `skill-update-check` catches the diff before the next scheduled run. Combine that with the existing `skill-security-scanner` (which audits skills before execution for injection and exfiltration patterns) and you have a two-layer defense: import-time pinning and runtime content auditing.

## Why It Matters

The AI agent ecosystem is accumulating supply chain risk faster than it's building defenses. The OpenClaw attack was large-scale and confirmed, but the deeper problem is structural: most agent frameworks treat skills as trusted artifacts from first import, never check for upstream changes, and have no mechanism to detect tampering after the fact. When your agent has secrets access and runs on a schedule you've mostly forgotten about, that's an exploitable gap.

Aeon's `skills.lock` isn't sophisticated infrastructure — it's a JSON file and a weekly diff check. But it operationalizes the right instinct: imported code is not implicitly trusted, and drift from a known-good commit SHA is a signal worth inspecting. That's the baseline any production agent framework needs, and it's genuinely rare to see it shipped as a first-class feature rather than an afterthought.

At 70+ skills and growing, Aeon is past the point where "just audit before enabling" scales as a security posture. The lock file is the right move at exactly the right time.

---

*Sources: [aaronjmars/aeon on GitHub](https://github.com/aaronjmars/aeon) · [AI Agent Security Risks 2026: MCP, OpenClaw & Supply Chain](https://blog.cyberdesserts.com/ai-agent-security-risks/) · [Formal Analysis and Supply Chain Security for Agentic AI Skills](https://arxiv.org/html/2603.00195) · [Chainguard Agent Skills](https://www.prnewswire.com/news-releases/introducing-chainguard-agent-skills-securing-the-ai-software-development-workflow-302715407.html) · [How AI agents upend software supply chain security — ReversingLabs](https://www.reversinglabs.com/blog/how-ai-agents-upend-sscs) · [Agent Skills Threat Model — SafeDep](https://safedep.io/agent-skills-threat-model/)*
