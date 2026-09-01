*aeon-update — 2026-09-01*
synced 34 upstream commits → PR #209 ⭐

`aeonfun/aeon` went 34 commits ahead this week (08-26 → 08-31). pulled 91 files clean, 8 need your eyes. all 17 CI checks green.

highlights:
- new skill: `cortx-reliability` (x402 endpoint reliability check)
- **`rightstack` + `skill-article` finally landed.** the 08-25 sync held them back because eyebrow couldn't run in-sandbox. ran it this time — sha-pinned v0.4.1 binary, scrubbed env, scan + verify both clean, catalogs regenerated in-branch. the sync loop repaired its own repair loop
- cursor + hermes harness adapters shipped upstream; GLM moved from harness to the claude AI gateway, tiered model mapping (`GLM_MODEL_SONNET/OPUS/HAIKU`)
- mcp-server single-flight queue, telegram reply-to-previous-skill-run, envelope fail-on-garbage

manual (8): `scripts/llm-gateway.sh` + `messages.yml` are the real ones — your `b054cb0` emergency GLM pin from the outage overlaps upstream's proper implementation. upstream's is a superset; take it. rest is carried README/CHANGELOG/workflow drift.

PR: https://github.com/aaronjmars/aeon-agent/pull/209
