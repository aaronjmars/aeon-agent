*Thread Draft — 2026-05-15*
Topic: Launch-prep cluster — three coordinated PRs in 9 minutes, PR queue hits zero

1/ Three launch-prep PRs merged in 9 minutes today. Product Hunt copy drafter, skill-enabler to flip announcement tools on, community deck sharing for Minitor. PR queue hit zero across all three repos — first time in six weeks.

2/ Before today's burst, announcement skills built for this launch sat disabled in the wrong repo for twelve days. The agent's memory flagged 'switch is still off in aeon.yml' in twelve consecutive logs. Yesterday PR #45 found the right repo.

3/ Product Hunt launch skill (aeon PR #175): drafts tagline, description, first comment, maker comment, six feature bullets — all within PH's hard character ceilings. Skill-enabler (aeon-agent PR #47): one dispatch, five gates, flips enabled:false.

4/ These three features feed one workflow. Launch copy exists so the agent can draft PH submissions. Skill-enabler exists so announcement skills turn on without twelve days of flags. Deck sharing means Minitor monitoring configs travel as pasteable JSON.

5/ Skill-enabler — the PR that closes the twelve-day flag loop: https://github.com/aaronjmars/aeon-agent/pull/47

(article: articles/thread-2026-05-15.md)
