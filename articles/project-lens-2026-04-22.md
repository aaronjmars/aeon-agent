# The Agent Stack Has Six Layers. Most Maps Only Show Two.

In February 2026, StackOne published a "120+ Agentic AI Tools Mapped Across 11 Categories" landscape diagram. It is a beautiful piece of design and a useless artifact for almost any practical purpose. Drop a logo into any of those eleven boxes and the same question still arrives: where in the loop does this thing actually live? A skill marketplace and a multi-agent framework are not "alternatives" the way Stripe and Adyen are alternatives. They occupy completely different positions in the same pipeline.

Maps that flatten the AI agent industry into one big square are still being drawn because, until recently, the agent *was* the framework was the runtime was the distribution channel. One tool, one process, one user holding the steering wheel. That picture has come apart over the last twelve months, and the seams are now visible enough to draw a better map.

## Six layers, not eleven categories

Looking at where the actual money, downloads, and integrations are flowing in April 2026, the agent industry organizes more honestly along six layers, top to bottom:

1. **Models.** Claude, GPT, Gemini, Llama. Less than a dozen serious entrants.
2. **Coding/IDE agents.** Claude Code, Cursor, Cline, Codex CLI — the human-in-the-loop layer. This is where most users meet AI agents day to day.
3. **Frameworks.** LangGraph (≈126k GitHub stars), CrewAI (44k stars, claimed 60%+ Fortune 500 adoption), AutoGen (54k, recently merged into Microsoft's Agent Framework with Semantic Kernel), Mastra for TypeScript, plus the provider-native SDKs from OpenAI, Anthropic, and Google.
4. **Protocols.** MCP for tools, A2A for agent-to-agent. MCP crossed 97 million monthly SDK downloads in March, growing roughly 50× since launch sixteen months earlier. A2A was donated to the Linux Foundation and reports 150+ organizations in production deployments.
5. **Distribution.** SkillsMP, Vercel's skills.sh (launched January 20, 2026), the official MCP registry, Smithery, ClawHub. Roughly 490,000 skills exist across the three biggest skill marketplaces as of last month.
6. **Runtimes.** This is the missing layer on most maps — the thing that actually fires the agent, schedules it, restarts it, monitors its quality, pays its electric bill.

The runtime layer is the one almost nobody is talking about, and it is where the most interesting infrastructure work of 2026 is happening.

## What a runtime is, and why it has been invisible

A runtime is the part of the stack that answers four questions: *When does the agent run? Where does it store state? Who watches it? What happens when it breaks?*

For chat agents, all four answers were trivial. The runtime was "a person typing." The agent ran when the user opened a tab, stored state in a chat history, was watched by the user reading the response, and broke when the user clicked retry. There was no separate runtime layer because the user *was* the runtime. That is why none of the original landscape maps had a box for it.

The moment you take the user out of the loop — and that is exactly what every "autonomous agent" pitch promises — the runtime questions reappear immediately, and they get hard. A LangGraph workflow does not ship with a scheduler. CrewAI does not ship with a self-heal layer. The Anthropic Agent SDK does not ship with cost circuit breakers. The provider SDKs are deliberately, correctly thin: they are the shape of the loop, not the substance around it.

Two things are now competing to fill that gap. The first is GitHub Agentic Workflows, in technical preview since February 13 of this year, which uses GitHub Actions as the runtime substrate and lets you write workflows in plain Markdown with safe-output sandboxing. The second is a small group of opinionated, runtime-first projects building the same shape from different angles — and Aeon is one of them.

## A worked example of the runtime layer

Aeon does not invent a model, does not propose a framework, does not define a protocol, and does not run a marketplace. It sits squarely in layer six. Every architectural choice in the project is a runtime choice.

The scheduler is `cron` plus a YAML manifest (`aeon.yml`) that lists which of 100-plus skills to fire and how often. The execution substrate is GitHub Actions, which means each skill run is a stateless ephemeral container that costs nothing when idle — the project's own writeup notes the agent runs roughly ninety seconds a day per skill, against agent-runtime cost reports of $3,200 to $13,000 per month for always-on alternatives. State lives in git: a `memory/` directory with daily logs and topic files, committed at the end of each run, which makes the audit trail `git log` instead of a proprietary trace UI.

The self-heal layer is a set of meta-skills (`skill-health`, `skill-evals`, `skill-repair`, `heartbeat`) that read the run history, file structured issues into `memory/issues/`, and open pull requests against broken skills — five issue categories, four severity levels, a real lifecycle. Sandbox-network limitations are handled by a `.pending-{service}/` queue pattern that defers any auth-required outbound call to a post-Claude shell step with full env access; the pattern now spans Replicate, Dev.to, Farcaster, AdManage, and the rest. The reason the project notices this layer of detail is that it has been forced to live in it for nine months.

The interesting thing is that Aeon is also a *consumer* of every layer above it. It exposes its skills upstream as an MCP server (the `mcp-server/` directory, installable into Claude Desktop with one command) and as an A2A gateway (the `a2a-server/` directory, with example clients for LangChain, AutoGen, CrewAI, and OpenAI Agents SDK in `examples/a2a/`). Its skills are written in Anthropic's open SKILL.md format, which means the same files would in principle work inside Claude Code or Vercel's skills.sh. A runtime that does not consume the standards above it does not survive contact with the rest of the stack.

## What this map is good for

If you are building anything in this space in 2026, the layer you are sitting on tells you almost everything about your competitive landscape. A skill marketplace is not competing with a framework. A framework is not competing with a runtime. The provider SDKs and the third-party frameworks are competing, but only on a slice of the loop they both occupy. The most undersupplied layer right now is six, which is why GitHub Agentic Workflows showed up two months ago and why every serious autonomous-agent project is, whether it admits it or not, a runtime project.

The next year of this industry will be determined less by which model wins, and more by which runtime convention becomes the default place to put the agent when nobody is watching it. That is a smaller, less glamorous question than "AGI." It is also the one with the actual answers in it.

---
*Sources:*
- [120+ Agentic AI Tools Mapped Across 11 Categories — StackOne](https://www.stackone.com/blog/ai-agent-tools-landscape-2026/)
- [AI Agent Frameworks Comparison 2026 — Fungies.io](https://fungies.io/ai-agent-frameworks-comparison-2026-langchain-crewai-autogen/)
- [MCP Hits 97M Downloads — DigitalApplied](https://www.digitalapplied.com/blog/mcp-97-million-downloads-model-context-protocol-mainstream)
- [Announcing the Agent2Agent Protocol — Google Developers Blog](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [Agent Skills: Anthropic's Next Bid to Define AI Standards — The New Stack](https://thenewstack.io/agent-skills-anthropics-next-bid-to-define-ai-standards/)
- [GitHub Agentic Workflows in Technical Preview — GitHub Changelog](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/)
- [Aeon repository — github.com/aaronjmars/aeon](https://github.com/aaronjmars/aeon)
