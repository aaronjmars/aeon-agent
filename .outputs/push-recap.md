*Push Recap — 2026-04-17 (updated)*
aaronjmars/aeon + aaronjmars/aeon-agent — 35 meaningful commits by @aaronjmars and aeonframework

Fork ↔ Upstream Sync: aeon upstream absorbed fork-side resilience work (miroshark's fetch-tweets pipeline, eval-audit coverage tool, XAI 429 retry, GH_GLOBAL token fallback). Aeon-agent mirrored back upstream polish — tags frontmatter across 48 skills (100% coverage on shared skills), sandbox notes, path fixes.

Opus 4.7 Upgrade: default model bumped from 4.6 → 4.7 across aeon.yml, workflows, README, dashboard picker, and cost-report pricing. Secret forwarding fix (DEVTO/NEYNAR/VERCEL/BANKR) patches a silent-failure class where new integration skills were calling WebFetch with unset Bearer tokens.

fetch-tweets Stabilization: 11 commits in aeon-agent to fix dedup being too aggressive, Grok false positives (bare-word "aeon" matches), cache pollution, and non-persistent seen-lists. New post-filter script drops tweets without exact cashtag/handle/URL match. Persistent seen-file (58-URL seed) survives log rotation.

tweet-allocator Rewrite: Bankr wallet is now the single gate — no unverified/pending paths. Simplified from +144/-57 to a straight-line "log → exclude → Bankr → pay" flow. Successfully paid 10 verified handles today.

Key changes:
- New scripts/eval-audit (272 lines, Python) on aeon — generates eval stubs for uncovered skills
- Telegram notify moved to HTML parse mode (fixes underscore-eating in handles like BioStone_chad)
- 14 scratch files (634 lines) purged from aeon-agent; .gitignore standardized across both repos
- skill-graph PR #38 merged on upstream aeon — Mermaid map of 91 skills

Stats: ~90 files changed, +2,200/-1,000 lines across 35 meaningful commits (plus ~40 auto-commits).
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-04-17.md
