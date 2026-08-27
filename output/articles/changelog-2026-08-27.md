# Changelog — Week of 2026-08-27

*Window: 2026-08-20 → 2026-08-27 · Sources: aeonfun/aeon=ok, aeonfun/minitor=ok, aeonfun/opendia=ok, aeonfun/soul.md=empty*

## aeonfun/aeon

> **Highlights:** Aeon added four new run harnesses — fx (Vercel's native agent), Cursor CLI, Hermes, and GLM Coding Plan — and closed two credential-leak paths: a `secretcurl` argv exposure and infra channel tokens sitting in every skill's runtime env.

### Added
- fx — Vercel's native Zig coding agent — joins Aeon as a 7th run harness, with full native MCP support and no npm/pipx install step. ([#941](https://github.com/aeonfun/aeon/pull/941))
- Cursor CLI, Hermes (via Nous Portal), and GLM Coding Plan (Z.AI) added as three more supported harnesses. ([#967](https://github.com/aeonfun/aeon/pull/967))
- New `skill-article` skill turns any skill in the catalog into a publish-ready launch article, receipts-first (no invented stats). ([#945](https://github.com/aeonfun/aeon/pull/945))
- New `rightstack` skill: an optional, read-only Web3 stack-planning advisor (workflow, tools, tradeoffs, migration warnings). ([#961](https://github.com/aeonfun/aeon/pull/961))
- Dashboard now auto-allowlists MCP secret names into run workflows when you Connect a new integration. ([#931](https://github.com/aeonfun/aeon/pull/931))
- Three community skill packs added to the catalog: CultOS, Farcaster, and Spoolis Outcome Gate. ([#974](https://github.com/aeonfun/aeon/pull/974), [#977](https://github.com/aeonfun/aeon/pull/977), [#978](https://github.com/aeonfun/aeon/pull/978))
- Agent Plugins support (plugin.json + privacy/support pages) for Kiro Powers, plus a MiniMax operator-console plugin manifest. ([#964](https://github.com/aeonfun/aeon/pull/964), [#965](https://github.com/aeonfun/aeon/pull/965))
- Dashboard gained a recommend-only harness comparison view. ([#969](https://github.com/aeonfun/aeon/pull/969))

### Fixed
- Windows "Connect" no longer truncates the OAuth URL; slow first-time sign-in no longer times out; long chain configs no longer corrupt on save. ([#930](https://github.com/aeonfun/aeon/pull/930))
- The documented "run `cd` as its own Bash call" pattern was silently denied on some forks for weeks — `cd` is now allowlisted, unblocking any skill that relied on it. ([#933](https://github.com/aeonfun/aeon/pull/933))
- Diagnostic output from a failed skill run is no longer truncated mid-error. ([#932](https://github.com/aeonfun/aeon/pull/932))
- fx was missing from the dashboard's harness picker and MCP dispatch after launch — both fixed same week. ([#943](https://github.com/aeonfun/aeon/pull/943), [#953](https://github.com/aeonfun/aeon/pull/953))
- Fixed races where concurrent runs could corrupt shared state: the issue store and `aeon.yml` config saves. ([#936](https://github.com/aeonfun/aeon/pull/936), [#944](https://github.com/aeonfun/aeon/pull/944))
- Fixed duplicate Telegram message delivery and unbounded reply-chunk rendering. ([#937](https://github.com/aeonfun/aeon/pull/937), [#970](https://github.com/aeonfun/aeon/pull/970))
- Fixed kimi auth capture, macOS cron-date parsing, macOS issue-store repo defaults, and `add-skill` commit provenance tracking. ([#956](https://github.com/aeonfun/aeon/pull/956), [#957](https://github.com/aeonfun/aeon/pull/957), [#971](https://github.com/aeonfun/aeon/pull/971), [#972](https://github.com/aeonfun/aeon/pull/972))
- `mcp-server` now runs skills through a single-flight async queue instead of blocking on each dispatch. ([#973](https://github.com/aeonfun/aeon/pull/973))
- The run scorer now grades the notification actually delivered, not an internal summary of it. ([#949](https://github.com/aeonfun/aeon/pull/949))
- Dashboard auth rows updated to reflect the newly added harnesses. ([#975](https://github.com/aeonfun/aeon/pull/975))

### Changed
- `memory-flush` now runs deterministic prep with a structured watermark. ([#938](https://github.com/aeonfun/aeon/pull/938))
- Vuln-scanner runs now emit machine-readable execution evidence alongside their report. ([#968](https://github.com/aeonfun/aeon/pull/968))
- Removed a stale project from the public ecosystem list. ([#979](https://github.com/aeonfun/aeon/pull/979))

### Security
- Fixed a secret leak in `secretcurl`: substituted API keys were landing in curl's own process args, readable by any other process via `ps`/`/proc`. ([#935](https://github.com/aeonfun/aeon/pull/935))
- Removed infra channel tokens (Telegram/Discord/Slack/Buzz) from every skill's runtime environment — only a new post-run delivery dispatcher can now read them to send. ([#951](https://github.com/aeonfun/aeon/pull/951), [#955](https://github.com/aeonfun/aeon/pull/955))
- Added opt-in network egress auditing ("iron-proxy") to log and inspect outbound calls from a run. ([#947](https://github.com/aeonfun/aeon/pull/947))

*Internal: 17 commits hidden (README/docs sync, CI lint gates, asset cleanup, tests). Bots filtered: 0.*

---

## aeonfun/minitor

> **Highlights:** No user-facing changes this week; 2 internal commits.

*Internal: 2 dependency bumps. Bots filtered: 2 (dependabot).*

---

## aeonfun/opendia

> **Highlights:** No user-facing changes this week; 1 internal commit.

*Internal: 1 commit (dropped a redundant dependency-version override). Bots filtered: 0.*
