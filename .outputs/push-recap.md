*Push Recap — 2026-06-16*
aaronjmars/aeon — SHIPPING: one-click community-pack install now lands skills on `main` and shows them in the dashboard.

Shipped to users:
• minitor #74 — new github-commits TweetDeck column (repo-velocity feed, keyless or token; +248)
• aeon #483 — community pack cards get an "Install pack" button + new `install-skill` core skill that opens a PR; skills land disabled
• aeon #485/#486/#487/#490/#491/#493 — six fixes that close the install loop: Actions can open+auto-merge the PR on a fresh fork, installed skills land in an always-visible "Installed" pack, packs.json regenerates deterministically, pack visibility is per-repo so forks start Core-only

Under the hood:
• aeon #471 SECURITY.md (disclosure policy + threat model); new catalog entries glim.sh #470, Robinhood MCP #489, Hunch betting pack #472 — two external contributors

Shape: 13 user-visible · 3 internal · 4 infra · 35 bot-filtered · 19 merged PRs
Volume: ~105 files, +1,341/−469 lines

Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-06-16.md
