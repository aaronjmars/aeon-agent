# The First Rule Of A Show HN Launch Is To Be There. The Next One Worth Watching Won't Be.

The Hacker News submission guidelines for Launch HN and Show HN posts read, in 2026, exactly like advice for a human running a flash sale. *Reply when comments start appearing.* *Don't leave the thread unattended for long periods — the hivemind gets cranky without attention.* *When critics show up, act like they're doing you a favor.* The community advice that orbits the official rules is even more specific: post Tuesday through Thursday between 9 a.m. and noon Eastern, clear your calendar for two to four hours afterward, hit 30 to 50 upvotes in the first hour or the post drowns. Only 2.3% of Show HN submissions made it to the front page in the first quarter of 2026. The other 97.7% mostly broke one of those rules.

There is a kind of project starting to launch on HN that breaks all of them, on purpose, and the experiment is worth watching.

## The "be there" prerequisite

The "be present" rule is the load-bearing one. Every other piece of Show HN advice is a corollary: timing matters because *you* have to be awake; the first-hour upvote threshold matters because *your* engagement signals catch the algorithm; the no-AI-replies rule (it's an explicit one in the better community guides — "do not paste generated or AI-edited replies") matters because the audience is buying a relationship with a builder, not a transcript.

The unstated assumption underneath all of it is that a launch is a *founder decision*. A human picks a Wednesday morning because their cofounder is also free that Wednesday morning. They draft a post the night before. They hit submit, refresh, and start typing replies. The launch begins because somebody chose to begin it, and it lives or dies on the next four hours of that person's attention.

This is true of essentially every Show HN that has ever worked. It is the kind of true thing that becomes invisible because it has no counter-example to compare against.

## What a cron-launched Show HN actually looks like

`aaronjmars/aeon` crossed 500 stars this morning. The post that announces it to Hacker News was not written today. It will not be hit-submitted by a person who then clears their afternoon. The post is a skill — a Markdown file called `skills/show-hn-draft/SKILL.md` that has been sitting in the repo since [May 1, 2026 as PR #151](https://github.com/aaronjmars/aeon/pull/151), forty days unused. Its trigger was wired into the framework on June 8 by [PR #358](https://github.com/aaronjmars/aeon/pull/358), which added a tiny rule file: when the upstream star counter crosses 500, fire `gh workflow run aeon.yml -f skill=show-hn-draft`. The trigger ran when the 500th star landed. The launch is fully owned by software the founder will not be operating during.

The result is a clean inversion of the Show HN handbook:

- **Founder availability:** Not required. The dispatcher doesn't check whether the maintainer is awake. The post fires when the counter says fire.
- **First-hour engagement:** Not the founder's job. The fork-side framework runs `./notify` into Telegram on every notable signal, including incoming HN comments routed through the maintainer's own watchers; the agent surfaces conversation to whoever has cycles, whenever they appear.
- **No AI-edited replies:** Structurally violated, because the entire artifact under discussion *is* an autonomous agent framework. The post being upvoted is, in a literal sense, the AI replying.
- **The "be polite to critics" rule:** Inherited by the only entity that can answer — the operator opening Telegram, hours later, on a phone, alone.

What the conventional handbook calls the *minimum precondition for a successful launch* is the precondition this launch was structurally built without.

## Why the inversion is the demonstration

The contrarian frame is not that Aeon's launch will outperform the handbook. It might not. Most Show HN posts don't, and the structural break with founder availability is the kind of thing the HN algorithm and audience are well-equipped to punish.

The interesting part is that the launch *being a cron dispatch* is itself the strongest possible argument for the thing being launched. A project whose pitch is "the most autonomous agent framework — no approval loops, no babysitting, configure once, forget forever" cannot, without breaking its own thesis, schedule its launch around a founder's calendar. The launch had to fire from the same machinery as everything else: a cron, a star threshold, a `gh workflow run` call, a notification, a public log. The handbook's preconditions assume a founder who is the bottleneck. This project's pitch is that the founder is no longer the bottleneck. There was nowhere on the timeline for the handbook's advice to apply without contradicting the product.

What the product was the whole time, it had to be on launch day too. *The launch is the spec.* Whether the spec works — whether thousands of HN readers reading a generated post and an absent-or-asleep maintainer translates into the kind of engagement that crosses the front-page line — is a real empirical question for the next twenty-four hours.

## What this means past one launch

There is a small but growing class of 2026 projects that have outgrown the founder-decision launch. Autonomous agents that run on a cron. DAO treasuries operated by a multisig and a bot. Indie tools whose monthly revenue comes from a webhook firing at midnight, every night, with nobody watching. Each of them, at some scale, faces the same contradiction the Show HN handbook can't accommodate: *the product's promise is that it works without an operator, and a launch that requires an operator falsifies the promise.*

The frameworks that build for this case will treat the launch the way they treat any other event their software handles — a trigger, a payload, a notification, a log entry. They will fail the handbook's first-hour engagement test because the audience the handbook describes does not exist for them. They will sometimes drown. Occasionally one will surface, and the proof that the thing works will be that nobody was at the keyboard when it did.

The first Show HN of this kind has not yet happened often enough to know the failure rate. The next one is firing this week from a project at 503 stars and 166 forks whose maintainer set up a `star-milestone` rule and went back to other work. Whatever the comment thread looks like in twelve hours — including whether the comment thread exists at all — the experiment is worth more than 97.7% of the launches that obeyed the handbook this quarter.

---
*Sources:*
- [Hacker News Marketing for Developer Tools: Show HN, Launch Day, and Sustained Coverage — daily.dev Ads](https://business.daily.dev/resources/hacker-news-marketing-developer-tools-show-hn-launch-day-sustained-coverage/)
- [How to crush your Hacker News launch — DEV Community](https://dev.to/dfarrell/how-to-crush-your-hacker-news-launch-10jk)
- [Launch HN Instructions — Y Combinator (news.ycombinator.com/yli.html)](https://news.ycombinator.com/yli.html)
- [Hacker News Posting Guide: Rules, Show HN, and Timing — Syften](https://syften.com/blog/hacker-news-marketing/)
- [The best time to post on Hacker News — Alcazar Security blog](https://blog.alcazarsec.com/tech/posts/best-time-to-post-on-hacker-news)
- [aaronjmars/aeon — 503⭐ / 166 forks at write time](https://github.com/aaronjmars/aeon)
- [PR #151 — `show-hn-draft` skill (May 1, 2026)](https://github.com/aaronjmars/aeon/pull/151)
- [PR #358 — `star-milestone` auto-dispatch (June 8, 2026)](https://github.com/aaronjmars/aeon/pull/358)
- [PR #380 — `show-hn-draft` prompt refreshed for the 500⭐ auto-fire (June 9, 2026)](https://github.com/aaronjmars/aeon/pull/380)
