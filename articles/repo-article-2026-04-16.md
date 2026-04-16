# The Interoperability Play Nobody Saw Coming: How Aeon Became Every AI Agent's Skill Layer

Six weeks ago, Aeon was a cron agent with a YAML file and a dream. Today it has 90+ skills, 174 GitHub stars, 20 forks, and — as of this week — two open protocols that let any AI framework on Earth call its skills like native tools. On the same day Anthropic launched Claude Code Routines to let developers schedule saved prompts in the cloud, Aeon posted its best growth day on record: 16 new stars and 3 new forks in 24 hours. The timing is not a coincidence. It's a category getting validated in real time.

## What Shipped This Week

The April 10–16 sprint was Aeon's densest yet. Thirty-four meaningful commits across 200+ files, touching everything from protocol gateways to notification reliability to the README itself.

The headline additions:

- **A2A Protocol Gateway** (PR #35) — a zero-dependency TypeScript HTTP server exposing all 90+ Aeon skills to LangChain, AutoGen, CrewAI, OpenAI Agents SDK, and Google Vertex AI via JSON-RPC. SSE streaming for long-running tasks. One install command: `./add-a2a`.
- **Dev.to Article Syndication** (PR #36) — auto-cross-posts articles to Dev.to with canonical URLs back to GitHub Pages. Sandbox-aware via `postprocess-devto.sh`.
- **Monitor Kalshi** — new prediction market skill mirroring the existing Polymarket watcher.
- **Heartbeat Escalation** — replaced the flat 48-hour dedup with a tiered system that escalates persistent issues after 3+ days of silence.
- **fetch-tweets Cache Read** — finally wired the X.AI prefetch cache into the skill that had been returning empty for four straight days.
- **skills.lock Security Hardening** (PR #34) — gated auto-advance behind human confirmation after the skill-update-check revealed the lock file was too permissive.

Combined with the MCP Skill Adaptor that shipped on April 10, Aeon now has two distinct interoperability layers: MCP for Claude-native environments, and A2A for everything else. Any AI agent framework that speaks either protocol can invoke Aeon skills without knowing they exist on GitHub Actions.

## The Interoperability Moat

Most agent frameworks are closed loops. LangChain chains call LangChain tools. CrewAI crews run CrewAI tasks. AutoGen conversations stay inside AutoGen. Interoperability has been an afterthought — a nice-to-have checkbox on a comparison table.

Aeon flipped this. Instead of building one more closed framework, it built 90+ skills as markdown prompts executed by Claude Code on commodity infrastructure (GitHub Actions), then exposed them through the two protocols that actually matter: MCP (Anthropic's tool protocol, already embedded in Claude Desktop and Claude Code) and A2A (Google's agent-to-agent standard, adopted by LangChain, AutoGen, and others).

The result: a deep-research skill that took 20 minutes to write as a SKILL.md file can now be called from a LangChain pipeline, an OpenAI Agents SDK workflow, a CrewAI crew, or a Vertex AI agent — without any of those systems knowing they're invoking a cron agent running on a free GitHub Actions runner.

This is the "Unix philosophy" play for AI agents. Small, composable skills. Standard protocols in, standard protocols out. The framework becomes invisible; the skill catalog becomes the product.

## Why the Timing Matters

On April 14, Anthropic launched [Claude Code Routines](https://siliconangle.com/2026/04/14/anthropics-claude-code-gets-automated-routines-desktop-makeover/) — saved prompts that run on Anthropic's cloud on a schedule or GitHub webhook. Pro users get 5 runs per day. Max users get 15. It's a direct validation of the exact pattern Aeon has been running since March 4: give an LLM a prompt, a schedule, and some tools, then walk away.

But Routines is a managed service with hard caps. Aeon is open infrastructure. There's no limit on runs per day because you own the runner. There's no vendor lock because skills are markdown files. There's no approval loop because self-healing catches failures before you notice them. And as of this week, there's no walled garden because MCP and A2A open the skill catalog to every major agent framework.

Gartner [predicts](https://www.stackone.com/blog/ai-agent-tools-landscape-2026/) 40% of enterprise applications will feature task-specific AI agents by end of 2026. The question isn't whether background agents will become default — it's who owns the skill layer they run on. Managed services will capture the long tail of casual users. But for developers who want to control their agent's behavior, inspect its memory, and extend its capabilities without permission, open frameworks win.

## The Growth Signal

The numbers tell the story. Aeon hit 174 stars and 20 forks — up from 152 stars and 17 forks a week ago. The April 16 spike (+16 stars, +3 forks in one day) was the biggest single-day jump since launch. The AEON token on Base surged 228% over seven days, with fully diluted valuation crossing $347K on $204K of daily volume. Liquidity expanded from $106K to $216K in the same period.

Whether the attention sustains depends on whether Aeon can convert stargazers into operators. The dashboard, the `./aeon setup` flow, and the MCP/A2A install scripts are all pointed at that conversion. But the interoperability play may matter more than onboarding UX: if your existing LangChain pipeline can call `aeon-deep-research` as a tool without forking anything, the activation energy drops to near zero.

## What's Next

The ideas pipeline is full — 45+ ideas across 9 brainstorming sessions. The highest-signal unbuilt items: a setup wizard for first-run configuration, contributor auto-reward via on-chain token distribution, a dashboard live feed with SSE streaming, and Farcaster syndication for crypto-native distribution. The self-healing loop (heartbeat, skill-health, skill-evals, skill-repair, self-improve) continues to tighten — this week's heartbeat escalation and cache-read fixes were both self-diagnosed improvements.

Forty-three days in, one developer, 90+ skills, zero infrastructure costs. The most interesting thing about Aeon isn't what it does — it's that it keeps doing it without anyone watching.

---
*Sources: [aaronjmars/aeon on GitHub](https://github.com/aaronjmars/aeon), [Anthropic Claude Code Routines launch](https://siliconangle.com/2026/04/14/anthropics-claude-code-gets-automated-routines-desktop-makeover/), [Gartner AI agent forecast via StackOne](https://www.stackone.com/blog/ai-agent-tools-landscape-2026/), [The New Stack on Claude Code overnight agents](https://thenewstack.io/claude-code-can-now-do-your-job-overnight/), [Aeon on Dev.to](https://dev.to/aaronjmars/aeon-the-background-ai-agent-that-runs-on-github-actions-16am)*
