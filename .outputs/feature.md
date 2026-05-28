*Feature Built — 2026-05-28 — aaronjmars/aeon-agent*

sparkleware-catalog backport (15th same-day-after)

Aeon-agent now has the same sparkleware-catalog skill that landed upstream in aeon yesterday — a weekly enriched export of the curated skill-packs.json registry. The skill reads the local skill-packs.json, calls GitHub for each pack's live stars / last-pushed / archived flag and its current skills-pack.json manifest, then writes a machine-readable skill-packs-catalog.json at the repo root that external community tools like Sparkleware can fetch without screen-scraping anyone's README. Default schedule is Tuesday 09:00 UTC, registered disabled — operators flip it on when they want the weekly enriched feed published.

Why this matters:
Sparkleware (sparkleware.vercel.app, aeon Issue #244) is the external community discovery catalog that crawls GitHub for topic:aeon-skill-pack repos and lists each pack with install commands. It complements skill-packs.json rather than replacing it — but it had no view into the curated registry's human-edited descriptions, trust_level signals, or declared skills arrays. This skill is the bridge: a stable raw URL that exposes the curated registry joined to live truth (current stars, last-push recency, live manifest skill count). Without it, aeon-agent's fork-local registry stays a static file with no freshness layer; with it, the registry has the same weekly health view the upstream now has. This is also the 15th consecutive same-day-after backport in the established cadence, which is now the longest unbroken chain in the project's history — every meaningful upstream skill ships into aeon-agent the following day.

What was built:
- skills/sparkleware-catalog/SKILL.md: New skill (verbatim backport, +289 lines). Reads skill-packs.json; for each pack, gh api repos/{owner}/{repo} for stars + pushed_at + archived + default_branch, then gh api contents/skills-pack.json?ref={default_branch} (base64 decode) for live skill count + slug array. Handles 404/403 as unreachable (carries registry fields forward, never drops the pack). Handles missing manifest as no_manifest (falls back to registry slug list — many packs ship without a root manifest). Detects registry/manifest drift (live ≠ registry slug set). Backport note at the top explicitly lists the three adaptation points that ran clean: notify arg style, output paths, gh-api pattern.
- aeon.yml: Registered enabled:false, schedule "0 9 * * 2", model claude-sonnet-4-6 — Tuesday 09:00 UTC slot matches upstream.
- skills.json: New entry, category dev, total 93 → 94.

How it works:
Step 0 bootstraps memory/topics/sparkleware-catalog-state.json (recovers from corruption silently). Steps 2-3 parse the registry and enrich each pack with live GitHub signals using gh api (no curl, no env-var-in-headers — matches CLAUDE.md sandbox guidance). Step 4 assembles per-pack objects (curated description WINS over live GitHub "About" field — registry editorial copy is authoritative). Step 5 writes the catalog at the repo root and a human-readable article at articles/sparkleware-catalog-{today}.md. Step 6 computes deltas vs prior state (new packs / removed packs / newly unreachable / recovered) — star and skill-count drift alone DO NOT notify (they change every week, would make this noisy). Step 7 picks one of seven exit states (OK/QUIET/DRY_RUN/PARTIAL/NO_REGISTRY/STATE_CORRUPT/BAD_VAR). Step 8 advances state and gates the notification on registry composition + reachability changes only.

What's next:
Operator can dispatch this skill manually for a baseline run before flipping the cron on, then turn the cron on so the enriched feed refreshes weekly. The next same-day-after backport target is whatever lands in upstream aeon today (May-28) — the chain extends.

PR: https://github.com/aaronjmars/aeon-agent/pull/66
