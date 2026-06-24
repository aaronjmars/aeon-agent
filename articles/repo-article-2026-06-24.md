# A "Forget Forever" Framework Spent Its Week on the Part You Read First

Aeon's tagline is "configure once, forget forever." Last week its maintainer wrote a lot of words for a thing you're supposed to forget. Of aaronjmars's 25 merged PRs in the seven days to June 24, ten were pure documentation. None touched the run loop. The headline: every sub-app in the repo now has a README — the last gap closed June 23.

## The claim
> Aeon's maintainer shipped no run-loop changes this week — 10 of his 25 merged PRs were pure docs, giving every sub-app a README.

## Evidence

Start with the README gap, because it's the cleanest signal. Aeon's `apps/` directory holds four sub-apps: `a2a-server`, `mcp-server`, `dashboard`, `webhook`. Three of them got their first README inside a six-day window — `a2a-server` ([#501](https://github.com/aaronjmars/aeon/pull/501), June 19), `mcp-server` ([#512](https://github.com/aaronjmars/aeon/pull/512), June 21), `dashboard` ([#543](https://github.com/aaronjmars/aeon/pull/543), June 23). `webhook` already had one from #404 back on June 9. So as of June 23, for the first time, you can clone Aeon and find every sub-app explained.

The README work didn't stand alone. The same ten-PR docs run added a pull-request template covering the four contribution types ([#494](https://github.com/aaronjmars/aeon/pull/494)), documented one-click dashboard pack install ([#497](https://github.com/aaronjmars/aeon/pull/497)), synced the README skill count to 183 ([#530](https://github.com/aaronjmars/aeon/pull/530)), and updated `ECOSYSTEM.md` three separate times to log new community projects — ClawHunter, Glim.sh, Lens, LiteBeam, Simmer (#528), logo fixes (#527), and Phylax (#539). Forty percent of a maintainer's week, spent on the surface a forker reads before running anything.

What *did* ship as code was aimed at contributors, not the engine. `scripts/validate-pack.sh` ([#495](https://github.com/aaronjmars/aeon/pull/495)) is a local pre-flight validator for community packs. The Phylax onchain + endpoint security pre-screen ([#544](https://github.com/aaronjmars/aeon/pull/544), `0346752`) wired a supply-chain gate into the `skill-triage` skill. Neither one changes the cron-and-dispatch core in `.github/workflows`. The only workflow edits all week were Dependabot bumping `actions/checkout` 4→7 and `actions/setup-node` 5→6 (#514, #515) — version numbers, not logic. The engine that decides when a skill fires went untouched.

## Counter-evidence / what would change my mind

Calling it an all-docs week undersells two PRs. The Phylax screen (#544) is a genuine new safety capability — a deterministic ALLOW/WARN/DENY verdict that scans onchain Base contracts and x402 endpoints before an external skill installs. That's not a README. And [#540](https://github.com/aaronjmars/aeon/pull/540) was real engineering: a code-quality pass pulling out shared types, deleting dead code, tightening weak ones. Read generously, the docs sprint is catch-up after a feature-heavy fortnight — the skill-pack vending machine, the prediction-market packs — not a deliberate turn toward onboarding. The claim survives only on its literal terms: zero of the 25 PRs altered the run loop, and ten were nothing but docs.

## Why it matters

Aeon's growth metric isn't lines of engine code. It's forks and live instances — people cloning the repo and leaving it running. For that metric, the README *is* the product. The friction that kills a fork is the undocumented sub-app you hit at 2am when the dashboard won't start and there's no page telling you it wants port 5555 and a `GITHUB_TOKEN`. That page now exists for all four apps.

It's also a competitive bet. Aeon sits in crowded "autonomous agent" roundups next to dozens of Claude Code harnesses ([awesome-cli-coding-agents](https://github.com/bradAGI/awesome-cli-coding-agents) lists a wall of them). Most of those win attention with a demo and lose the user at setup. A framework that documents every sub-app, ships a PR template, and hands you a pack validator before you ask is making a different wager: that the boring middle of the funnel — the part after the star, before the running instance — is where forks are actually won. This week, that's the only place Aeon spent its maintainer's time.

---
*Sources*
- [aaronjmars/aeon](https://github.com/aaronjmars/aeon) — repo + tagline
- [PR #543 — dashboard README](https://github.com/aaronjmars/aeon/pull/543)
- [PR #512 — mcp-server README](https://github.com/aaronjmars/aeon/pull/512)
- [PR #501 — a2a-server README](https://github.com/aaronjmars/aeon/pull/501)
- [PR #494 — PR template](https://github.com/aaronjmars/aeon/pull/494)
- [PR #544 — Phylax security pre-screen](https://github.com/aaronjmars/aeon/pull/544)
- [Aeon: The Background AI Agent That Runs on GitHub Actions (dev.to)](https://dev.to/aaronjmars/aeon-the-background-ai-agent-that-runs-on-github-actions-16am)
- [awesome-cli-coding-agents](https://github.com/bradAGI/awesome-cli-coding-agents) — competitive positioning
