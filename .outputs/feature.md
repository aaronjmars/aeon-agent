*Feature Built — 2026-04-23*

Fork Skill Digest
Aeon now has a third lens on its fork fleet: a weekly digest that surfaces *where the configured forks systematically disagree with upstream defaults*. If most operators turn a skill on that ships off, or pick a cheaper model than the one upstream ships with, this digest flags it as a candidate for upstream to flip — converting fleet behavior into actionable upstream recommendations every Sunday.

Why this matters:
The fork-intelligence stack already had two lenses — `skill-leaderboard` (what's *popular*) and `fork-fleet` (what *unique work* each fork is doing) — but neither answered "where has the fleet voted differently than the defaults we ship?" That's the peer-learning gap. Operators have been making individual enable/disable/model decisions in the dark for months; this turns those individual decisions into a fleet signal. Memory had this flagged as one of the two highest-priority unbuilts coming out of the Apr-21/22 sprint (Apr-22 repo-actions idea #2).

What was built:
- `skills/fork-skill-digest/SKILL.md`: New 14-step weekly skill. For each skill in upstream, computes four divergence dimensions (enabled, var, model, schedule) against every configured fork, then classifies each into at most one bucket: `DEFAULT_FLIP_ENABLE` (>=50% turn on what upstream defaults off), `DEFAULT_FLIP_DISABLE` (>=50% turn off what upstream defaults on), `MODEL_CONSENSUS` (>=2 forks share an alternative model), `VAR_HOTSPOT` (>=2 forks share a non-default var value), or `EMERGING` (25-49% adoption watchlist).
- Per-fork customization fingerprint: top 5 heaviest customizers ranked by total override count, each tagged with a dominant category lean (e.g. "content-heavy: 14 article/digest skills enabled, 3 model overrides to claude-sonnet-4-6").
- Fork-only skill enumeration: lists `skills/<name>/SKILL.md` paths that exist in a fork's tree but not in upstream — surfaces fork experiments worth reviewing for upstreaming.
- `aeon.yml`: registers the skill on Sunday 18:30 UTC (after the 17:00 cluster of skill-leaderboard / skill-graph / fork-contributor-leaderboard) using `claude-sonnet-4-6` for cost optimization, matching sibling weekly skills.
- `README.md`: Meta/Agent skills table count bumped 13->14.

How it works:
The skill resolves the target repo from `${var}` or `memory/watched-repos.md`, snapshots upstream defaults from the local `aeon.yml`, then enumerates active forks (pushed in last 30 days) via `gh api ... /forks` with pagination. For each active fork it makes one recursive `git/trees` call (cheaper than per-path contents) plus one `aeon.yml` fetch. Each fork is tiered as `CONFIGURED` (any divergence from upstream defaults), `TEMPLATE` (untouched), or `UNREADABLE` — the divergence math runs only against the configured denominator, so a 30-fork fleet of 28 templates and 2 configured doesn't drown out the signal. State persists to `memory/topics/fork-skill-digest-state.json` for week-over-week deltas (NEW_FLIP / STRENGTHENED / FADED / NEW_FORK_ONLY / NEW_HEAVY_CUSTOMIZER) — the article never drives deltas, the JSON is the contract. Notification fires only when N_CONFIGURED >= 2 AND at least one signal bucket is non-empty (silent runs are correct, not failures), following the autoresearch-evolution gate pattern. All API calls go through `gh api` so `GITHUB_TOKEN` auth works inside the sandbox; rate-limit hits trigger a 60s backoff with one retry, partial-fleet runs degrade gracefully and surface the gap in the source-status footer.

What's next:
First production run is Sunday 2026-04-26 at 18:30 UTC — that establishes the baseline state file so subsequent weeks get week-over-week deltas. The aeon-agent fork (this running instance) is itself one of the configured forks the digest will see. Only one Apr-22 highest-priority unbuilt remains: Smithery + MCP Registry Submission (idea #1) — that one requires external registry PRs and is harder to verify autonomously, so it's the next candidate for the operator to gate.

PR: https://github.com/aaronjmars/aeon/pull/140
