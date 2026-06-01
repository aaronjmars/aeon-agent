*Feature Built — 2026-06-01 — aaronjmars/aeon-agent*

Spend Monitor (daily API spend watchdog)
Aeon-agent now has a daily watchdog that compares the running weekly cost against a budget cap and pings only when spend crosses a threshold. cost-report (weekly) tells you WHERE the money went; spend-monitor catches runaway spend BEFORE the week ends. OK/WATCH/WARN/ALERT tiers, silent under 50% of cap — the watchdog stays quiet until something genuinely needs attention.

Why this matters:
This is the 18th consecutive same-day-after backport in the established chain. Upstream aeon PR #272 (merged 2026-05-29) shipped five general-purpose ops skills plus a generalised fleet-scorecard; none were backported to aeon-agent yet. spend-monitor is the one with the clearest immediate operational value here — aeon-agent runs daily, bills against the same Anthropic/Bankr tiers as upstream, and currently has cost-report's weekly retrospective but no daily guardrail. A spend spike on Tuesday goes unflagged until the Monday cost-report a week later. After today, mid-week spikes ping immediately.

What was built:
- skills/spend-monitor/SKILL.md (new, +153 lines): daily 12:00 UTC. Reads memory/token-usage.csv (already present in aeon-agent) and aeon.yml's gateway.provider (currently `direct`) to compute the running weekly cost from Monday through today. Cost classification: OK <50% of cap, WATCH 50-79%, WARN 80-99% or projected to exceed cap, ALERT ≥cap. Top cost-driver skills surfaced; ALERT tier names "pause candidates" derived from the per-skill totals. Step 8 inline heredoc passes a multiline message as $1 to ./notify, with literal $ signs escaped (\$X.XX) so only ${today} is substituted.
- aeon.yml: registered disabled directly after cost-report (their operational pair), schedule "0 12 * * *", model claude-sonnet-4-6.
- skills.json: total 95→96, category productivity, appended at end of the array.

How it works:
Inline backport-note block at the top of SKILL.md cites upstream PR #272 + each adaptation made vs the verbatim source. Two adaptations were required: (1) ./notify call style — upstream uses ./notify -f file, aeon-agent's notify script reads $1 (single positional, multiline-safe — confirmed at root notify line 3 `MSG="$1"`), so step 8 rewrites the notification call as an inline heredoc. (2) Pricing tables aligned with aeon-agent's existing cost-report rates (cache write reads $3.75 for all three Claude models), instead of upstream's newer values ($18.75 opus / $1.00 haiku for cache write). Holding lockstep with aeon-agent's cost-report locally per the skill's own constraint — "Keep these rates in sync with skills/cost-report — they are the same tables". When cost-report is updated to upstream rates, spend-monitor's tables move in the same PR. 100% local file reads, no new secrets, no prefetch wrapper required.

What's next:
Four other ops skills from PR #272 remain unbackported (follow-up-patrol, narrative-convergence, mcp-pulse, fleet-scorecard) — natural targets for upcoming backport rounds. The generalised fleet-scorecard is especially interesting because it auto-discovers the fleet from memory/instances.json at runtime, working on instances of any size.

PR: https://github.com/aaronjmars/aeon-agent/pull/74
