*Push Recap — 2026-06-24*
aaronjmars/aeon · aaronjmars/minitor · aaronjmars/aeon-agent — SHIPPING — phylax security screen, dashboard docs, and minitor column guards

Shipped to users:
• skill-triage now inline-runs phylax-audit's onchain + endpoint scan on any incoming skill that references a Base contract or payment endpoint — pure-prompt skills skip it, DENY → BLOCK in the triage receipt (#544)
• apps/dashboard finally has a README: quickstart, six views, config, and the loopback security gate — the last sub-app doc gap closed (#543)
• 4 minitor social columns (linkedin, bluesky, mastodon, youtube) now throw a clear "input required" error before firing a wasted upstream call; template documents the pattern for future columns (#79, #80)

Under the hood:
• feature skill and repo-actions skill both hardened against repeat failure modes — compound-bash trap documented in the skill most likely to hit it, and a runtime-boundary check stops infeasible bash→LLM-gate ideas from ranking as Top Pick (#115, #116)

Shape: 4 user-visible · 2 internal · 0 infra · ~52 bot-filtered · 6 merged PRs
Volume: 21 files, +409/-24 lines

Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-06-24.md
