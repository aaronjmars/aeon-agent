*Push Recap — 2026-06-03*
aeon + aeon-agent + minitor — ~19 substantive PRs by 7+ authors

*ECOSYSTEM.md overhaul*: Logo column landed (aeon #327) and seven batched PRs (#328–#333) backfilled 100% logo coverage for the table in a single evening. Five X-handle corrections (Clerk, Liq, RootAi, Gitlawb, Precog) and USIC→MANAGR rename rode along; Careful Finance row removed; docs updated for the new row format (#334). README ecosystem is now a visual catalog instead of a name list.

*Atrium onchain marketplace closes its loop* (aeon #335): new `install-from-atrium` Bash CLI fetches skills from atriumhermes.tech/.well-known/skills/, runs them through the same scan.sh as `./add-skill`, records onchain CID as commit_sha in skills.lock. Pairs with yesterday's PR #316 (Atrium-Hermes skill-pack). Aeon now has three skill-install paths (add-skill / install-skill-pack / install-from-atrium) all converging on the same scanner + lockfile schema.

*ecosystem-entrants skill* (aeon #339, +289 lines, weekly Mon 11:45 UTC, disabled): diffs ECOSYSTEM.md against prior snapshot, surfaces added/removed entries as a discrete signal. Pairs with ecosystem-pulse (liveness, 11:00 UTC) — pulse watches the living projects, entrants watches the door. Deterministic primary_url resolution (GitHub → X → first link → name) prevents link-order swaps from faking add/remove churn.

Key changes:
- aeon ecosystem table: 4 new entries (Reppo, VIGIL, Atrium, Sparkleware), 5 handle fixes, 1 rename, full logo backfill across 40+ rows
- aeon-agent: 20th consecutive same-day-after backport — pr-merge-queue (PR #79, +315 skill, daily 09:45 UTC operator-facing PR-queue digest bucketed by touched-file risk tier, reuses scan.sh verbatim)
- minitor #59: per-column pin-to-front toggle (+530, 11 files, DB migration 0007). 5th rung on the column-density UX ladder (tabs May-29 → collapse May-30 → JSON export May-31 → quick-search Jun-02 → pin today). DB-backed because pin is a persistence choice; DnD across pin/unpin is intentionally no-op
- aeon-agent #77: repo-pulse self-fix — 4th `$(date ...)` anti-pattern site removed (after weekly-shiplog, push-recap, heartbeat). Three sites remain
- aeon #336: test glob widened to include .test.ts via tsx loader (Raeli Savitt, devDep tsx 4.22.4)

Stats: ~19 substantive PRs · ~2,400 net lines · aeon (15) / aeon-agent (3) / minitor (1)
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-06-03.md
