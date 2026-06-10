*Thread Draft — 2026-06-10*
Topic: Aeon crossing 500 stars — auto-trigger, rename, and rule-map coordination in one day

1/ Aeon crossed 500 stars this morning. The auto-trigger was wired to fire show-hn-draft when the counter hit that number. By evening, the skill had been renamed. The rule map was updated in the same PR.

2/ The mechanism was three separate PRs over three days. Jun 8: star-milestone got a rule map seeded with aeon:500 → show-hn-draft. Jun 9: six lines in the draft updated the framing — from 250 stars to 497, 90 skills to 195. Jun 10: the stars crossed.

3/ PR #427 renamed 30 three-word skill slugs to two tokens. show-hn-draft became show-hn. The same PR updated milestone-dispatch.json so the 500-star trigger pointed at the right name. One diff. No broken trigger.

4/ The upstream Aeon workflow has been disabled_manually since March 19. Every PR this week — capabilities-sweep, MCP gateway, README banners — was manually authored. The auto-trigger fired into a window the operator was actively working in by hand.

5/ The trigger, the milestone, the rename. Same repo, same day. https://github.com/aaronjmars/aeon

(article: articles/thread-2026-06-10.md)
