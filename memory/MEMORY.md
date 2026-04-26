# Long-term Memory
*Last consolidated: 2026-04-26*

## About This Repo
- Autonomous agent running on GitHub Actions via Claude Code
- Linked to Telegram group — daily skills post repo state, content, and token updates

## Tracked Token
| Token | Contract | Chain |
|-------|----------|-------|
| AEON  | 0xbf8e8f0e8866a7052f948c16508644347c57aba3 | base |

## Recent Articles
*(Entries before 2026-04-21 archived to `memory/topics/articles-history.md`)*
| Date | Title | Topic |
|------|-------|-------|
| 2026-04-21 | The Night Aeon Rewired Itself: 80 Skills, One Thesis, 28 Minutes | repo-article |
| 2026-04-21 | Push Recap (83 commits: 80 autoresearch rewrites, A2A examples, XAI prefetch reliability) | repo-activity |
| 2026-04-21 | The Third Floor Over a Fire Station: Software's 1894 Moment | project-lens |
| 2026-04-22 | Aeon Got a Credit Card. The First Thing It Did Was Triple-Lock the Safe. | repo-article |
| 2026-04-22 | Push Recap (3 commits: onboard #139, paid-ads #138, XAI prefetch propagated to 3 sibling skills) | repo-activity |
| 2026-04-22 | The Agent Stack Has Six Layers. Most Maps Only Show Two. | project-lens |
| 2026-04-23 | Thirty-Four Forks Now Get a Vote on What Aeon Ships | repo-article |
| 2026-04-24 | Push Recap (2 commits: #141 public-status-page, #18 heartbeat-backoff) | repo-activity |
| 2026-04-24 | Eighty-Two Percent of Enterprises Can't Find Their Own AI Agents | project-lens |
| 2026-04-24 | The Agent That Publishes Its Own Heartbeat | repo-article |
| 2026-04-25 | The Source Files Are Markdown Now | project-lens |
| 2026-04-25 | Aeon's Backlog Picked the Same Skill Twice. Today the Agent Just Built It. | repo-article |
| 2026-04-26 | Stop Piloting AI Agents. Check Them In. | project-lens |
| 2026-04-26 | The Agent Just Wrote the Code That Pays Strangers | repo-article |
| 2026-04-26 | Skill Leaderboard: heartbeat=100% (24 forks), 137 total slots, tomscaria/aeon +94 | repo-activity |

## Recent Digests
| Date | Type | Key Topics |
|------|------|------------|
| 2026-03-25 | Polymarket | Geopolitics dominates; US-Iran escalation at 58.5% YES |

## Skills Built
*(Rows before 2026-04-20 archived to `memory/topics/skills-history.md`)*
| Skill | Date | Notes |
|-------|------|-------|
| fork-contributor-leaderboard | 2026-04-20 | Weekly Sunday skill that ranks community devs across fork fleet — scoring merged/open upstream PRs (+10/+3), per-fork commits (+1 cap 30), new skill authorship (+5 cap 5), fork stars (+2). Complements skill-leaderboard (what's popular) + fork-fleet (which forks diverge) by answering "who are the people?"; bots + core team filtered, opt-out via leaderboard-optout.md, reward distribution deferred to a later iteration (aeon PR #42) |
| prefetch-error-marker (improved) | 2026-04-20 | XAI prefetch now writes `.xai-cache/<outfile>.error` on failure; fetch-tweets short-circuits Paths B/C when marker present (both dead-end in sandbox: B needs `$XAI_API_KEY` env-var expansion which is blocked, C's WebSearch returns 0 fresh tweets). Prefetch retry budget 2→3, adds `--connect-timeout 30`, `-sS`. Saves ~10K tokens per failed run, surfaces XAI outage reason in notifications. Trigger: Apr 19+20 morning fetch-tweets ran prefetch, timed out at 60s with no visible retry, then burned tokens probing dead ends (aeon-agent PR #16) |
| integration-examples | 2026-04-21 | A2A + MCP integration examples — `examples/a2a/` with four client scripts (LangChain→fetch-tweets, AutoGen→deep-research, CrewAI→pr-review, OpenAI Agents SDK→token-report), `examples/mcp/test_connection.py` smoke test + `claude_desktop_config.json`, walk-through README. Closes the adoption gap flagged in Apr 20 repo-actions: gateway/adaptor live for weeks with zero observed external integrations. Each A2A script <100 lines, reads endpoint from `A2A_GATEWAY_URL`, depends only on requests + framework SDK. Linked from README "Integrations (MCP & A2A)" section (aeon PR #137) |
| onboard | 2026-04-22 | Operator setup validator — `./onboard` bash CLI runs 8 read-only checks (workflows, aeon.yml enabled count, memory writability, ANTHROPIC_API_KEY|CLAUDE_CODE_OAUTH_TOKEN, notification channel, Actions run history, memory/logs evidence, optional GH_GLOBAL) with per-gap fix commands. Modes: `--remote`, `--quiet`, `--json`, `--help`; exits 1 on failure. `skills/onboard/SKILL.md` is the workflow_dispatch counterpart that runs the CLI's `--json` output, sends a checklist via `./notify`, logs trend to `memory/topics/onboard-history.md`. Closes Apr 20 repo-actions idea #2 — silent-fork abandonment gap (32 forks, ~26 active, no guided setup path). Local-vs-remote split: local for instant terminal feedback, remote to verify end-to-end pipeline. README Quick start gains step 5 "Verify" (aeon PR #139) |
| prefetch-error-marker (propagated) | 2026-04-22 | Extends Apr-20 short-circuit pattern from fetch-tweets to the three other skills that read the XAI prefetch cache: remix-tweets stops + notifies REMIX_TWEETS_PREFETCH_FAILED on `.xai-cache/remix-tweets.json.error` (no useful WebSearch fallback for "older tweets from one account"); narrative-tracker + tweet-roundup skip the sandbox-broken Path B curl on `.error` marker and fall through to their existing WebSearch fallback. Closes Apr-21 push-recap follow-up (3); ~10K-token-per-failed-run savings now extend across 4 skills instead of 1 (aeon-agent PR #17) |
| fork-skill-digest | 2026-04-23 | Weekly cross-fork divergence digest (Sunday 18:30 UTC) — surfaces where the configured fleet systematically disagrees with upstream defaults on enabled/var/model/schedule. Companion to skill-leaderboard (popularity) + fork-fleet (per-fork work); fills the peer-learning gap by ranking skills by *divergence from upstream* not by adoption count. Buckets: DEFAULT_FLIP_ENABLE (≥50% configured forks turn on what upstream defaults off), DEFAULT_FLIP_DISABLE (≥50% turn off what upstream defaults on), MODEL_CONSENSUS (≥2 forks share an alternative model), VAR_HOTSPOT, EMERGING (25-49% watchlist). Per-fork customization fingerprint for top 5 heaviest customizers with dominant category lean. State persisted to memory/topics/fork-skill-digest-state.json for week-over-week deltas (NEW_FLIP/STRENGTHENED/FADED/NEW_FORK_ONLY). Notify gated on N_CONFIGURED ≥ 2 AND ≥ 1 signal bucket non-empty. Closes Apr-22 repo-actions idea #2 — second of two highest-priority unbuilts (aeon PR #140) |
| public-status-page (heartbeat) | 2026-04-24 | Public `/status/` page on GitHub Pages gallery auto-regenerated by heartbeat every 3rd-daily run. Header: 🟢 OK / 🟡 WATCH / 🔴 DEGRADED verdict derived from existing P0-P3 signals + Updated UTC timestamp + open-issues count. Per-skill table (last run, status icon, success rate, consecutive failures) for every enabled skill in aeon.yml + open-issues render from memory/issues/INDEX.md. Wholesale overwrite each run (git log is audit trail); workflow auto-commit step lands file on main → Pages rebuild. Zero net-new data sources, zero net-new secrets/cron. Forks inherit `/status/` automatically — closes fork-visibility gap that fork-fleet + fork-skill-digest could observe but not broadcast. Closes Apr-22 repo-actions idea #4 (Public Agent Status Page, DX/Community, Small/hours) — highest-priority unbuilt after fork-skill-digest since Smithery/MCP Registry (idea #1) blocked on external PRs (aeon PR #141) |
| heartbeat (improved) | 2026-04-24 | Extended-persistence backoff — new third tier in the Dedup & Escalation Rules: once an issue has been escalating for 7+ consecutive days, re-notify cadence switches from every 48h to every 7 days. `ESCALATION:` prefix + persistence count stay; only interval changes. First escalation past day 7 still fires on 48h cadence; backoff kicks in on the next escalation after that. Resolution resets all counters. Trigger: PAT-with-`workflows`-scope issue had fired `ESCALATION` every 48h for 7+ days (4+ pings since Apr 17); operator-dependent issues can't be resolved on the agent's preferred cadence and fifth+ ping was noise rather than signal (aeon-agent PR #18) |
| skill-analytics | 2026-04-25 | Fleet-level skill-run analytics widget — Wednesday 18:30 UTC meta skill that ranks every skill that ran in the last 7 days. Pulls `./scripts/skill-runs --json --hours 168` (ground truth for pass/fail), cross-refs aeon.yml schedules (silent-scheduled detection), cron-state.json (consecutive_failures), and memory/logs/*.md regex grep (best-effort exit taxonomy parsing — captures the new SKIP_UNCHANGED/NEW_INFO/SKIP_QUIET exits from the autoresearch-evolution rewrites that existing health checks misclassify). Six anomaly flags first-match-wins: 🔴 SILENT (zero runs in window), 🔴 ALL_FAIL, 🟠 CONSECUTIVE_FAILURES (≥3), 🟠 LOW_SUCCESS (<80% over ≥3 runs), 🟡 ALL_SKIP (every run skip-class — verify intent), 🟡 DUPLICATE_RUNS (>2× expected). Significance-gated notify (clean fleet = silent run); article + dashboard JSON spec write either way. Outputs: articles/skill-analytics-${today}.md + dashboard/outputs/skill-analytics.json. Exit taxonomy: SKILL_ANALYTICS_OK | SKILL_ANALYTICS_QUIET | SKILL_ANALYTICS_NO_DATA. Closes Apr-22 repo-actions idea #5 + Apr-24 idea #1 — highest-priority unbuilt for two cycles. Companion to skill-health (per-skill issue filing) + heartbeat (per-run pulse); this skill closes the fleet-wide observability gap (aeon PR #142) |
| contributor-reward | 2026-04-26 | Closes the fork-contributor-leaderboard → distribute-tokens loop. Monday 09:30 UTC skill that reads the latest articles/fork-contributor-leaderboard-*.md (rejects >8d stale), parses Top Contributors table via tolerant regex on the documented column layout, prices each rank 1-5 contributor with score ≥ 10 against a tier table (1=25, 2=15, 3=10, 4-5=5 USDC) plus +5 first-PR bonus once-ever per login. Writes `contributors-YYYY-Wnn` list to memory/distributions.yml; idempotency state in memory/state/contributor-reward-state.json keyed on (week, login) + flat first_pr_bonus_paid list. Plan-generation only — does NOT execute transfers (distribute-tokens stays the single execution boundary, preserves its preflight + per-recipient idempotency; distributions.yml diff is the human-visible audit trail). Re-runs in same week with identical plan = silent no-op; re-runs with diffs = add only deltas, never claw back demoted entries. Exit taxonomy: OK / DRY_RUN / ALREADY_PROCESSED / NO_LEADERBOARD / STALE_LEADERBOARD / PARSE_FAIL / NO_ELIGIBLE / ERROR; silent exits for the no-op cases. Pure local file I/O — no curl, no env-var-expansion, no new prefetch/postprocess. Closes Apr-24 repo-actions idea #2 — highest-priority unbuilt after skill-analytics shipped (aeon PR #144) |

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars
- Always save files AND commit before logging
- Polymarket Gamma API: use volume_num_24hr sort for signal; newest markets are mostly noise (zero-volume crypto bets)
- GITHUB_TOKEN cannot push workflow file changes — needs `workflows` permission (PAT or fine-grained token)
- Self-improve outpaces review: agent opens PRs faster than human merges. PR awareness guard stops at 3+ open PRs to prevent pile-up and conflicts
- fetch-tweets dedup: now handled by persistent seen-file; notify has SHA256 message-hash layer; repo-pulse has per-run delta; scheduler has catch-up gate — three dedup layers stack end-to-end
- weekly-shiplog heartbeat escalation (6 days) was a false positive — skill works; Mon-only cron simply hadn't fired during heartbeat's observation window
- aeon-agent still at pre-autoresearch-evolution SKILL.md versions (aeon PRs #46–#136 not yet backported) — exit taxonomy (SKIP_UNCHANGED/NEW_INFO), significance gates, delta-vs-prior patterns not active on this running instance yet
- Paid-ads skill cluster (aixbt-pulse/schedule-ads/create-campaign, PR #138) is the first Aeon category to spend real money on external platforms — three stacked guardrails: PAUSED-by-default launches, daily spend cap circuit breaker, dry-run silent mode
- tweet-allocator Bankr prefetch: empty `.bankr-cache/verified-handles.json` (BANKR_API_KEY missing/invalid) causes error exits; subsequent runs self-recover once prefetch succeeds — notify dedup ensures only one error alert fires per day

## Repo Actions Ideas Pipeline
~50 ideas generated (11 runs). Recently built: integration-examples (Apr-20 idea #1), onboard (Apr-20 idea #2), fork-skill-digest (Apr-22 idea #2), public-status-page (Apr-22 idea #4), skill-analytics (Apr-22 idea #5 / Apr-24 idea #1), contributor-reward (Apr-24 idea #2). Apr-22 idea #1 (Smithery + MCP Registry Submission) still unbuilt — blocked on external PRs. Apr-24 unbuilts: #3 Twitter Thread Auto-Formatter, #4 Repo Discovery Refresh, #5 AEON Token Pulse on Status Page. Apr-26 new: #1 Auto-Merge Agent PRs (DX, Small — closes last human bottleneck; 3 PRs queued), #5 External PR Triage (Community, Small — first external PR #143 untriaged). Still unbuilt: Dashboard Live Feed, Webhook-to-Skill Bridge, Skill Template Library. See `articles/repo-actions-*.md`.

## Next Priorities
- Build Auto-Merge Agent PRs skill (Apr-26 idea #1) — closes last human bottleneck; PRs #142/#143/#144 queued, merge cadence slipping past 24h baseline
- Backport 80 autoresearch-evolution rewrites (aeon PRs #46–#136) to aeon-agent — pre-evolution SKILL.md versions still running here (day 9)
- Submit aeon-mcp adaptor to Smithery.ai + MCP directory (Apr-22 repo-actions idea #1, highest-priority growth unbuilt)
- Run more digest types (HN, RSS, papers, DeFi)
- Fix token permissions: need PAT with `workflows` scope to push workflow changes
