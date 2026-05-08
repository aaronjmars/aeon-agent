# Push Recap — 2026-05-08

## Overview
3 substantive commits across aeon and minitor in the 24h window (15:34 UTC May 7 → 15:34 UTC May 8). The day's main thrust was a coordinated Hugging Face Hub surface — same morning, same content domain, two delivery channels: an aeon skill that ships a curated daily digest, and a minitor column that renders the same data live in a deck. A long-stalled fork-author PR fixing reply-maker's sandbox path also landed overnight. aeon-agent saw no substantive commits — only the usual cron auto-commits from the scheduler.

**Stats:** 15 files changed, +751 / −8 lines across 3 substantive commits (excluding 32 cron auto-commits in aeon-agent).

---

## aaronjmars/aeon

### Theme 1: Hugging Face Hub coverage — the AI artifact layer joins paper-pick + github-trending
**Summary:** aeon already had `paper-pick` (one daily HF Papers pick) and `github-trending` (curated trending repos). What it didn't have was a skill for the artifact layer — the models / datasets / spaces that ship alongside (and frequently before) the paper or HN post. PR #162 closes that gap with the same curation contract github-trending uses: filter the noise on the HF front page, require a one-line "why notable" per pick, tag momentum, cluster into capped buckets, lead with one Top pick.

