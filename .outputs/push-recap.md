*Push Recap — 2026-06-17*
aeon · aeon-agent · minitor — SHIPPING: pack validator, PR template & CONTRIBUTING land across all three repos

Shipped to users:
• `validate-pack.sh` (aeon #495) — 282-line pre-flight validator running the exact invariants `install-skill-pack` enforces (manifest, slugs, paths, capability taxonomy); pack authors now catch rejections before a reviewer does
• PR template (aeon #494) — `.github/PULL_REQUEST_TEMPLATE.md` with a four-way "type of change" split + per-type checklists, shown on every PR
• minitor CONTRIBUTING (#75) — 66-line column-plugin walkthrough: Node 20+, PGlite bundled, `git clone && ./minitor`
• tweet-digest now tracks @aeonframework daily (aeon-agent #105)

Under the hood:
• Repaired tweet-digest prefetch so scheduled runs stop hitting an empty cache in the sandbox (aeon-agent #107); content-filter fix unblocks CODE_OF_CONDUCT.md on aeon (#100)

Shape: 4 user-visible · 2 internal · 0 infra · 25 bot-filtered · 6 merged PRs
Volume: ~20 files, +735/-17 lines

Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-06-17.md
