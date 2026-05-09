# Long-term Memory
*Last consolidated: 2026-05-06*

## About This Repo
- Autonomous agent running on GitHub Actions via Claude Code
- Linked to Telegram group — daily skills post repo state, content, and token updates

## Tracked Token
| Token | Contract | Chain |
|-------|----------|-------|
| AEON  | 0xbf8e8f0e8866a7052f948c16508644347c57aba3 | base |

## Recent Articles
*(Entries before 2026-05-01 archived to `memory/topics/articles-history.md`)*
| Date | Title | Topic |
|------|-------|-------|
| 2026-05-01 | Aeon Wrote Its Own Application to the Agent Registry | repo-article |
| 2026-05-01 | Self-Hosting Used to Mean a Compiler. Now It Means an Agent. | project-lens |
| 2026-05-02 | Aeon Just Started Shipping Features To A Product That Isn't Itself | repo-article |
| 2026-05-02 | A Fortune 500 Just Found 347 AI Agents It Didn't Know It Had | project-lens |
| 2026-05-03 | Watching the Whole Federated Web Without an API Key | repo-article |
| 2026-05-03 | Termites Built Cathedrals Without Holding Standups. Most Multi-Agent Systems Still Can't. | project-lens |
| 2026-05-04 | Aeon Built a Skill For Bugs That Don't Crash | repo-article |
| 2026-05-04 | The 1976 Theory That Already Named Why Your AI Agent Will Disappoint You | project-lens |
| 2026-05-05 | Aeon Built the Stopwatch For Its Own Launch | repo-article |
| 2026-05-05 | The 2026 Agent Stack Has Five Layers. Most Comparisons Are About One. | project-lens |
| 2026-05-06 | Aeon Wrote The v4 Migration Guide Two Weeks Before v4 Lands | repo-article |
| 2026-05-06 | Sixty-One Percent of Unpaid Maintainers Are Alone. Their Repo Doesn't Have to Be. | project-lens |
| 2026-05-07 | Aeon Built the Skill Template Library Its Forks Were Reverse-Engineering | repo-article |
| 2026-05-08 | The AI Stack Has Three Layers. Aeon Built A Skill For Each One — And A Dashboard Column Too. | repo-article |

## Recent Digests
| Date | Type | Key Topics |
|------|------|------------|
| 2026-03-25 | Polymarket | Geopolitics dominates; US-Iran escalation at 58.5% YES |

