*Push Recap — 2026-06-22*
aaronjmars/aeon + aeon-agent + minitor — SHIPPING — phylax-audit gates external skill installs; docs-sync auto-publishes changelogs

Shipped to users:
• phylax-audit (aeon #537): new skill from external contributor Phylax — takes any skill ref or URL, runs static prompt-injection scan + Base contract audit + x402 probe, returns ALLOW/WARN/DENY before ./add-skill runs
• docs-sync (aeon-agent #110): new daily skill (08:00 UTC) — fetches merged PRs from the product repo, writes a changelog entry, opens a draft PR on the website repo; idempotent by PR number, bootstrap path creates the full /changelog surface on first run

Under the hood:
• aeon: pruned dangling refs to 3 defunct skills across 15+ SKILL.md files (#531); README count fixed 182→183 (#530)
• aeon-agent: git identity now --global so cross-repo commits don't fall back to unlinked email (#114); skill-runs --hours validated before reaching date arithmetic (#112)
• minitor: 5 Grok columns now reject blank search queries with a clear error instead of an opaque API failure (#78)

Shape: 2 user-visible · 8 internal · 1 infra · 42 bot-filtered · 11 human merged PRs
Volume: ~20 files, ~+600/−126 lines

Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-06-22.md
