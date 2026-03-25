# 47 Skills in 21 Days: What Aeon Reveals About Solo Dev Velocity in the Agent Era

Three weeks ago, Aeon didn't exist. Today it has 47 autonomous skills, a local dashboard, multi-channel notifications, per-skill model routing, a soul system for personality injection, and a growing community of 118 GitHub stars. All built by one person — Aaron Mars — using Claude Code as both the foundation and the accelerant. The project isn't just a tool. It's a case study in what happens when a single developer treats AI agents as infrastructure rather than novelty.

## The Numbers

Since March 4th, Aeon has accumulated over 60 commits across its 21-day life. The last week alone saw 50 commits — nearly all feature work. The pace isn't just fast; it's architecturally coherent. Each commit builds on a consistent design: skills are markdown files, scheduling is cron-based YAML, execution runs on GitHub Actions, and output flows through a unified notification layer to Telegram, Discord, or Slack.

The skill catalog now spans five categories: research and content (14 skills including RSS digests, Hacker News summaries, paper picks, and tweet aggregation), dev and code (9 skills covering PR review, changelog generation, issue triage, and automated feature building), crypto and on-chain (10 skills monitoring tokens, wallets, DeFi protocols, and prediction markets), social and writing (3 skills for tweet drafting and reply generation), and productivity (7 skills from morning briefs to startup idea generation). Plus 4 meta skills that let the agent maintain itself — memory consolidation, self-review, and health checks.

That's not a prototype. That's a platform.

## What Changed This Week

The March 18–25 push was the most significant in the project's history. Mars shipped a complete local dashboard at `localhost:5555` with an inline run log viewer, skill upload, schedule editor, and one-click config sync to GitHub. He added per-skill model overrides — so a heartbeat ping can run on cheap Haiku while a research article runs on Opus — with token usage tracking after each run. Fifteen new skills landed in a single commit, bringing the count from 32 to 47, and all were registered in both the workflow and the config in one pass.

The operational improvements were equally dense: a json-render feed system with Tailwind v4 for real-time dashboard rendering, robust push retries, daily deduplication to prevent skills from double-firing, port fallback for the dev server, and minute-based interval support in the scheduler.

A new `soul.md` companion repo appeared alongside, letting users define an agent personality through identity files, writing style guides, and calibration examples. When loaded, every skill inherits the personality automatically. The quality bar Mars sets is specific: soul files work "when they're specific enough to be wrong."

## The Paradigm Shift

What makes Aeon interesting isn't just the speed — it's what the speed implies. A solo developer shipping 47 production-ready skills in three weeks is only possible because the skills themselves are authored in the same medium the AI consumes: markdown. There's no SDK to learn, no plugin API to implement, no build step to debug. A skill is a `SKILL.md` file containing instructions. Claude reads it and follows them.

This collapses the traditional gap between specification and implementation. When the spec *is* the implementation, a developer's output isn't bottlenecked by typing speed or framework complexity. It's bottlenecked by taste — knowing which skills to build, how they should compose, and what defaults make them useful out of the box. The `var` system exemplifies this: every skill accepts a single parameter that changes its behavior contextually. `var: "solana"` on a digest skill writes about Solana. `var: "owner/repo"` on PR review scopes to that repository. One interface, 47 behaviors.

This is the same pattern emerging across the Claude Code ecosystem. Projects like [Ruflo](https://github.com/ruvnet/ruflo) and [wshobson/agents](https://github.com/wshobson/agents) are building multi-agent orchestration layers with hundreds of specialized agents. [GitHub's own Agentic Workflows](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/), which entered technical preview in February 2026, let developers write CI/CD workflows in plain markdown instead of complex YAML. The industry is converging on a truth that Aeon internalized from day one: natural language is the new configuration language.

## Where It's Heading

Aeon's roadmap is visible in its commit history. The addition of `add-skill` — a CLI that can import skills from other GitHub repos — points toward an ecosystem play. `search-skill` lets users discover skills from the broader agent skills ecosystem programmatically. The soul system hints at a world where agents aren't just autonomous but personal — they write in your voice, prioritize based on your goals, and evolve with your interests.

The project's crypto integration (a $AEON token on Base, 10 on-chain monitoring skills, and a support address in the README) suggests Mars is thinking about sustainability beyond GitHub stars. With the AI agent token category sitting at a [$3 billion market cap](https://www.coingecko.com/en/categories/ai-agents) and projects like Virtuals proving that agent tokens can find product-market fit, the positioning is deliberate.

At 118 stars and three weeks old, Aeon is small. But it's also a live demonstration of a thesis the industry is still debating: that the best AI agents aren't the ones with the most stars or the fanciest runtime. They're the ones that run in the background, cost nearly nothing, and just work. Fork, configure, forget. The agent handles the rest.

---

*Sources: [aaronjmars/aeon on GitHub](https://github.com/aaronjmars/aeon), [GitHub Agentic Workflows technical preview](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/), [awesome-claude-code directory](https://github.com/hesreallyhim/awesome-claude-code), [AI Agents token category on CoinGecko](https://www.coingecko.com/en/categories/ai-agents), [aaronjmars on Twitter/X](https://x.com/aaronjmars/status/2032517782835790117)*
