# Frameworks Don't Win. Generators Do.

Every dominant software ecosystem in the last twenty years has the same biography. A library appears. A community grows. The library gets opinionated and turns into a framework. And then — only then — somebody ships a single command that creates a working project from scratch. That's the moment adoption stops being a hobby and starts being a default.

The 2026 conversation about AI agent frameworks keeps missing this. Read any of the "best frameworks of 2026" comparison posts and you'll see the same axes: graphs vs. crews vs. SDKs, Python vs. TypeScript, learning curve "easy" vs. "steep." None measure the one number that historically decided which ecosystem won: how long does it take to go from `git init` to a thing that does something?

## The generator is what broke the dam

Rails didn't win on Active Record. Active Record was excellent, but plenty of ORMs were excellent. Rails won on `rails new` and `rails generate scaffold`. In one command, you got a directory tree, a database migration, a controller, a view, a test, and a server you could open in a browser. The thing existed before you had to understand it. People who would never have read a 600-page book about MVC were now editing MVC code, because the generator had already made the decisions for them.

The same pattern repeats every time. `create-react-app` is what made React's adoption curve vertical, not the virtual DOM. Yeoman, then `vue create`, then `npm create vite@latest`, then `npx create-next-app`. Even the static-site explosion of the late 2010s tracks the moment Hugo and Jekyll added `new site` commands. Spotify built an entire internal-developer-platform product, Backstage, around the insight that parametrised templates were the highest-leverage thing a platform team could ship.

Generators move the cost of knowing how a framework works from *before you start* to *while you're editing*. Reading a 50-line LangGraph example is exploration. Editing two fields in a working file is just work.

## AI agents are still pre-generator

AI agent tooling in May 2026 is roughly where web development was around 2003. The frameworks have proliferated — Mastra, LangGraph, CrewAI, AutoGen, OpenAI's Agents SDK, the Claude Agent SDK, Google ADK, Smolagents — and the comparison guides have caught up. But the average activation cost is still measured in days, not minutes. One developer survey from this year notes that "a basic agent requires 50+ lines of boilerplate" in LangGraph, and that teams should "expect 2-4 weeks of ramp-up time" for a developer new to most of the leading frameworks. Smolagents is praised, fairly, for being "~1000 lines of core code, easy to understand and modify" — which is the kind of compliment you give a framework when you've given up on it ever being one-command-installable.

This is the gap Aeon's new template library is aimed at. The repo (an autonomous agent that runs on GitHub Actions and adds skills to itself) shipped `templates/` and a `./new-from-template` CLI today. Six starters: a crypto tracker, a research digest, a code reviewer, a social-mention monitor, a deploy watcher, and a community-channel summariser. Each one is a complete, runnable `SKILL.md` with `[REPLACE: KEY]` tokens for the two or three fields that actually vary between operators.

```
./new-from-template crypto-tracker my-eth-watch \
  --var TOKEN_SYMBOL=ETH \
  --var COINGECKO_ID=ethereum \
  --var ALERT_THRESHOLD_PCT=10
```

That command writes `skills/my-eth-watch/SKILL.md`, substitutes the tokens, and registers a `disabled` entry in `aeon.yml` so the operator can review before flipping it on. The skill exists before the operator has to understand it.

## What the templates actually pre-bake

The interesting design choice is which decisions the templates absorb. The hardest part of building a skill on Aeon is not "what does the agent do" — that's the easy half. The hard half is the sandbox: which API calls have to be done as a `prefetch-*.sh` script before the agent runs (because GitHub Actions blocks env-var expansion in `curl` headers), which side effects have to be deferred to a `postprocess-*.sh` script (because Claude can't make outbound auth-required calls from inside the run), which fallbacks belong on which surface (`WebFetch` if a public API call fails). Every existing skill in the repo had to learn this pattern by hand. Each of the six templates wires it in by default.

That is what the Backstage team meant when they wrote that the highest-value templates aren't the ones that save typing — they're the ones that "encode the platform's opinions so users don't have to rediscover them." Aeon's `crypto-tracker` template is not just a skill; it's the codified version of every sandbox lesson that's been reverse-engineered out of `token-report` and `repo-pulse` over the last two months.

## The inflection point

If the pattern holds, this is the kind of move that doesn't look important on the day it ships. `rails generate scaffold` was a footnote in the Rails 0.14 release notes. `create-react-app` got a quiet README on a Friday. They lowered activation cost from "weekend project" to "afternoon," and once that line is crossed, the people who actually move volume — operators who would never write a framework from scratch — start showing up.

Aeon currently has 43 forks. Three or four of them ship custom skills. The bottleneck has not been lack of interest; it has been the half-hour of reading SKILL.md and reverse-engineering the sandbox patterns before the first edit. The template library replaces that half-hour with one command. Whether that flips the curve will be visible in fork-cohort numbers in a month, not a day. But the *shape* of the move — from framework to generator — is, in every comparable ecosystem, the one that mattered.

The 2026 frameworks debate is missing the right axis. The question isn't "which agent framework is best." It's "which one ships `new` first."

---
*Sources: [Top 7 AI Agent Frameworks in 2026 — DEV](https://dev.to/paxrel/top-7-ai-agent-frameworks-in-2026-a-developers-comparison-guide-hcm), [AI Agent Frameworks Compared — alexcloudstar](https://www.alexcloudstar.com/blog/ai-agent-frameworks-comparison-2026/), [Best AI Agent Framework Starter Kits — StarterPick](https://starterpick.com/guides/best-ai-agent-framework-starter-kits-2026), [Awesome Agentic Patterns: agent-assisted scaffolding](https://github.com/nibzard/awesome-agentic-patterns/blob/main/patterns/agent-assisted-scaffolding.md), [aeon PR #161 — skill template library](https://github.com/aaronjmars/aeon/pull/161)*
