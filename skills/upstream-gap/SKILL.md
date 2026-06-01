---
name: upstream-gap
description: Weekly diff of local skills/ against upstream aaronjmars/aeon — sorted queue of pending backports by upstream merge date, alerts when any skill has been pending >48h
var: ""
tags: [meta, community]
---
> **${var}** — Optional. Pass `dry-run` to skip notify (state and article still write). Pass `owner/repo` to override the upstream parent. Combine with a space (`dry-run owner/repo`) for both.

Today is ${today}. This repo is a fork of aaronjmars/aeon and has run a 17-consecutive-day same-day-after backport streak that depends entirely on the operator (or the `feature` skill) noticing what landed upstream. Every other gap-detection surface in this fleet measures someone *else's* drift — `fork-skill-gap` looks at OTHER forks, `fleet-skill-adoption` looks at the fleet's enabled count, `skill-update-check` compares already-imported skills against their lock. None of them answer the question that drives the backport chain: **"what shipped upstream that this fork hasn't picked up yet?"**

## Why this exists

If a skill merges into upstream on a day when the operator's attention is elsewhere, it can sit unbackported for days with no signal — the backport chain is observable only after the fact, and the silence between rounds reads identical to a clean state. As external contributors accelerate the upstream merge cadence (10+ open PRs from HoundFlow / MandateSeal / antfleet-ops / rsavitt at the time of writing), one missed day compounds: the longer the gap, the harder it is to backport cleanly without resolving cross-skill conflicts.

This skill turns "did anything land upstream that I'm missing?" from an operator memory check into an explicit weekly artifact with a sortable queue. Notification fires only when there's something actionable — silent on clean weeks.

## Scope and inputs

Two read-only sources, neither requires a secret:

1. **Local `skills/` directory** — every directory under `skills/` that contains a `SKILL.md`. Slug = directory name.
2. **`gh api repos/{parent}/contents/skills`** — upstream's skill list. Slug = directory entry name.

The first time a slug is observed as a gap, this skill fetches its first-merge commit date via `gh api repos/{parent}/commits?path=skills/{slug}/SKILL.md`. That date is the upstream merge timestamp the table sorts on.

## Steps

### 0. Bootstrap

```bash
mkdir -p memory/topics articles
[ -f memory/topics/upstream-gap-state.json ] || cat > memory/topics/upstream-gap-state.json <<'EOF'
{"parent":null,"last_run":null,"last_status":null,"upstream_skill_count":null,"local_skill_count":null,"gaps":{}}
EOF
```

`gaps` is a map keyed by slug. Each entry holds `{first_seen_local, upstream_merged_at, days_pending, last_seen}`. `first_seen_local` is the date THIS skill first observed the slug as a gap — it powers the "Days pending" column without relying on git history of this repo. `upstream_merged_at` is the upstream merge date for the slug's SKILL.md. Entries are evicted on the run where the slug becomes locally present (i.e. backport landed).

### 1. Parse var

- Split `${var}` on whitespace. Tokens: `dry-run`, anything matching `^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$` (treated as `PARENT_OVERRIDE`), anything else.
- If any unknown token is present → log `UPSTREAM_GAP_BAD_VAR: ${var}` and exit (no notify).
- `MODE=dry-run` if `dry-run` token present, else `execute`.

### 2. Resolve parent repo

```bash
if [ -n "$PARENT_OVERRIDE" ]; then
  PARENT_REPO="$PARENT_OVERRIDE"
else
  PARENT_REPO=$(gh api "repos/$(gh repo view --json nameWithOwner -q .nameWithOwner)" --jq '.parent.full_name // empty')
  [ -z "$PARENT_REPO" ] && PARENT_REPO="aaronjmars/aeon"
fi
```

If `state.parent` is set and differs from the resolved `PARENT_REPO` → log `UPSTREAM_GAP_PARENT_CHANGED`, reset `gaps` to `{}`, update `state.parent`. (Changing upstream is a clean slate — pending counters from a prior parent are meaningless.)

### 3. Enumerate upstream skill slugs

```bash
gh api "repos/${PARENT_REPO}/contents/skills" \
  --jq '[.[] | select(.type=="dir") | .name]' > /tmp/up-slugs.json
UPSTREAM_COUNT=$(jq 'length' /tmp/up-slugs.json)
```

