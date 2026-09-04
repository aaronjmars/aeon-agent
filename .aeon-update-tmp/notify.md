⭐ *aeon-update — 2026-09-04*

synced 22 upstream commits → PR, all green.

`aeonfun/aeon` `3b4c5a3..bf33365`. 30 files applied clean, 10 need your hand. baseline advances to `bf33365` on merge.

the gist: notify per-channel status, fleet-scorecard no longer leaks non-skill runs into reliability, vuln-scanner PoC gate + deploy-uni-hook template fixes, block-style per-skill `model:` scheduler fix (#1024).

one snag worth knowing: upstream bumped the eyebrow gate to v0.4.2 and it now checks content hashes — the old "verify tolerates drift" assumption is dead. first push went red. fixed by refreshing 5 lock entries from upstream HEAD (byte-identical skills only, no binary run) after proving 72/72 hash-compat. green now.

held back: `skill-health` (#1018 recovery detection) — clean merge but needs an eyebrow rescan i can't run here. surfaced, not shipped.

your call: merge, or reconcile the 10 conflicts (workflows + CHANGELOG carry the GLM_REASONING_EFFORT / PoC-gate wiring; 2 package.json are cosmetic-only; `aeon.yml` gains a `dev-loop` chain).

PR: https://github.com/aaronjmars/aeon-agent/pull/220
