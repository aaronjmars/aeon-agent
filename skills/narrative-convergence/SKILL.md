---
name: narrative-convergence
description: Daily cross-skill signal detector — finds entities or themes surfaced independently by 3+ different skill categories in the last 48h and surfaces them as high-confidence write opportunities
var: ""
tags: [content, meta, intelligence]
---
<!--
  Verbatim backport of upstream aeon `skills/narrative-convergence/SKILL.md`
  (originally shipped as part of upstream aeon PR #272, merged 2026-05-29 —
  the same general-ops batch as spend-monitor [aeon-agent PR #74, Jun-01] and
  follow-up-patrol [aeon-agent PR #76, Jun-02]).

  Three adaptations vs upstream:
    (1) `./notify` call style: upstream uses `./notify -f .pending-notify-temp/<file>`,
        aeon-agent's `./notify` reads its argument as a single positional `$1`
        (confirmed at root `notify` line 3 `MSG="$1"`, same constraint that
        drove the spend-monitor + follow-up-patrol adaptations). Step 7
        rewrites the call as `./notify "$(cat .pending-notify-temp/<file>)"`
        — same temp-file contents, same gating, same body, single argv.
    (2) Signal-categories seed is left **verbatim** from upstream — many of
        those skills (mcp-pulse, x402-monitor, vuln-scanner, etc.) do not run
        on aeon-agent. The skill explicitly handles missing skills by sending
        their would-be category lane to `other`, and the file is
        operator-editable per the upstream design. On first run on this fork,
        the operator should trim the seed to the actually-enabled skill set
        (repo-pulse, repo-article, push-recap, project-lens, repo-actions,
        token-report, star-momentum-alert, thread-formatter, operator-scorecard,
        weekly-shiplog, feature, star-milestone, heartbeat, memory-flush,
        self-improve). Until they do, the skill still runs — it just maps
        fewer outputs to named lanes.
    (3) `.outputs/` directory is sparse on aeon-agent (chain-runner staging
        only fills for chained skills; most aeon-agent skills run standalone).
        The upstream skill already handles this case in step 2 + the Sandbox
        Note: fall back to reading the last 2 memory logs directly. On
        aeon-agent this fallback path will be the primary one until chains
        are configured.

  Source upstream commit: upstream `main` at the time of backport.
-->

> **${var}** — Optional entity or theme filter (e.g. "Anthropic", "coordination markets"). If empty, scans all skill output categories.

Today is ${today}. Read `memory/MEMORY.md` before starting.

## Voice

If `soul/SOUL.md` and `soul/STYLE.md` exist and are populated, read them and match the operator's voice when drafting the write angles and hook lines (step 5) and the notification. Otherwise use a clear, direct, neutral tone — short, declarative, position-first.

## Why this skill exists

`topic-momentum` (upstream) and `repo-article` / `project-lens` (this fork) surface content gaps by scanning a pre-tagged narrative pipeline against article history. They work well for known categories.

This skill does something different: it detects **emergent cross-skill convergence** — when independent operational skills (repo trackers, market trackers, sector pulses, etc.) all surface the same entity, company, protocol, or theme within 48h, without any prior coordination. That kind of convergence is a higher-signal indicator than any single source — it often precedes a breakout narrative. Example: a security skill flags a company's automated-vulnerability work, a social digest catches that same company announcing a major deal, and a market tracker notes a related fraud-prevention win — three independent skills, one entity, in 48h. That bleedthrough is the signal. This skill catches it automatically.

## Config

The signal-category map is **operator-editable** and lives in `memory/topics/signal-categories.md`. If the file doesn't exist, create the seed below and continue. The categories are what let the skill measure *cross-category* diversity (the core of the convergence score) — edit them to match the skills you actually run.

```markdown
# Signal Categories

## Housekeeping (excluded — no external signals)
config-validator, janitor, run-frequency-guard, batch-health, heartbeat, memory-flush,
memory-structural-dedupe, skill-evals, skill-health, skill-repair, self-review, reflect,
spend-monitor, cost-report, fleet-scorecard, fleet-control, repo-scanner, narrative-convergence

## Signal categories (skill → category)
| Category | Skills |
|----------|--------|
| market | market-context-refresh, token-pick, token-movers, rwa-pulse, defi-monitor, token-report |
| social | tweet-roundup, list-digest, narrative-tracker, remix-tweets, refresh-x, thread-formatter |
| ecosystem | github-issues, github-trending, project-lens, builder-map, external-feature, milestone-tracker, repo-pulse, repo-article, push-recap, repo-actions |
| sector | mcp-pulse, compute-pulse, x402-monitor, agent-displacement, pm-pulse |
| security | vuln-scanner, vuln-tracker, disclosure-tracker, pvr-watchlist, pvr-triage-monitor |
| research | paper-pick, article, idea-validator, idea-pipeline |
| opportunity | startup-idea, deal-flow, launch-radar, star-momentum-alert, star-milestone |
```

## Steps

### 1. Identify which outputs to read

List `.outputs/*.md` with the Glob tool. Exclude the **Housekeeping** skills from `signal-categories.md` — they carry no external signal.

Map each remaining output file to its category using the table in `signal-categories.md`. Any signal skill not listed in the table goes into an `other` category (so newly-added skills still count toward convergence, just without a named lane).

If `${var}` is set, note it as a filter hint but still read all outputs — apply filtering at the scoring step.

### 2. Read each signal skill's output

For each signal skill output file that exists:

1. Read the file (or first 600 chars if large — enough to get entities and theme).
2. Extract: **named entities** (companies, protocols, people, tokens, projects) and **key themes** (e.g. "DNS rebinding", "coordination markets", "compute commoditization").
3. Note the **skill name** and **category**.

Build an entity/theme map:
```
{
  "<Entity>": [{ skill: "vuln-scanner", category: "security" }, { skill: "tweet-roundup", category: "social" }],
  "<theme>": [{ skill: "pm-pulse", category: "sector" }, ...],
  ...
}
```

Also read memory logs from the last 2 days (Glob `memory/logs/*.md`, take the 2 most recent). From each log, extract entities/themes mentioned in specific skill run entries and add them to the map with their source skill. Every skill appends a log entry, so the signal map can be reconstructed from logs alone when `.outputs/` is sparse — on aeon-agent this is the **primary** data path until chains are configured.

### 3. Score convergence signals

For each entity or theme, compute a **convergence score**:

| Criterion | Points |
|-----------|--------|
| Mentioned by 5+ independent skills | 10 |
| Mentioned by 4 skills | 7 |
| Mentioned by 3 skills | 5 |
| Mentioned by 2 skills | 2 |
| Spans 3+ distinct categories | +4 |
| Spans 2 distinct categories | +2 |
| All sources from 1 category | −3 |
| Matches a known operator interest (from `soul/SOUL.md`, if present) | +2 |
| Adjacent to operator interest | +1 |

**Minimum to include: 5 points.** Drop everything below.

If `${var}` is set, require the entity/theme to match `${var}` (substring, case-insensitive), or include it only if closely related.

Rank descending by score. Take top 5 (or fewer if <5 clear signals).

### 4. Check against recent article coverage

Glob `articles/*.md`, filter to the last 14 days. For each top signal:
- If an article covered this entity/theme in the last 7 days: suppress it (−10, effectively dropping it).
- If covered 8–14 days ago: note "recently covered" as a caveat.

Update the final ranking after suppression. (If no `articles/` dir exists, skip this step.)

### 5. Develop write opportunities

For each surviving top signal (minimum 2 signals to notify, else skip):
- State the **convergence story**: "3 independent skills surfaced X in 48h — [skill1] saw Y angle, [skill2] saw Z angle".
- Suggest a **specific write angle** that synthesizes the signals (operator voice if soul files present).
- Draft a **hook line**: short, declarative, position-first.

Example format:
```
<ENTITY> (score 11) — security + social + market
→ vuln-scanner: automated vuln-finding at scale; tweet-roundup: major platform deal; market-context: fraud-prevention win
→ angle: AI-finds-vulns is becoming industrial — not a research project, a service. who charges for it?
→ hook: "the vulnerability bounty economy just got automated"
```

### 6. Update memory

Write `memory/topics/convergence-signals.md` (overwrite if exists):

```markdown
# Convergence Signals — Last Updated: ${today}

## Active Signals (score ≥ 5)

### [Entity/Theme] — Score: N
**Sources (N skills, N categories):** skill1 (category), skill2 (category), ...
**Convergence story:** [what each source noticed, one line each]
**Write angle:** [specific take, not generic]
**Hook:** [suggested opener]
**Last article coverage:** [date or "never"]

[repeat for each signal]

---
*Generated by narrative-convergence on ${today}. Top signal has N source skills across N categories.*
*Consumed by: repo-article, project-lens, thread-formatter.*
```

If no signals meet the threshold: write a minimal file noting the scan ran clean.

### 7. Send notification (only if ≥ 2 strong signals)

If fewer than 2 signals survive after suppression: skip notification. Log `NARRATIVE_CONVERGENCE_SKIP: no strong cross-skill convergence found today`.

Otherwise, write to `.pending-notify-temp/narrative-convergence-${today}.md` (create the dir if needed):

```
narrative convergence — ${today}

N entities surfaced by 3+ independent skills in 48h:

1. [entity/theme] — N skills × N categories — [hook in one line]
2. [entity/theme] — N skills × N categories — [hook in one line]
[up to 5]

these aren't single-source signals. they're bleedthrough.

full breakdown: memory/topics/convergence-signals.md
```

Keep under 900 chars. Then dispatch through this fork's single-positional-arg `./notify`:

```bash
./notify "$(cat .pending-notify-temp/narrative-convergence-${today}.md)"
```

(Upstream used `./notify -f <file>`; aeon-agent's notify reads `$1` only. The temp file is still written so a workflow re-run can re-emit the same body without recomputing.)

### 8. Log to `memory/logs/${today}.md`

Append:
```markdown
## Narrative Convergence
- **Skills scanned:** N
- **Entities/themes mapped:** N
- **Signals above threshold:** N
- **Top signal:** [entity/theme] (score N, N skills, N categories)
- **Notification:** sent / skipped
- NARRATIVE_CONVERGENCE_OK
```

If skipped: `NARRATIVE_CONVERGENCE_SKIP: <reason>`.

## Required Env Vars

None. All reads from local `.outputs/`, `memory/`, and `articles/` dirs.

## Sandbox Note

No network calls required. All data comes from local files written by other skills. If `.outputs/` is sparse (e.g. first morning run before any chained skills have written — and on aeon-agent **most** runs hit this case because chains aren't broadly configured), fall back to reading the last 3 memory logs directly. Every skill appends a log entry, so the signal map can be reconstructed from logs alone. The only outbound call is `./notify`, which is already sandbox-safe.