**Commits:**
- `9c36154` — feat: add huggingface-trending skill — curated trending HF artifacts (#162)
  - New `skills/huggingface-trending/SKILL.md` (+179 lines): full 9-step skill. Pulls keyless from `/api/{models,datasets,spaces}?sort=trendingScore`, applies six noise filters (test/debug, low-signal gated, trivial fine-tunes, 3-day re-features, quantization-only forks under 500 likes, broken/scaffold spaces), requires a ≤18-word "why notable" line per survivor, tags momentum (DEBUT/ACCELERATING/RETURNING/HOLDOVER), clusters into 5 capped buckets, picks a single Top pick. Sandbox-safe — curl + WebFetch fallback, no prefetch needed (keyless API). Four-status exit taxonomy: `HF_TRENDING_OK` / `_QUIET` / `_ERROR` / `_BAD_VAR`.
  - `aeon.yml` (+1 line): registered `enabled: false, schedule: "30 9 * * *", model: claude-sonnet-4-6` — slots in right after github-releases (09:30 UTC) so the morning AI/dev block lands as one batch.
  - `skills.json` (+14, −2): bumped total 111 → 112; new research-category entry.
  - `generate-skills-json` (+1 line): added `huggingface-trending` to the research case so future regenerations stay in lockstep.
  - `README.md`: Research & Content cluster row count 17 → 18.

**Impact:** When enabled, an operator running aeon now gets a curated daily slate of where the AI ecosystem's attention moved across all three layers — papers (theory) → repos (code) → HF Hub (artifacts). Slots between paper-pick (14:00 UTC) and github-trending (09:00 UTC) without overlap. Ships disabled by default, like all new skills.

### Theme 2: Reply-maker's sandbox-blocked runtime curl path finally fixed
**Summary:** `scripts/prefetch-xai.sh` had cases for `tweet-roundup` and `narrative-tracker` but not for `reply-maker`. The reply-maker SKILL.md still led with a `curl https://api.x.ai/v1/responses -H "Authorization: Bearer $XAI_API_KEY"` that the sandbox blocks (env vars in headers don't expand inside the runtime), so reply-maker had no way to consume Grok x_search results in CI — every run fell straight through to the WebSearch/memory fallback. PR #156 was opened May 3 by tomscaria (a fork operator), sat unreviewed for ~102 hours, and was flagged by heartbeat as the single stalled fork-author PR every day. Merged overnight.

**Commits:**
- `795a5a1` — fix(reply-maker): wire XAI prefetch case + cache-read path (#156)
  - `scripts/prefetch-xai.sh` (+21, −0): adds a `reply-maker)` case mirroring the SKILL.md contract — numeric `${VAR}` → X list ID, `@`-prefixed → handle (with `allowed_x_handles` filter), anything else → topic. Empty var skips cleanly so the skill falls through to its memory/WebSearch fallback. Calls the shared `xai_search` helper with the right query shape per branch.
  - `skills/reply-maker/SKILL.md` (+12, −2): documents Path A (read `.xai-cache/reply-maker.json`) as preferred, Path B (direct curl) as skipped under sandbox. Renumbers fallback chain so the cache-read sits at position 1. Updates the Sandbox note to say outright "do not attempt direct curl to api.x.ai at runtime."

**Impact:** Closes the sixth shared-helper consumer of the prefetch-xai pattern (after fetch-tweets, refresh-x, remix-tweets, tweet-roundup, narrative-tracker, article). reply-maker can now actually return reply candidates from CI instead of always degrading to memory + WebSearch. Also clears heartbeat's open stalled-PR notification — the only one in the queue going into May 8.

---

## aaronjmars/minitor

### Theme 3: 37th column type is Hugging Face — first consumer of the dormant `ai` category
**Summary:** Minitor's column system has carried an `ai` `ColumnCategory` in `types.ts` since the plugin system shipped, with no consumer until now. PR #30 lands the Hugging Face column as the 37th type and the first to populate that category. Three resource modes (models / datasets / spaces) × three sort modes (trending / most-likes / newest), optional substring search filter, brand chip in HF yellow `#FFD21F` with the 🤗 mark.

**Commits:**
- `a48938b` — feat(plugins): add huggingface column type — trending models, datasets, spaces (#30)
  - `lib/integrations/huggingface.ts` (NEW, +202 lines): typed fetcher for `/api/{models,datasets,spaces}?sort=trendingScore&direction=-1&limit=50`. Schema-drift safe — HF list responses for **models** omit `author` (packed into `id` as owner/name) and `lastModified`; **datasets** include both; **spaces** omit `downloads`. The mapper falls back gracefully on each shape and still produces a complete card. Per-resource permalink builder: `/{id}` for models, `/datasets/{id}`, `/spaces/{id}` (avoids relying on absent fields). Slice-based pagination matching the documented `paginate.ts` trade-off the rest of the plugins use.
  - `lib/columns/plugins/huggingface/plugin.ts` (NEW, +56): zod schema for `{resource, mode, search}`; `HuggingfaceMeta` includes `pipelineTag`, `libraryName`, `sdk`, `gated`, `tags`, `trendingScore`. Brand color set to HF yellow with a comment explaining the choice.
  - `lib/columns/plugins/huggingface/server.ts` (NEW, +36): server-side fetch routing.
  - `lib/columns/plugins/huggingface/client.tsx` (NEW, +218): ConfigForm renders Resource select, Sort select, Search input. ItemRenderer drops `region:`/`license:` tag noise, switches descriptor under the title (pipeline tag for models, library or sdk for datasets+spaces, falls back to the resource name), conditionally hides the `↓ downloads` icon when the field is absent (spaces). Renders the gated lock icon when applicable, plus the trending-score flame icon when present.
  - `lib/columns/plugins/manifest.ts`, `lib/columns/registry.ts`, `lib/columns/server-registry.ts`: three single-line registry edits, parity check covered by the existing test that asserts every plugin in `manifest.ts` has matching client + server registrations.
  - `README.md`: column count 36 → 37; new "AI / ML (1)" cluster row added between News & web and Long-form & video; hero paragraph and keyless-columns line both pick up Hugging Face. Tagline "Build a deck, pack it with columns…" gets Hugging Face inline alongside the other surface mentions.

**Impact:** Pairs with the same-day aeon PR #162 to give both running surfaces (live dashboard column / agent-curated daily digest) coverage of the HF Hub's daily movement. Activates a category that had been dormant since the plugin system shipped, opening the door for arxiv / DEV.to / future AI-ecosystem columns (both already in the May 8 repo-actions ideas pipeline) without further category plumbing.

---

## aaronjmars/aeon-agent

No substantive PRs merged in the 24h window. 32 routine cron auto-commits from the scheduler and per-skill auto-commits across token-report, fetch-tweets, tweet-allocator, repo-pulse, feature, self-improve, repo-actions, heartbeat, push-recap, repo-article, project-lens — plus their corresponding `chore(cron): <skill> success` markers. PR #33 (`improve/xai-prefetch-truncation-warning`, opened by self-improve at 13:30 UTC May 8) is **still open**, not merged — last log entry that implied it was merged was wrong.

---

## Developer Notes

- **New dependencies:** None. Both Hugging Face shipments use keyless public REST endpoints (`huggingface.co/api/...`) — no key, no SDK, no env var.
- **Breaking changes:** None. Both new surfaces ship disabled-by-default (aeon `enabled: false`; minitor columns are user-instantiated, never auto-created).
- **Architecture shifts:** The minitor `ai` `ColumnCategory` flips from declared-but-unused to live. The aeon AI-ecosystem coverage triple (paper-pick / github-trending / huggingface-trending) is now structurally complete at three resource layers; future research-cluster skills can cite it as the canonical pattern.
- **Tech debt:** None added. PR #156 fully resolves a documented sandbox-curl gap rather than papering over it.
- **Stalled PRs cleared:** PR #156 (open ~102h, May 3 → May 8) — the only stalled fork-author PR heartbeat had been flagging.
- **Open PRs as of recap:** aeon-agent PR #33 (xai-prefetch truncation warning) still open — bot self-improve PR, not yet reviewed.

## What's Next

- aeon `huggingface-trending` ships disabled. First natural enable date is whenever the operator flips it; the 09:30 UTC slot is already reserved in `aeon.yml`. First run will compete for attention with github-releases (same slot) and github-trending (09:00) — three AI/dev surfaces back-to-back-to-back.
- Today's repo-actions output (May 8 article) named **arxiv column** and **DEV.to column** as the next two minitor integrations — both keyless, both fit the AI / ML cluster row created today, both follow the same plugin-shape (lib/integrations/* → lib/columns/plugins/{name}/{plugin,server,client} → 3 registry edits + README).
- aeon-agent PR #33 still open. Next iteration of self-improve or a manual review will need to merge it, otherwise May-6's max-output-token raise lands without its companion observability fix.
- The pattern of two repos shipping the same content domain on the same day (aeon skill + minitor column) is now the third occurrence (Stack Overflow May 7, Hugging Face May 8, with at least one prior). The repo-article angle for May 8 has natural material here: agent identifies an AI-stack gap, ships both the curation skill and the live-dashboard surface in the same morning.
