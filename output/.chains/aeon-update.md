✅ aeon-update: 19 commits synced → PR #229

⭐ *aeon-update — 2026-09-21*
synced 19 upstream commits → PR

`aeonfun/aeon` was 19 commits ahead (`95142d1..ba01e9f`). 36 files applied clean — 6 new, 28 updated, 2 auto-merged 3-way. baseline moves to `ba01e9f` when you merge.

shipped in: dev-loop proof/repair stack + ci-gate, `vuln-scanner` disclosure hardening, reflected-XSS fix on the mcp-auth callback, mcp-server riva isolation.

left for you (14): new skills `sc-audit` + `create-prove` need a generator + `eyebrow scan` on install — can't run headless. overlap conflicts on `aeon.yml`-wf, `ci-tests.yml`, `README`, `CHANGELOG`, `docs/skill-packs`. `aeon.yml` also gains an `sc-audit` entry + dev-loop `max_dispatches: 2→5` — merge by hand.

catalogs + eyebrowlock untouched on purpose: every updated skill is byte-identical to upstream, drift allowed, gates green.

PR: https://github.com/aaronjmars/aeon-agent/pull/229

🔗 https://github.com/aaronjmars/aeon-agent/pull/229