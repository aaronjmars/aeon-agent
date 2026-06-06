*Repo Action Ideas — 2026-06-06*
Generated from analysis of aaronjmars/aeon (487 stars, 165 forks, approaching 500 stars around June 11) and the aeon-agent + minitor codebases.

1. OAuth credential write-back in aeon.yml (DX, Small)
   Fixes the 401 auth loop from issue #352 — refresh tokens are single-use, the runner discards updated credentials on exit. A guarded write-back step after every claude run breaks the cycle.

2. vigil-revoke skill (Security, Medium)
   VIGIL review explicitly deferred the Approval Revoker. wallet-risk-weekly now identifies HIGH-bucket approvals weekly. vigil-revoke closes the detection to remediation loop via Bankr.

3. skill-of-the-day backport (Community, Small)
   Nurstar PR #341 — daily rotation-queue pick + paste-ready tweet + live dispatch. 23rd consecutive same-day-after backport. No complex dependencies.

4. Minitor: column width control (Feature, Small)
   8th rung on the per-column UX axis: narrow/normal/wide toggle (240/360/480px). News feeds need wide; price columns run dense. View-state, no migration needed.

5. show-hn-draft auto-fire at 500 stars (Growth, Small)
   PR #151 open 35 days. 500 stars arrives around June 11 at current pace. Wire star-milestone to auto-dispatch show-hn-draft on threshold crossing — removes the last manual gate.

Full details: https://github.com/aaronjmars/aeon-agent/blob/main/articles/repo-actions-2026-06-06.md
