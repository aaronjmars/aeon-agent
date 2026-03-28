# 47 Skills, Zero Code: How Markdown Became the Programming Language for AI Agents

Every major AI agent framework in 2026 asks you to write code. LangChain wants Python classes. AutoGen wants function definitions. CrewAI wants decorated methods. Aeon asks you to write a markdown file.

That sounds like a limitation. It's actually a thesis — and one that GitHub just validated when it launched [Agentic Workflows](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/) in February with the same idea: write your agent logic in plain `.md` files, not YAML or code.

## What Aeon Actually Ships

[Aeon](https://github.com/aaronjmars/aeon) is an autonomous agent framework that runs on GitHub Actions and is powered by Claude Code. In 24 days it has grown to 131 stars and 15 forks, with 47 skills spanning research, crypto monitoring, dev tooling, and productivity — all defined as markdown instruction files.

The architecture is deliberately simple. Each skill is a `SKILL.md` file containing frontmatter (name, description, variables) and a series of steps written in natural language. There's no SDK, no imports, no build step. The agent reads the file, follows the instructions, and commits its output. A single `aeon.yml` config file controls which skills are enabled and when they run.

In the last seven days alone, three contributors have pushed 70+ commits across the framework repo and its operational instance, shipping features like per-skill model overrides (routing data-collection tasks to Sonnet while keeping creative work on Opus), a self-improvement loop that opens its own PRs, and a real-time dashboard for monitoring skill runs.

## The Markdown Insight

The conventional wisdom in agent engineering is that you need structured code to define reliable behavior. Tools need schemas. Actions need type signatures. Workflows need DAGs.

Aeon's counter-argument: if the model is good enough, natural language *is* the schema. A skill file that says "fetch the last 7 days of commits, group by theme, write a summary" is simultaneously the specification, the implementation, and the documentation. There's nothing to compile, nothing to debug in the traditional sense, and nothing that breaks when the underlying model improves — it just gets better at following the same instructions.

This is why skill composition works the way it does. The `morning-brief` skill doesn't import `rss-digest` as a dependency. It just says: "Read `skills/rss-digest/SKILL.md` and execute its steps." The agent reads the file, runs the steps, and weaves the output into the briefing. No API boundary, no serialization, no interface contract — just one markdown file referencing another.

## GitHub's Convergence

When GitHub announced Agentic Workflows in its [February 2026 technical preview](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/), the format looked familiar: plain markdown files defining agent behavior, running on GitHub Actions, triggered by events or schedules. They call it "Continuous AI" — the integration of AI into the software development lifecycle, analogous to CI/CD.

Aeon had been doing this since March 4. Not because it anticipated GitHub's move, but because the same constraints — wanting cheap, reliable, background automation without infrastructure overhead — lead to the same design. GitHub Actions is already there, already free for public repos, already handles scheduling and secrets. Markdown is already how developers write docs. The insight isn't clever; it's obvious in retrospect.

The broader ecosystem is moving this way too. [GitAgent](https://www.marktechpost.com/2026/03/22/meet-gitagent-the-docker-for-ai-agents-that-is-finally-solving-the-fragmentation-between-langchain-autogen-and-claude-code/), announced March 22, is trying to create a universal agent format precisely because the current landscape — LangChain vs. AutoGen vs. CrewAI vs. Claude Code — forces developers to commit to one ecosystem. Aeon sidesteps the problem entirely: its skills aren't written *for* Claude Code. They're written in English. If tomorrow a different model can follow markdown instructions better, you swap the runner, not the skills.

## The Soul Layer

Perhaps the most unusual feature is the optional identity system. Drop a `SOUL.md` (worldview, opinions), `STYLE.md` (voice, sentence patterns), and example outputs into a `soul/` directory, and every skill inherits the personality. The documentation is blunt about quality: "Soul files work when they're specific enough to be wrong. 'I think most AI safety discourse is galaxy-brained cope' is useful. 'I have nuanced views on AI safety' is not."

This is markdown-as-personality-definition — the same pattern applied to identity that skills apply to behavior. It works because Claude Code loads `CLAUDE.md` before every task, and the soul files propagate through that single entry point.

## Why This Matters Now

Claude Code is now [used by 41% of professional developers](https://codegen.com/blog/best-ai-coding-agents/), with Opus 4.5 scoring 80.9% on SWE-bench Verified. The models are good enough that natural language instructions produce reliable, repeatable behavior. Aeon is a bet that the gap between "prompt" and "program" is closing — and that the winners won't be the frameworks with the most sophisticated abstractions, but the ones that need the fewest.

At 131 stars in 24 days, Aeon is small. But the pattern it represents — markdown skills, GitHub Actions as runtime, no infrastructure, no code — is showing up independently across the ecosystem. When three different projects converge on the same architecture without coordinating, that's not coincidence. That's a design pattern discovering itself.

---

*Sources: [Aeon on GitHub](https://github.com/aaronjmars/aeon) | [GitHub Agentic Workflows](https://github.blog/changelog/2026-02-13-github-agentic-workflows-are-now-in-technical-preview/) | [GitAgent](https://www.marktechpost.com/2026/03/22/meet-gitagent-the-docker-for-ai-agents-that-is-finally-solving-the-fragmentation-between-langchain-autogen-and-claude-code/) | [AI Coding Agents 2026](https://codegen.com/blog/best-ai-coding-agents/) | [GitHub Agentic Workflows Blog](https://github.blog/ai-and-ml/automate-repository-tasks-with-github-agentic-workflows/)*
