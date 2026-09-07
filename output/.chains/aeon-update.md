✅ aeon-update: PR #221

**aeon-update ⭐ — synced 7 upstream commits → PR #221**

canon shipped 7, we pulled them down. 17 files applied clean, 2 workflows need a hand-merge.

what landed:
- send-email: delivery preflight — checks prior sends for bounces before firing (#1033)
- pr-review: verified review receipts, trivial PRs get an approve-ready receipt not a skip (#1027)
- vuln-scanner: trufflehog git-history scan bounded, no more phantom-success runs (#1030)
- dry-run: explicit claude/codex model selection (#1029)
- deploy-uni-hook: price/balance/skew gates anchored to the pool's own price, not an implicit 1.0 (#1031)

eyebrowlock reconciled without running the binary — 4 skill entries swapped verbatim from upstream's v0.4.2 lock, byte-identical content so it's deterministic. catalogs untouched (body-only edits, nothing semantic moved). CI's green.

manual bit: `.github/workflows/aeon.yml` — #1032 binds `RESEND_API_KEY` in the secret-injection step, the functional half you want for Resend. overlaps your narrowed secrets block, so it's yours to merge.

baseline moves to `21b82db` when you merge.

PR: https://github.com/aaronjmars/aeon-agent/pull/221

🔗 https://github.com/aaronjmars/aeon-agent/pull/221