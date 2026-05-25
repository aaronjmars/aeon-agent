*Push Recap — 2026-05-24*
12 substantive PRs across aeon (7), aeon-agent (3), minitor (1) + ~22 cron auto-commits. ~8,260/-108 lines, 6 distinct authors.

Skill catalog explosion: aeon's evening of May 23 absorbed 34 derivative-instance skills back into upstream (catalog now 155), added ECOSYSTEM.md (39-project table for products built on Aeon), bundled 4 community packs into the README, merged the machine-readable skill-packs.json registry. Three registries now formally separate forks (SHOWCASE), pack authors (skill-packs.json), and product builders (ECOSYSTEM.md).

AntFleet two-model bench sweep: antfleet-ops opened 3 PRs in 60 seconds on aeon — workflow_dispatch shell injection (High), GATEWAY tr-d parse error (High), notify-dedup-hash-before-delivery silent message loss (Medium). All from claude-opus-4-7 + gpt-5 unanimous review on aeon-bench PR #31. None merged yet.

Bot's autonomous cycle: aeon PR #226 closes last open AntFleet High on v4-readiness (silent false-clean READY now structurally unreachable); aeon-agent PR #59 combined backport of install-skill-pack CLI + skill-packs.json registry (12th same-day-after in a row); aeon-agent PR #60 self-corrective response to today's own XAI 403 outage (5-variant PREFETCH_FAILED notification routing); minitor PR #49 per-column refresh intervals (last open May-22 idea consumed).

Key changes:
- aeon PR #219 ported 34 skills (+6,162/-69, 36 files), dropped 3 duplicates, merged auto-merge-agent-prs retry-cap into auto-merge
- aeon PR #220 ECOSYSTEM.md splits products-built-on-Aeon from forks + skill packs (39-project alphabetized table)
- minitor PR #49 per-column refresh intervals (+513/-2, 10 files) — column-row level field, never reaches plugin fetchers, all 47 plugins keep working unchanged

Stats: ~70 files changed, +8,262/-108 lines across 12 substantive PRs
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-24.md
