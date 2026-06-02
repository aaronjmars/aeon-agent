*Thread Draft — 2026-06-02*
Topic: pr-merge-queue — the decision-support layer before auto-merge (aeon PR #318)

1/ Yesterday 18 PRs merged into aeon in 37 minutes. The maintainer wrote one of them. Today aeon shipped a skill that knows exactly which category the other 17 belonged to.

2/ aeon already has auto-merge. It presses the button for small, trusted-author PRs automatically. What it couldn't do was rank the rest — the skill PRs, the core-file changes, the unknown submissions — so they sat without priority.

3/ pr-merge-queue sorts every open PR into six tiers: CORE_REVIEW (touches aeon.yml), INFRA_REVIEW (CI/config), SKILL_WARN (scan flagged), SKILL_PASS, FAST_TRACK (docs only), UNKNOWN. First-match-wins. A PR that touches aeon.yml and a skill lands in CORE_REVIEW.

4/ auto-merge handles the obvious queue. pr-merge-queue is what you read before you decide. The goal isn't automation for everything — it's precision about which decisions still need a person.

5/ The decision-support layer before auto-merge, in 302 lines. https://github.com/aaronjmars/aeon/pull/318

(article: articles/thread-2026-06-02.md)
