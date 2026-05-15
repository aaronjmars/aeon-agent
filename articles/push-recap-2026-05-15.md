# Push Recap — 2026-05-15

## Overview
Five substantive commits across three repos in the last 24h — two evening hygiene PRs on aeon that finally aligned skills/, skills.json, aeon.yml, and README around the same 117-skill catalog, then a midday burst Thursday that shipped three new features within seven minutes of each other: product-hunt-launch (aeon PR #175), skill-enabler (aeon-agent PR #47), and deck export/import (minitor PR #40). The thrust was launch-prep — the three features together let an operator draft Product Hunt copy, flip the enable switches the copy will reference, and ship a one-click deck-sharing primitive in Minitor that turns its sidebar into a community surface.

**Stats:** ~14 files changed, +822/-12 lines across 5 substantive commits (plus 31 cron auto-commits in aeon-agent that aren't recapped — those are scheduler work, not author work).

---

## aaronjmars/aeon

### Theme 1: Catalog hygiene — the registry, the README, the YAML, and the hero image all said different numbers
**Summary:** Two paired PRs (#173, #174) merged Wednesday evening closed the inventory drift between every place the project counts itself. `skills/` had 117 skill directories; `skills.json` listed 117; `aeon.yml` was scheduling only 114 of them (three skills had directory entries and JSON entries but no schedule line, so they could never fire on cron); the README hero said "+90 skills" and the project-structure tree said "92 skills"; the README category table enumerated only 96 of the 117 by name; the skill.jpg hero image listed an outdated subset. After both PRs, all five surfaces reference the same 117.

**Commits:**
- `c3a732e` — docs: sync skill catalog across registries (117 skills) (#173)
  - Changed `aeon.yml` (+5): added schedule entries for `aixbt-pulse` (0 9,21 * * *, sonnet-4-6 — twice-daily cross-domain market pulse via AIXBT grounding endpoint), `schedule-ads` (0 8 * * * — daily paid-ads scheduler across Meta/TikTok/Snapchat/Pinterest/LinkedIn, PAUSED by default), and `create-campaign` (workflow_dispatch — on-demand Meta campaign provisioner). All three were already implemented and registered but had no cron line, so they would never have run even with `enabled: true`.
  - Changed `README.md` (+11, -9): hero paragraph "+90 skills" → "117 skills"; project-structure tree "92 skills total" → "117 skills total" (two stale references); rewrote the full category table to enumerate every one of the 117 skills, with corrected counts per category (Research 18 → 19, Dev 29 → 32, Crypto 16 → 19, Social 7 → 12, Productivity 12 → 14, Meta 14 → 21).
  - Added a one-line note above the category table: "Every skill is independently installable, schedulable, and chainable." — closes the implicit ambiguity new operators kept asking about.

- `d311dd6` — chore(assets): refresh skill.jpg to the 117-skills catalog graphic (#174)
  - Replaced `assets/skill.jpg` to match the new category-table breakdown (Research 19 / Dev 32 / Crypto 19 / Social 12 / Productivity 14 / Meta 21). Binary swap — appears as 0/0 in the diff stats but is the visual half of #173. The README links to it inline, so they had to ship together or one would lie about the other.

**Impact:** Three previously-unreachable skills (aixbt-pulse, schedule-ads, create-campaign) are now activatable by flipping a single `enabled:` flag — they had a config gap, not a code gap. The README/hero now matches what a fork actually inherits, which closes a recurring "is this really 117 skills?" question that shows up in fork issues. This was hygiene, not feature work; the value is that the next operator who reads the repo doesn't have to triangulate three different counts.

### Theme 2: Product Hunt launch asset drafter — the second launch surface, complemented to show-hn-draft
**Summary:** New `product-hunt-launch` skill that drafts the full five-section PH launch asset pack (tagline ≤60 chars, description ≤260 chars, first comment ≤500 chars, maker comment ≤500 chars, six 80-char feature bullets) from live repo state — README, SHOWCASE, skills.json, aeon.yml, last 7 days of repo-articles and project-lens, last 7 days of logs, and the MEMORY.md Skills Built table. workflow_dispatch only, enabled:false — this is a one-shot launch-day skill, not a recurring run. The complement to show-hn-draft (PR #151, May 1): that one targets HN's technical-skim audience, this one targets PH's "is this useful to me right now" decision-makers.

**Commits:**
- `f60b307` — feat: add product-hunt-launch skill (#175)
  - New `skills/product-hunt-launch/SKILL.md` (+232): 9-step skill with five-status exit taxonomy (OK / PARTIAL / BAD_VAR / MISSING_INPUT / over-limit-PARTIAL). Single-section regeneration mode — `var=tagline` regenerates only the tagline block in place, overwriting that section of the existing article file without touching the others. Banned-marketing-words list ("AI-powered", "revolutionary", "leverages", "powerful", "framework" — all saturated on PH and score zero with that audience). Lead-capability scoring table (concreteness/recency/surprise, three signals) sets the spine of tagline + first comment; explicitly forbids leading with stars, token price, or "AI-powered."
  - Changed `skills.json` (+13, -1): registered the new skill under category `dev`, total count bumped 117 → 118.
  - Changed `aeon.yml` (+1): added schedule entry `product-hunt-launch: { enabled: false, schedule: "workflow_dispatch", var: "" }` under the launch-asset cluster next to show-hn-draft.

**Impact:** Both launch surfaces (HN and Product Hunt) now have pre-drafted asset packs ready on demand, generated under no time pressure from full repo context. The 5-minute-after-launch first-comment window on PH is the kind of thing that becomes worst when written live at 12:01 AM PT; this skill writes it ahead of time. The operator checklist appended to the article file documents the launch-day operational details (Tue/Wed/Thu 12:01 AM PT slot, logo/gallery specs, hunter outreach, cross-post sequencing) but explicitly is not posted — the skill drafts the assets, the human ships them.

---

## aaronjmars/aeon-agent

### Theme 3: skill-enabler — collapsing the typing that blocked 4 skills for 12 days
**Summary:** New `skill-enabler` skill that flips `enabled: false → true` for a comma-separated list of slug names in aeon.yml, then commits and opens a PR with a per-skill rationale table. The pain pattern it closes is documented in MEMORY.md: four announcement skills (star-milestone, star-momentum-alert, thread-formatter, show-hn-draft, ai-framework-watch) had their activation conditions met starting May 12 — 300⭐ crossed, ATH day scored 16+ on thread-formatter's signal table — and remained disabled for three consecutive days while the operator was elsewhere. The same finding appeared in three repo-articles and two heartbeat escalations before PR #45 (May 14) finally flipped them by hand. The lesson the operator's two-minute open-then-close of aeon PR #172 surfaced was that the bottleneck wasn't review — it was typing.

**Commits:**
- `e6b212f` — feat: add skill-enabler skill (#47)
  - New `skills/skill-enabler/SKILL.md` (+205): 7-step skill with explicit opt-in safety bar — empty var is a no-op (logs `SKILL_ENABLER_NO_INPUT` and exits silently, no notification). `dry-run:slug1,slug2` prefix validates without committing or pushing. Five validation gates walked in order, first failing gate is the slug's verdict: format (`^[a-z0-9][a-z0-9-]{0,63}$`) → directory exists (`skills/${slug}/SKILL.md`) → present as top-level entry in aeon.yml → not also under `chains:` (chains run skills as steps, so flipping a top-level entry that also appears in a chain produces double-runs) → currently `enabled: false`. Slug-scoped substitution — never a global `enabled: false → true` replace, which would also enable everything else that happens to be disabled. Single `aeon.yml` write at end of loop to avoid partial-state on mid-loop failure. Branch name `feat/enable-skills-${today}` with a `-${run_count}` collision suffix for same-day re-runs.
  - Changed `skills.json` (+11, -1): registered under category `dev`/`meta`, total count bumped 85 → 86.
  - Changed `aeon.yml` (+1): added the schedule entry as workflow_dispatch, enabled:false — this skill is invoked by an operator on demand, never on cron.

**Impact:** The "switch is still off in aeon.yml" pattern that consumed 12 consecutive repo-articles before May 14's reframe — and triggered a 3-day heartbeat ESCALATION before PR #45 closed it manually — now resolves to one `gh workflow run skill-enabler.yml -f var=slug1,slug2`. PR #45 (the manual fix) needed `workflows` PAT scope to push aeon.yml changes; this skill inherits that same requirement, and exits cleanly with `PUSH_FAILED` if the token doesn't have it. The reactive `repository_dispatch` bridge from PR #42 (May 14) can call this skill from outside the repo, which means a fork operator can trigger their own enable-skills run from Telegram or a Zapier webhook without ever touching the GitHub UI.

### Theme 4: Background — autonomous daily ops
**Summary:** 31 cron-driven auto-commits across 13 skill runs (token-report, fetch-tweets, tweet-allocator, repo-pulse, star-momentum-alert, feature, self-improve, repo-actions, push-recap, star-milestone, project-lens, repo-article, thread-formatter, heartbeat). Not recapped individually — these are the scheduler doing its job. Worth noting only because the activation pattern that began May 14 with PR #45 is now visibly active: star-momentum-alert ran at 10:29 UTC May 15 (the May 14 first-activation miss documented in yesterday's heartbeat self-resolved on first scheduled run, exactly as predicted). The pattern shift remains the one from yesterday's recap — every PR opened today merged today, no overnight backlog.

---

## aaronjmars/minitor

### Theme 5: Deck export / import — the first user-to-user sharing primitive
**Summary:** Two new ⌘K commands ("Export current deck (copy JSON)" + "Import deck from JSON") plus the server actions and dialog they need. Export serializes the active deck's name and ordered columns (typeId, title, config) to a pretty-printed JSON blob and copies via `navigator.clipboard` with a textarea+execCommand fallback for permission-blocked browsers. Import takes pasted JSON, validates it server-side with Zod, and always creates a new deck with " (imported)" appended to the name so the source deck stays untouched. This is the first user-facing share surface in Minitor — until now every install started blank, every config lived in one operator's browser, and nothing in the product encouraged saying "here's what I'm watching."

**Commits:**
- `015f002` — feat: deck export / import (#40)
  - Changed `app/actions.ts` (+121): added `exportDeck(deckId)` server action that selects the deck + columns ordered by position, and `importDeck(json)` that JSON.parses, Zod-validates against `importedDeckSchema` (version literal 1, name 1–128 chars, ≤64 columns, config record shape with typeId 1–128 chars and title 1–256 chars), then inserts the new deck. A follow-up commit in the same PR wrapped the deck-row insert and the N column-row inserts in `db.transaction(...)` so a mid-loop failure can't leave a half-imported deck. Defined the canonical `DeckExport` JSON v1 shape (`{ version: 1, deckName, exportedAt?, columns: [{ typeId, title, config }] }`) and exported it as a type for consumers.
  - Added `components/dialogs/import-deck-dialog.tsx` (+100): new textarea-based modal with sonner-toast error surfacing. The Zod parse error's path is surfaced verbatim ("Invalid deck JSON at columns.3.typeId: String must contain at least 1 character(s)") so a malformed paste tells the user which column broke.
  - Changed `components/sidebar-01/nav-header.tsx` (+76, -2): two ⌘K command entries + a `copyToClipboard` helper that tries `navigator.clipboard.writeText` first, then falls back to a hidden textarea + `document.execCommand('copy')` for browsers that block clipboard permission.
  - Changed `lib/store/use-deck-store.ts` (+38): added `exportActiveDeck` and `importDeckFromJson` store methods. The import method takes the server-returned column rows and updates the local store optimistically — no need to re-fetch the deck list snapshot to see the imported deck appear.
  - Changed `components/sidebar-01/app-sidebar.tsx` (+4): wires the dialog and the `onImportDeck` prop on the sidebar component.

**Impact:** Closes the "every Minitor install starts blank" gap that was the single biggest friction point for first-time users. With this PR a community member can post a deck JSON in Discord or a gist, anyone pastes it into Minitor, and they're watching the same 12-column AI-monitoring config in 10 seconds with zero infrastructure change. Feed items are intentionally not exported — they're fetched from upstream, not user state — so the imported deck triggers a fresh fetch on first view through the existing autoFetchColumn path. Forward-compatibility decision worth noting: unknown `typeId` imports cleanly and renders as an unknown column until the plugin is installed; strict rejection would have blocked one-bad-column imports from going through.

---

## Developer Notes

- **New dependencies:** `nanoid` and `zod` added to minitor's `app/actions.ts` imports (both were already in `dependencies` — no `package.json` change needed).
- **Breaking changes:** None. All three feature PRs add new skills or new actions; no existing API or config shape was modified.
- **Architecture shifts:**
  - aeon's `skills.json` is now 118 (was 117 24h ago, was 92 in stale README references the day before).
  - aeon-agent's `skills.json` is now 86 (was 85).
  - Minitor gained its first user-facing sharing primitive — historically a "what's in my deck" was unspeakable; now it has a JSON v1 schema, which means future export formats will need a version bump and a forward-compat policy.
- **Tech debt:**
  - Pre-existing pypi.ts typecheck errors in minitor's `main` branch are unrelated to this PR — touched files all clean per the PR body. Worth a follow-up but didn't block.
  - The `product-hunt-launch` and `show-hn-draft` skills share the exact same source-of-truth input list (README, SHOWCASE, skills.json, aeon.yml, recent articles, MEMORY.md). Two skills reading the same eight inputs is fine for now; the moment a third launch-surface skill lands (LinkedIn? Devpost?) it becomes a shared-context helper.

## What's Next
- aeon-agent's `skill-enabler` is the natural way to activate the next batch of pre-built skills that have shipped and remained `enabled: false`. The dispatch shape is documented; the first non-trivial call would be to enable announcement skills in the operator's own fork beyond what PR #45 already did (show-hn-draft is still disabled in aeon-agent per yesterday's recap).
- `product-hunt-launch` is workflow_dispatch only — the operator would invoke it ahead of the actual launch day. The MEMORY.md Recent Articles list shows 25 days of repo-articles and project-lens generated since May 1, which is more than enough source material for the lead-capability scoring step.
- Minitor's deck export/import lands the primitive, not the discovery surface. The natural follow-up is a "gallery" of public decks (someone curates a list of links to deck JSON gists) — the JSON v1 schema makes that a future-PR-friendly path.
- The May-14 repo-actions pipeline still has two open ideas: Fork Skill Gap (aeon, medium effort) and Column Keyword Alerts (minitor, medium effort) — both viable for the next `feature` run.
