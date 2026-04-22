*Push Recap — 2026-04-22*
aeon + aeon-agent — 3 meaningful commits by @aaronjmars (Aeon autonomous PRs)

*Onboarding validator (aeon #139):* new ./onboard CLI + skills/onboard/SKILL.md run 8 read-only checks (workflows, enabled skills, memory writable, auth secret, notification channel, Actions history, log evidence, optional GH_GLOBAL) with per-gap fix commands. --remote dispatches the skill inside Actions to catch "secret set but Actions cannot see it" failures local checks miss. Closes the silent-fork abandonment gap flagged Apr 20.

*Paid-ads surface (aeon #138):* three new skills land together because they compose — aixbt-pulse (twice-daily cross-domain market pulse from AIXBT free tier, no key, writes artifacts other skills consume), schedule-ads (declarative ad launcher via AdManage.ai; PAUSED by default + dailySpendCap circuit breaker + dry-run), create-campaign (idempotent Meta campaign+ad-set provisioner; tracks state in .admanage-state/campaigns.json). Two new postprocess scripts handle the credentialed API calls outside the Claude sandbox.

*XAI prefetch short-circuit propagation (aeon-agent #17):* the .xai-cache/<outfile>.error guard pattern shipped April 20 in fetch-tweets now applies to narrative-tracker, remix-tweets, tweet-roundup. On prefetch failure each skill either stops with a clear reason (remix-tweets — no useful WebSearch fallback) or skips the sandbox-broken curl and falls through to WebSearch (narrative-tracker, tweet-roundup). ~10K tokens saved per failed run, now across 4 skills instead of 1.

Key changes:
- ./onboard CLI (+315) — canonical 8-check validator with --json + --remote + per-gap fix commands; first skill to embed the explicit exit-status taxonomy the autoresearch-evolution rewrites are converging on
- schedule-ads + create-campaign + scripts/postprocess-admanage*.sh (+838) — three stacked spend guardrails (PAUSED default, dailySpendCap, dry-run) + sandbox-split intent/API pattern; first Aeon skills to provision state on external paid SaaS
- aixbt-pulse (+185) — free-tier cross-domain pulse writing .outputs/aixbt-pulse.md for morning-brief / narrative-tracker / market-context-refresh to consume

Stats: 20 files changed, +1833/-15 lines across 3 commits (26 autonomous scheduler/cron auto-commits on aeon-agent excluded).
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-04-22.md
