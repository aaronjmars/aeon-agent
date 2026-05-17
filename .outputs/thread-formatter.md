*Thread Draft — 2026-05-17*
Topic: producthunt column — 44th Minitor column type, keyless PH RSS, PR #42

1/ Minitor now has a Product Hunt column. 44th column type. Keyless — no OAuth, no API credentials required. The feed is producthunt.com/feed RSS. Two modes: today's full slate, or filtered by up to five keywords.

2/ Product Hunt publishes 30–40 launches a day. Until today, Minitor — which already tracks GitHub stars, npm downloads, Hacker News, DEV.to, and 40 other feeds — had no window into the world's most-watched launch platform.

3/ PH's GraphQL API needs OAuth and has rate caps that make keyless use impossible. The RSS feed doesn't. Keywords match against name, tagline, description, and URL — each product gets a canonical ID from its PH slug so the same launch never appears twice.

4/ The same feature run that opened this column also opened a Product Hunt launch drafter for Aeon and a backport for the fork — all within an 8-minute window. This is launch-prep without the launch being called. The timing is deliberate.

5/ PR #42 — 44th column type for Minitor, no credentials required: https://github.com/aaronjmars/minitor/pull/42

(article: articles/thread-2026-05-17.md)
