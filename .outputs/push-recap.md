*Push Recap — 2026-06-02*
3 repos · ~12 PRs merged in 24h · ~30 substantive commits

*Capability declarations go live (aeon):* 19 high-blast-radius skills got `capabilities:` frontmatter (#322) — every onchain investigator, every key-spender. Same day, the audit skill (#313, merged 6/1) shipped a fix (#319) for the bootstrap state where nobody had declared anything yet — was crying 6 fake gaps; now goes QUIET until first real declaration lands.

*Skill-marketplace registry entry (aeon):* PR #316 adds Atrium-Hermes/aeon-atrium-skills — 3 onchain Base/USDC skills (atrium-publish/scout/earnings). 8th community pack in `skill-packs.json`.

*Daily PR-queue digest (aeon):* PR #318 ships `pr-merge-queue` — buckets every open PR by touched-file risk tier (CORE_REVIEW > INFRA > SKILL > FAST_TRACK). Reuses scan.sh verbatim. Operator-facing only — no merge action.

Key changes:
- 19 SKILL.md capability declarations (+19 lines, single line each, zero risk)
- `skills/pr-merge-queue/SKILL.md` new (+288)
- aeon-agent: 19th-consecutive backport — follow-up-patrol from upstream PR #272 (#76, +175)
- minitor: per-column quick-search (#58, +222/-6) + same-day TS fix on yesterday's collapsed strip (#57, -2)

Stats: 12+ PRs · ~900 net lines · 3 ECOSYSTEM.md entries (HivemindOS / Echo Oracle / SyntheticsAI link refresh)
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-06-02.md
