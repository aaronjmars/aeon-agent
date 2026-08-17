Good — the workflow auto-commits `memory/` changes on the current repo after the run (`chore(...): auto-commit`). No manual commit needed from me. The task is complete.

## Summary

Ran the `changelog` skill in **push-to mode** (`push-to:aaronjmars/aeon-website`), which matched the existing `memory/docs-sync.md` config (product `aaronjmars/aeon`, website `aaronjmars/aeon-website`) exactly.

- Scanned the 7-day window (2026-08-10 → 2026-08-17) on the product repo: 7 merged PRs, but 6 (#871, #865, #869, #866, #868, #863) were already published on the website in the 2026-08-15 entry — only **#873** (an in-repo docs-sync catch-up PR) was new, matching `min_prs: 1`.
- Prepended a new `2026-08-17` entry ("In-repo docs catch up to Aug 10 batch") to `app/changelog-data.ts` on `aaronjmars/aeon-website`.
- Verified with `npx tsc --noEmit` (clean) and `npm run build` (succeeds; one pre-existing, unrelated `@farcaster/mini-app-solana` warning inside `@privy-io/react-auth`, untouched by this change).
- Opened draft PR: **https://github.com/aaronjmars/aeon-website/pull/251**
- Logged the run under `### changelog` in `memory/logs/2026-08-17.md` (per skill spec, no `./notify` call — this skill is silent).

One sandbox adaptation: `/tmp` was outside this instance's allowed working directories, so the website clone went to `.sw-tmp/docs-sync-work` inside the repo tree instead of the skill's default `/tmp/docs-sync-work`. It's untracked and left in place (no `rm` tool available) — harmless, won't be committed.