## Skills Built
*(Rows before 2026-05-03 archived to `memory/topics/skills-history.md`)*
| Skill | Date | Notes |
|-------|------|-------|
| operator-scorecard | 2026-05-03 | Weekly Monday 10:30 UTC sonnet — three-paragraph synthesis (agent health / community growth / economic activity), worst-of-three verdict 🟢/🟡/🔴 mirroring heartbeat P-flags. Every number from a file another skill wrote (aeon PR #153) |
| cron-state (script) | 2026-05-03 | Local viewer for memory/cron-state.json; --skill, --unhealthy (exits 1), --stale [hours] (exits 1), --json modes. Useful when gh api rate-limited or sandbox-blocked (aeon-agent PR #27) |
| mastodon-column (minitor) | 2026-05-03 | 32nd column type. Keyless Mastodon REST API; hashtag + author modes. HTML strip, federated handle parsing, reblog filter, CW prefix. #6364ff accent (minitor PR #26) |
| skill-freshness (aeon) | 2026-05-04 | Daily 08:00 UTC. Walks enabled skills' file deps, checks freshness per class (articles 28h/192h · .outputs 4h · topics 7d · state 30d). OK/WARN/STALE/MISSING bands. Fingerprint dedup 7d re-emit. Closes silent-staleness gap (aeon PR #157) |
| operator-scorecard (aeon-agent) | 2026-05-04 | Backport of aeon PR #153 + heartbeat-only fallback so forks without skill-analytics don't permanently report WATCH (branch B: OK if p0==0 AND p1==0 AND ok≥5). Merged PRs #28 + #29 |
| lobsters-column (minitor) | 2026-05-04 | 34th column type. Keyless lobste.rs JSON API; Hottest/Newest/Active/Tag modes. Tag pills, anchor icon, #ac130d accent (minitor PR #27) |
| star-momentum-alert (aeon) | 2026-05-05 | Daily 10:10 UTC. Projects next milestone via 7d rolling star average. Alert gates: 7-14d out AND Tue/Wed/Thu. Per-(repo,milestone) dedup 7d re-emit. Pairs with show-hn-draft (aeon PR #159) |
| skill-freshness (aeon-agent) | 2026-05-05 | Verbatim backport of aeon PR #157 (aeon-agent PR #30) |
| polymarket-column (minitor) | 2026-05-05 | 35th column type. Gamma API keyless; trending/newest/ending-soon/tag modes. 5 integration quirks (JSON-string outcomes parse, binary leading-outcome sort, price clamp 0..1, past-dated drop, event-slug permalink). #2D9CDB accent (minitor PR #28) |
| token-report (volume trend) | 2026-05-06 | Adds 24h vol % trend + 7d/30d avg vol to token-report output and notification (aeon-agent PR #31) |
| xai-prefetch max_output_tokens | 2026-05-06 | Raises max_output_tokens to 16384 in xai_search helper. Trigger: May-6 cache truncated at 7,354 tokens (6,486 reasoning), delivering 2 tweets instead of 10+. Affects 5 skills sharing the helper (aeon-agent PR #32) |
| v4-readiness (aeon) | 2026-05-06 | Workflow_dispatch one-shot. Reads aeon.yml + skills.json + MEMORY.md vs embedded v4 change manifest. Emits Safe/Review/Custom/Action breakdown with effort tags. Read-only, manifest-in-SKILL.md travels per-fork (aeon PR #160) |
| stack-overflow-column (minitor) | 2026-05-07 | 36th column type. Keyless Stack Exchange API 2.3; hot/votes/newest/week/month modes; optional 1–5 tag AND-filter (commas/spaces normalised to `;`). Accepted-answer badge, #F48024 brand orange, HTML-entity decoded titles. Plugin + 3 registry edits + integration helper (minitor PR #29) |
| skill-template-library (aeon) | 2026-05-07 | Closes activation gap for fork operators. `templates/` with 6 starters (crypto-tracker, research-digest, code-reviewer, social-monitor, deploy-watcher, community-manager) — each runnable SKILL.md with `[REPLACE: KEY]` tokens. `./new-from-template` CLI: --list, --tokens, --var KEY=VALUE; sed-substitutes (escapes `\&\|`), registers disabled entry in aeon.yml. Carried unbuilt from Apr-18 ideas (aeon PR #161) |
| huggingface-column (minitor) | 2026-05-08 | 37th column type. Keyless HF Hub REST API; 3 resources (models/datasets/spaces) × 3 sorts (trending/most-likes/newest) + search. First plugin to use the `ai` ColumnCategory (declared in types.ts since plugin-system shipped, no consumer until now). Schema-drift safe across the 3 resource types (models lack `author`+`lastModified`, datasets have both, spaces have no `downloads`). Plugin + 3 registry edits + integration helper. README adds AI/ML cluster row, count 36 → 37 (minitor PR #30) |
| huggingface-trending (aeon) | 2026-05-08 | Daily 09:30 UTC sonnet — curated trending HF models/datasets/spaces, mirroring github-trending's contract for the AI artifact layer. Six noise filters (test/debug, gated low-signal, trivial fine-tunes, 3d re-features, quantization-only forks <500 likes, broken/scaffold spaces); ≤18-word "why notable" gate per pick; momentum tags (DEBUT/ACCELERATING/RETURNING/HOLDOVER); 5-bucket cluster cap; single Top pick. Slots between paper-pick (theory, 14:00) and github-trending (code, 09:00) — completes the AI ecosystem daily-movement triple (aeon PR #162) |
| xai-prefetch truncation warning | 2026-05-08 | Companion observability fix to May-6 PR #32 (raised max_output_tokens to 16384). Parses `.usage.output_tokens` post-call; emits `::warning::xai-prefetch: <file> output_tokens=N (reasoning=R) within 5% of max_output_tokens=16384` when cap is approached. Surfaces both raw output and `output_tokens_details.reasoning_tokens` so operator can tell whether reasoning or output is the squeeze. Heartbeat + skill-runs --failures already pick up GH annotations. Pulls 16384 into a `local` for single-source-of-truth (aeon-agent PR #33) |
| contributor-spotlight (aeon) | 2026-05-09 | Weekly Sunday 20:00 UTC sonnet — recognition post for one POWER fork from latest fork-cohort run. 11-step skill with 8-status exit taxonomy, 4-week dedup state in `memory/topics/contributor-spotlight-history.json` (capped 26 entries ≈ 6 months), POWER → ACTIVE fallback, bot+parent filter, operator-authored skills starred ★. Recognition-paragraph contract enumerates required facts and forbids inventing motivations or copying commit messages verbatim (per CLAUDE.md untrusted-content rule). Closes the gap between "we have fork data" (fork-cohort PR #152) and "we do something social with it" — the social loop side of fork-contributor-leaderboard. Picked from May-8 ideas idea #4 (aeon PR #163) |
| skill-update-check backport (aeon-agent) | 2026-05-09 | Synced local v1 (flat catalog of SHAs) → upstream variation B: CRITICAL/HIGH/MEDIUM/LOW priority triage classified by drift_size × security verdict × aeon.yml ENABLED state, raw-accept-header SKILL.md fetch (avoids multiline base64 corruption), atomic skills.lock writes with `jq empty` validation, ACCEPT mode (`var=accept:{skill_name}`) for one-off operator-confirmed lock advancement, frontmatter-diff detection, breaking-change keyword scan, full security-scanner fallback. Diff +201/-100. Most-leveraged backport because every other skill drift becomes legible through it. skills.json bumped 57 → 58 (skill-update-check entry was missing entirely). May-8 idea #5 (aeon-agent PR #34) |
| arxiv-column (minitor) | 2026-05-09 | 38th column type. First academic-paper surface in the lineup; AI/ML cluster row count 1 → 2. Keyless arXiv Atom-XML query API (`export.arxiv.org/api/query`) — 12 CS / stat / math.OC categories, 2 sort modes (newest submission / recently updated), optional title+abstract keyword filter ANDed onto the category. Three integration quirks: (1) URLSearchParams escapes `+` to `%2B` but arXiv requires literal `+` as AND in `search_query=`, so query string built manually; (2) revision badge dual-redundant — `vN` suffix where N>1 OR `updated > published + 60s`; (3) PDF link extracted via `<link title="pdf">` pattern (arXiv-specific). #B31B1B Cornell-red accent, BookOpen icon. Plugin + 3 registry edits + integration helper. Companion to huggingface (#30, May-8) — together they cover artifact-to-research AI pipeline. May-8 idea #1 (minitor PR #31) |

## Lessons Learned
- Digest format: Markdown with clickable links, under 4000 chars
- Always save files AND commit before logging
- Polymarket Gamma API: use volume_num_24hr sort for signal; newest markets are mostly noise
- GITHUB_TOKEN cannot push workflow file changes — needs `workflows` permission (PAT or fine-grained token)
- Self-improve outpaces review: agent opens PRs faster than human merges. PR awareness guard stops at 3+ open PRs
- fetch-tweets dedup: persistent seen-file + SHA256 notify layer + per-run delta + scheduler catch-up gate — three dedup layers stack end-to-end
- aeon-agent still at pre-autoresearch-evolution SKILL.md versions (aeon PRs #46–#136 not yet backported) — SKIP_UNCHANGED/NEW_INFO exits, significance gates not active here
- grok-4-1-fast is a thinking model — reasoning trace eats output tokens before answer list; always set max_output_tokens ≥ 16384 in xai_search calls (triggered May-6: 2 tweets instead of 10+)
- tweet-allocator Bankr prefetch: empty `verified-handles.json` had three ambiguous causes — resolved by `.error` marker (aeon-agent PR #24)

## Repo Actions Ideas Pipeline
~65 ideas generated (14 runs). Recently built: skill-freshness (May-4), star-momentum-alert (May-5), polymarket-column (May-5), v4-readiness (May-6), stack-overflow-column (May-7), skill-template-library (May-7), huggingface-column + huggingface-trending + xai-prefetch warning (May-8), contributor-spotlight + skill-update-check backport + arxiv-column (May-9). May-9 burned 3 of the 5 May-8 ideas (#1 arxiv, #4 contributor-spotlight, #5 skill-update-check backport). May-8 unbuilt: #2 DEV.to column (minitor), #3 ai-framework-watch (aeon). May-6 article was stale on aeon side: idea #1 star-milestone already exists (PR #39 + autoresearch PR #111), idea #2 Reddit column for minitor already exists. Open unbuilts: Auto-Merge Agent PRs (needs workflows-scope PAT), Dashboard Live Feed, Webhook-to-Skill Bridge. Remaining backports for aeon-agent: fork-cohort, v4-readiness, thread-formatter (May-6 #3/#4/#5). See `articles/repo-actions-*.md`.

## Next Priorities
- Enable star-milestone in aeon aeon.yml — already exists upstream (PR #39 + autoresearch PR #111); aeon at 278⭐ (May-7) — flip enabled:true so the 300⭐ crossing is announced
- Enable star-momentum-alert in aeon.yml — shipped `enabled: false` PR #159 (May 5); first alert window opens ~May 7-8 (projection: 300⭐ ~4 days out)
- Enable thread-formatter in aeon.yml — first use is 300-star milestone (276⭐ now, ~24 from target); PR #148 (Apr 30)
- Enable show-hn-draft in aeon.yml — dispatch when stars approach 300 (currently 276⭐, ~24 from milestone); PR #151 (May 1)
- Enable pr-triage in aeon.yml — PR #147 (Apr 29); PR #143 from pezetel is first natural triage candidate
- Build Auto-Merge Agent PRs (Apr-26 idea #1) — needs workflows-scope PAT first
- Enable smithery-manifest in aeon.yml — PR #149 (May 1); submit docs/ to Smithery + MCP Registry
- Enable fork-cohort in aeon.yml — PR #152 (May 2); gives "X of 43 forks running in production" social proof
- Enable operator-scorecard in aeon.yml — PR #153 (May 3); weekly scorecard
- Enable skill-freshness in aeon.yml — PR #157 (May 4)
- Enable operator-scorecard in aeon-agent aeon.yml — PR #28 (May 4); first Monday run May 11
- Enable skill-freshness in aeon-agent aeon.yml — PR #30 (May 5)
- Enable v4-readiness in aeon aeon.yml — PR #160 (May 6); dispatch manually pre-v4-announcement
- Backport to aeon-agent: fork-cohort (#3), v4-readiness (#4), thread-formatter (#5) per May-6 ideas; also 80 autoresearch-evolution rewrites (aeon PRs #46–#136)
- Run more digest types (HN, RSS, papers, DeFi)
- Fix token permissions: need PAT with `workflows` scope for workflow + topics admin-scope writes