If the call returns 404 or empty array → log `UPSTREAM_GAP_NO_UPSTREAM_DIR`, exit (no notify). A parent with no `skills/` directory is either misconfigured or not Aeon-shaped.

A skill is a `skills/{slug}/` directory; we treat the SKILL.md inside as the unit. The contents endpoint does NOT verify SKILL.md exists in each subdir — that's checked in step 5 when the merge date is fetched.

### 4. Enumerate local skill slugs

```bash
ls -1 skills/ 2>/dev/null | while read -r SLUG; do
  [ -f "skills/${SLUG}/SKILL.md" ] && echo "$SLUG"
done | sort -u > /tmp/local-slugs.txt
LOCAL_COUNT=$(wc -l < /tmp/local-slugs.txt | tr -d ' ')
```

A directory under `skills/` without a `SKILL.md` is treated as absent — empty / WIP directories don't count as adopted.

### 5. Compute the gap set

```bash
jq -r '.[]' /tmp/up-slugs.json | sort -u > /tmp/up-slugs.txt
comm -23 /tmp/up-slugs.txt /tmp/local-slugs.txt > /tmp/gap-slugs.txt
GAP_COUNT=$(wc -l < /tmp/gap-slugs.txt | tr -d ' ')
```

For each slug in `/tmp/gap-slugs.txt`:

