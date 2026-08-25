✅ aeon-update → PR #198

**aeon-update — 2026-08-25**
synced 25 upstream commits → PR [#198](https://github.com/aaronjmars/aeon-agent/pull/198)

`aeonfun/aeon` `b7a909a..8b8d719`. 51 files applied clean (10 add, 36 update, 5 auto-merged). baseline advances on merge.

headline: **#912 phase-2 secret hardening** — channel delivery moved to a post-run dispatcher, dead channel creds no longer bind into every skill's env. plus egress-audit action, eslint+shellcheck gates, fx harness dispatch fix, and the OpenAI/MiniMax/Kiro plugin manifests.

**needs you (13):**
- 2 new skills held back (`rightstack`, `skill-article`) — can't run eyebrow/catalog gen in-sandbox, so shipping them would go CI-red. one-line manual step in the PR.
- 10 conflicts — mostly six→seven / 75→77 count bumps colliding with this fork's own numbers. the one that matters: `.github/workflows/aeon.yml` (the phase-2 secret rework lands here, over your narrowed env block).
- `aeon.yml` default toggle to eyeball.

`messages.yml` resolved itself via 3-way this run (pending since #193). merge #198 and the watermark moves.

🔗 https://github.com/aaronjmars/aeon-agent/pull/198