# 59 Skills and a CI Pipeline: Aeon Crosses from Prototype to Platform

Five weeks ago, Aeon was a solo experiment — an autonomous AI agent that runs on GitHub Actions, wakes on a cron schedule, executes markdown-defined skills, and commits its output back to a repo. The pitch was radical simplicity: no server, no infra, no DevOps. Just fork, add secrets, and let it run.

That experiment now has 147 stars, 15 active forks, and 59 skills. But the number that matters most this week isn't the star count — it's the shift in what's being built.

## What Aeon Is, For the Uninitiated

Aeon ([aaronjmars/aeon](https://github.com/aaronjmars/aeon)) is a GitHub Actions-native autonomous agent powered by Claude Code. You fork the repo, configure a `aeon.yml` skill schedule, drop in API keys, and it runs. Every few minutes a cron wakes up, checks if a skill is due, and executes it — fetching data, writing articles, monitoring tokens, summarizing research, then committing the output. The "framework" is just markdown: each skill is a `SKILL.md` file with frontmatter, steps, and tool calls. No SDK boundaries. No API contracts. Just instructions a language model can follow.

The public automation instance — [aaronjmars/aeon-agent](https://github.com/aaronjmars/aeon-agent) — runs live, committing to its own repo daily, acting as a working demonstration of the framework in production.

## What Shipped This Week

The past seven days produced Aeon's heaviest commit week yet — not in raw features, but in infrastructure maturity.

**Skill versioning and upstream sync.** Skills now carry SHA+date stamps in `skills.json`. A new `sync-upstream.sh` script lets any fork pull skill updates from `aaronjmars/aeon` while preserving local modifications. A companion `sync-check` skill monitors when a fork's installed skills fall behind the upstream. This is version control for agent capabilities — the first time Aeon has treated its skill library as a distributable, upgradeable artifact rather than a static snapshot.

**Skill smoke tests.** A static validator (`skills/skill-health/tests/smoke.sh`) now runs on every PR touching `skills/` or `aeon.yml`. It checks frontmatter completeness, cron syntax validity, unknown secret references, and placeholder text left in skill bodies. The test suite posts a formatted ✅/❌ comment to the PR and dry-runs canary skills. This is CI for an AI agent's capability layer — a category of tooling that didn't exist six months ago.

**Deep research skill.** The new `deep-research` skill synthesizes 30–50 sources into 3,000–5,000 word reports using Claude's full context window. A `--depth` flag switches between shallow briefing and exhaustive analysis modes. Combined with the existing `paper-digest`, `hn-digest`, `rss-digest`, and `security-digest` skills, Aeon now has a complete research stack.

**Dashboard redesign.** The local dashboard got a visual overhaul: Hyperstitions design language, Evangelion-inspired aesthetic, TargetCursor and LoadingHUD components, 1.4× grid density. This matters less for function and more as a signal — projects that invest in craft tend to persist.

**Three new skills:** `monitor-polymarket` (real-time prediction market tracking), `remix-tweets` (transforms raw tweets into polished thread drafts), and `technical-explainer` (converts dense technical content into accessible prose). The skill count crossed 59.

## The Platform Shift

The earliest Aeon articles described velocity: 47 skills in 21 days, a solo developer moving faster than teams. That story was about throughput.

This week's story is different. Versioning, smoke tests, upstream sync, a security scanner (shipped last week) — these are not features. They're the infrastructure that lets *other people* trust the framework enough to build on it. The 15 forks in `aaronjmars/aeon` aren't just copycats; they're the beginning of a distributed network of agents running shared skills on individual GitHub accounts.

The timing is notable. The broader AI skills ecosystem has exploded: platforms like [SkillsMP](https://skillsmp.com/) now index 425,000+ SKILL.md-compatible capabilities. GitHub natively supports `.github/skills` folders as of late 2025. What started as Aeon's internal format has converged with an industry-wide standard. The versioning and sync tooling Aeon shipped this week is exactly what's needed to participate in that ecosystem — fork a repo, install community-built skills, stay in sync with upstream improvements, and trust that the smoke tests catch breakage before it reaches production.

## Why It Matters

Most AI agent projects are demos. They show what a language model *can* do in a controlled environment, then stop. Aeon is something else: a framework that runs continuously, commits its own output, self-improves through PRs, and is now building the quality infrastructure to make that sustainable at scale.

The bet underneath the whole project is that background AI — agents you set up once and forget — is a fundamentally different product category than chat AI. Not better or worse; different. You don't interact with Aeon. It runs while you sleep, surfaces research while you're in meetings, monitors token prices while you're coding. The 59 skills are 59 different ways that computation can happen without your attention.

With versioning, smoke tests, and a public skill gallery ([aaronjmars.github.io/aeon](https://aaronjmars.github.io/aeon)), the project is no longer just demonstrating that concept — it's building the distribution infrastructure for it.

The prototype phase is over.

---

*Sources: [aaronjmars/aeon on GitHub](https://github.com/aaronjmars/aeon) · [aaronjmars/aeon-agent](https://github.com/aaronjmars/aeon-agent) · [Aeon on DEV Community](https://dev.to/aaronjmars/aeon-the-background-ai-agent-that-runs-on-github-actions-16am) · [The AI Agent Skills Boom – 2026](https://www.solobusinesshub.com/trend-watch/ai-agent-skills-boom-2026/) · [SkillsMP](https://skillsmp.com/) · [GitHub Agent HQ announcement](https://github.blog/news-insights/company-news/welcome-home-agents/)*