- If the slug is already in `state.gaps` → reuse stored `first_seen_local` and `upstream_merged_at`. (We don't refetch the merge date every week — once fixed, it's fixed.)
- Otherwise → fetch the upstream merge date:

  ```bash
  gh api "repos/${PARENT_REPO}/commits?path=skills/${SLUG}/SKILL.md&per_page=1" \
    --jq '.[-1].commit.committer.date // empty'
  ```

  This API returns commits newest first. `.[-1]` selects the *oldest* in the page — for `per_page=1` that's the most recent commit; for the **first-merge date** we instead want the last page:

  ```bash
  # Get the total count via the Link header trick or just paginate:
  gh api --paginate "repos/${PARENT_REPO}/commits?path=skills/${SLUG}/SKILL.md&per_page=100" \
    --jq '.[].commit.committer.date' | tail -1
  ```

  The `tail -1` picks the oldest commit touching that path — the first time the SKILL.md was added. Set `first_seen_local=${today}`. If the API errors after one retry → mark `upstream_merged_at=unknown`, do not add to the article (we don't sort on missing dates).

### 6. Detect resolved gaps (closed-the-loop bookkeeping)

For each slug in `state.gaps` that is NOT in today's `/tmp/gap-slugs.txt`:

- This slug has been backported since the last run. Record it in a separate `resolved_today` list for the notification.
- Evict the slug from `state.gaps`.

If `resolved_today` is non-empty, the notification (when sent) opens with a one-line "Closed since last run:" preamble before the pending list. This makes the chain visible — operator sees credit for completed backports as well as outstanding work.

### 7. Compute days_pending and classify

For each gap slug with a known `upstream_merged_at`:

```
days_pending = floor((now - upstream_merged_at) / 86400)
```

Bucket each gap:

| Tier | Trigger |
|------|---------|
| `URGENT` | `days_pending >= 7` |
| `STALE`  | `days_pending >= 2` AND `days_pending < 7` |
| `FRESH`  | `days_pending < 2` |
| `UNKNOWN` | `upstream_merged_at == unknown` (API failure) |

The 2-day floor on `STALE` mirrors the same-day-after backport cadence in MEMORY.md — anything 0-1 day old is in-flight, not lagging.

### 8. Pick the verdict

Priority order:
1. `URGENT_BACKLOG: {N} skills pending ≥7 days` — when `URGENT >= 1`.
2. `STALE_QUEUE: {N} skills pending 2–6 days` — when `STALE >= 1` and `URGENT == 0`.
3. `FRESH_ONLY: {N} new upstream skills` — when only `FRESH` entries exist.
4. `CLEAR: fork in sync with upstream` — when `GAP_COUNT == 0`.

### 9. Quiet-week gate

**Skip notify entirely** when ANY of:
- `MODE=dry-run`.
- Verdict is `CLEAR` AND `resolved_today` is empty (genuinely nothing to say).
- Verdict is `FRESH_ONLY` AND no slug has crossed from `FRESH` to `STALE` since the last run (i.e. operator already saw these slugs at FRESH, no new information).

Otherwise, gate is open and the notification fires.

### 10. Write the article

Path: `articles/upstream-gap-${today}.md`

```markdown
# Upstream Gap — ${today}

**Verdict:** {one-line verdict from step 8}

**Parent:** {PARENT_REPO} · **Upstream skills:** {UPSTREAM_COUNT} · **Local skills:** {LOCAL_COUNT}
**Gap:** {GAP_COUNT} · **Urgent (≥7d):** {N_URGENT} · **Stale (2–6d):** {N_STALE} · **Fresh (<2d):** {N_FRESH}

---

## Pending backports

(Sort by days_pending desc; ties broken by slug alphabetical. Cap at 30 rows; footer "... and N more" if truncated.)

| Slug | Tier | Upstream merged | Days pending |
|------|------|-----------------|--------------|
| {slug} | URGENT\|STALE\|FRESH | {YYYY-MM-DD} | {N} |

---

## Closed since last run

(Only render if resolved_today is non-empty.)

| Slug | First seen as gap | Days to backport |
|------|-------------------|------------------|

---

## Source status

`upstream_dir_count={UPSTREAM_COUNT} · local_dir_count={LOCAL_COUNT} · gap_count={GAP_COUNT} · merge_date_lookups=N/M · state_age_days=N`
```

Cap article at ~300 lines (deferred from 400 in `fork-skill-gap` — this skill produces a shorter, narrower view).

### 11. Update state

Write `memory/topics/upstream-gap-state.json`:

```json
{
  "parent": "{PARENT_REPO}",
  "last_run": "${today}",
  "last_status": "UPSTREAM_GAP_OK|UPSTREAM_GAP_QUIET|...",
  "upstream_skill_count": N,
  "local_skill_count": N,
  "gaps": {
    "slug-name": {
      "first_seen_local": "YYYY-MM-DD",
      "upstream_merged_at": "YYYY-MM-DD",
      "days_pending": N,
      "last_seen": "${today}"
    }
  }
}
```

Evict entries whose `last_seen` is more than 90 days old AND that are not in the current gap set (covers an upstream skill being removed from `skills/`, e.g. consolidation or deprecation — we shouldn't carry stale memory of a slug nobody ships anymore).

### 12. Append to memory log

```
## upstream-gap
- Status: UPSTREAM_GAP_OK | UPSTREAM_GAP_QUIET | UPSTREAM_GAP_CLEAR | UPSTREAM_GAP_DRY_RUN | UPSTREAM_GAP_NO_UPSTREAM_DIR | UPSTREAM_GAP_PARENT_CHANGED | UPSTREAM_GAP_API_FAIL | UPSTREAM_GAP_BAD_VAR
- Verdict: {one-line verdict}
- Upstream / Local / Gap: {UPSTREAM_COUNT} / {LOCAL_COUNT} / {GAP_COUNT}
- Urgent / Stale / Fresh: {N_URGENT} / {N_STALE} / {N_FRESH}
- Resolved today: {N_RESOLVED}
- Article: articles/upstream-gap-${today}.md
```

### 13. Notify — gated

Skip per step 9.

Otherwise send via `./notify` (keep ≤900 chars total):

```
*Upstream Gap — ${today} — {PARENT_REPO} → {THIS_REPO}*
{verdict line}

Local has {LOCAL_COUNT} of {UPSTREAM_COUNT} upstream skills. {N_URGENT} urgent / {N_STALE} stale / {N_FRESH} fresh.

{If resolved_today non-empty:}
Closed since last run: {slug1}, {slug2}, {slug3}{... and N more if >3}.

Top 3 pending (oldest first):
- {slug1} — merged {YYYY-MM-DD}, {N1}d pending ({TIER1})
- {slug2} — merged {YYYY-MM-DD}, {N2}d pending ({TIER2})
- {slug3} — merged {YYYY-MM-DD}, {N3}d pending ({TIER3})

Full queue: articles/upstream-gap-${today}.md
```

## Exit taxonomy

| Status | Meaning | Notify? |
|--------|---------|---------|
| `UPSTREAM_GAP_OK` | Run succeeded; verdict triggered notify gate | Yes |
| `UPSTREAM_GAP_QUIET` | Notify gate closed (FRESH_ONLY with no new STALE, etc.) | No (log only) |
| `UPSTREAM_GAP_CLEAR` | Zero gap, zero resolved — no signal to send | No (log only) |
| `UPSTREAM_GAP_DRY_RUN` | `MODE=dry-run`; state + article wrote, notify skipped | No |
| `UPSTREAM_GAP_NO_UPSTREAM_DIR` | Parent has no `skills/` directory | No (log only) |
| `UPSTREAM_GAP_PARENT_CHANGED` | Resolved parent differs from stored — state reset | No (log only) |
| `UPSTREAM_GAP_API_FAIL` | Upstream contents listing failed after one retry | Yes (single-line error notify) |
| `UPSTREAM_GAP_BAD_VAR` | `${var}` parse failed | No |

## Constraints

- **Read-only against upstream.** This skill never writes to the parent repo, never opens issues / PRs / discussions upstream. It only reads `contents/skills` and per-path `commits`.
- **The merge date is the upstream merge date, not when the skill was open as a PR upstream.** First commit touching `skills/{slug}/SKILL.md` on the parent's default branch is the authoritative timestamp. PRs that were never merged don't appear.
- **Never refetch known merge dates.** Once `upstream_merged_at` is in state, it stays. This caps the per-week API budget at roughly `(today's new gaps) * 1 paginated call` rather than `GAP_COUNT * N` every run.
- **A locally-absent skill is a gap even if the local fork has a renamed equivalent.** This skill compares slugs verbatim. If upstream renames `foo` to `foo-v2`, both appear as separate slugs and the rename has to be handled by the operator (or the backport that lands the rename). Rename detection is out of scope and would create false negatives in the much more common new-skill case.
- **First-day false `URGENT`.** On the very first run, `first_seen_local=${today}` for every gap slug — but `days_pending` is computed from `upstream_merged_at`, not from `first_seen_local`, so a skill that merged upstream 14 days ago and went unbackported still surfaces as URGENT on day 1. This is the desired behaviour: the cold-start signal is the entire point.
- **Bot allowlist not applicable.** We compare directory listings, not authors. A skill committed by `dependabot[bot]` upstream is still a skill the fork should consider backporting.
- **No cap on gap size.** Even if the fork is 60 skills behind, the article enumerates the full queue (capped at 30 rendered rows + footer count). The notification still leads with the top 3 — operators eyeball the article for the full list.

## Sandbox note

Uses `gh api` for everything — no `curl`, no env-var-in-headers. Authenticates via `GITHUB_TOKEN` automatically per CLAUDE.md sandbox guidance. The `--paginate` flag handles >100-commit paths transparently.

If the upstream `commits?path=...` lookup persistently 403s or 5xxs for a slug after one retry → mark that slug's `upstream_merged_at=unknown` and continue. The slug surfaces in the article without a merge date (sorted last under UNKNOWN tier); the run does NOT exit with `UPSTREAM_GAP_API_FAIL` — partial failures on individual slugs do not corrupt the queue's value for the slugs we DID resolve.

`UPSTREAM_GAP_API_FAIL` is reserved for the upstream `contents/skills` listing itself failing — when we can't even enumerate the parent's skills, there is no queue to write.

## Security

- Upstream slugs are read as strings from `gh api` JSON responses. They flow through `comm` and `jq` only — never interpolated into shell beyond the controlled `skills/${SLUG}/SKILL.md` path inside the gh api call. Slug character set is constrained by GitHub's directory-name rules (no shell metacharacters land in the upstream `skills/` tree in practice; if they ever did, `gh api` would escape them in the URL).
- This skill never reads SKILL.md *contents* from upstream — only the slug list and the path's commit history. It is structurally impossible for a malicious upstream SKILL.md body to influence the article or the notification.
- The article surfaces upstream slugs and merge dates only. No descriptions, no tags, no commit messages — nothing operator-actionable can be smuggled via attacker-controlled upstream prose.
