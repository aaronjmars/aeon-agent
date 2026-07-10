---
type: Article
---

# Push Recap — 2026-06-23

## Verdict
> SHIPPING — dashboard UX hardened, phylax-audit ships, minitor searches validated

**Shape:** 4 user-visible commits · 4 internal · 2 infra · 55 bot-filtered  
**Volume:** 42 files changed, +523/-96 lines across 10 human commits by 2 authors  
**Merged PRs:** 15 total (#537 #539 #540 #541 #542 aeon; #111 #112 #113 #114 aeon-agent; #78 minitor; #532–#536 dependabot)

---

## Top impact today
1. `c024edb` — code-quality pass + load-error UX fix. Dashboard's lazy-loaded panels (Strategy, MCP, Soul, Packs) and feed/analytics fetches now surface failures with a `PanelError` component and a Retry button — previously a non-ok response left `*Loaded` unset and spun the "Loading…" indicator forever. (16 files, +126/−48)
2. `764cd11` — feat(skill): add phylax-audit. External contributor usephylax ships a pre-install ALLOW/WARN/DENY security gate for external skills: deterministic score (100 minus severity weights), three scans (static prompt-injection/secret-exfil, Base contract bytecode, x402 endpoint probe). Complements the maintainer's in-repo `skill-scan`. (4 files, +124/−2)
3. `133ffc9` — feat: validate non-empty search query in Grok-backed columns. Five minitor columns (x-search, news-search, facebook, instagram, google-news) now trim the query and throw "Search query is required." on blank input instead of firing a wasted Grok API call that returned an opaque error. (5 files, +20/−14)

---

## aaronjmars/aeon

### Dashboard Hardening — runs feed + panel error UX

**What this is:** Two separate fixes close the two most visible UX gaps in the dashboard: an infinite spinner on load failures, and Dependabot noise flooding the FEED/RUNS tabs.

**Shipped to users**
- `c024edb` — code-quality pass + load-error UX fix (#540)
  - `apps/dashboard/components/PanelError.tsx`: new shared error component — renders the panel failure with a Retry button that re-runs the fetch. Previously missing entirely; load failures were silent spinners. (+16/−0)
  - `apps/dashboard/app/page.tsx`: wires error states for all lazy-loaded views (strategy, MCP, soul, packs) and feed/analytics fetches; each now rejects on non-ok response and sets an explicit error state. (+30/−15)
  - `apps/dashboard/lib/http.ts`: extracts `syncFields()` to a shared helper, used at 3 call sites that were bypassing the existing helper. (+14/−4)
  - `apps/dashboard/lib/utils.ts`: extracts `slugify()` into shared util; used at 5 call sites. (+6/−0)
- `cdeeb56` — fix(dashboard): show only Aeon-launched runs in feed/runs (#542)
  - `apps/dashboard/app/api/runs/route.ts`: replaces blocklist filter (`!push && !pull_request`) with an allowlist of events Aeon's own workflows actually emit (`workflow_dispatch`, `workflow_call`, `schedule`, `repository_dispatch`, `issues`). Structurally excludes Dependabot's `dynamic` event and any future GitHub-managed run type without enumerating them. (+11/−4)

**Under the hood**
- `c024edb` (code-quality portion): drops never-read `CATALOG_PROMPT` export from `lib/catalog.ts`; removes redundant `as Task` casts in `apps/a2a-server`; names `CommitResult` type (5 sites); reuses `McpServers` alias instead of inline `Record<string,Record<string,unknown>>` (3 sites); drops dev-history comments from `llm-gateway.sh` case labels.

### Ecosystem Security — phylax-audit (external contributor)

**What this is:** usephylax (Phylax) contributes the first external security skill targeting Aeon's install pipeline — a pre-install gate for skills fetched from outside the repo.

**Shipped to users**
- `764cd11` — feat(skill): add phylax-audit — pre-install ALLOW/WARN/DENY verdict (#537)
  - `skills/phylax-audit/SKILL.md`: 121-line new skill. Produces a deterministic ALLOW/WARN/DENY score for an external skill URL before `./add-skill`. Score = 100 − severity weights (crit 40 / high 20 / med 10 / low 3); DENY triggers at critical finding or score < 50. Three scan stages: static prompt-injection/secret-exfil, Base contract bytecode/privileged-surface/honeypot check, x402 endpoint HTTPS/402-schema/price probe. Registered disabled (workflow_dispatch) — opt-in manual gate, not yet wired into `./add-skill`. (+121/−0)
  - `aeon.yml`, `skills.json`, `packs.json`: manifest regenerated from full clone to fix shallow-checkout sha/updated fields. (+4/−2)
- `bbc35ba` — docs: add Phylax to ECOSYSTEM.md (#539): one-line acknowledgement of the external contributor. (+1/−0)

### Internal: Dependabot Configuration

**What this is:** Reduces Dependabot's GitHub Actions noise — from ~7–13 runs/day to a monthly batched cadence — without removing security coverage.

**Infra**
- `ea1123f` — chore(deps): group Dependabot updates per ecosystem, switch to monthly (#541): `.github/dependabot.yml` now opens one combined PR per ecosystem per cycle (not one-per-dep weekly); security updates (real CVEs) remain ungrouped and fire on advisory. (+34/−12)

---

## aaronjmars/minitor

### Search Input Validation

**What this is:** Five Grok-backed search columns now fail early with a clear error on empty queries rather than propagating blank input to the API.

**Shipped to users**
- `133ffc9` — feat: validate non-empty search query in Grok-backed columns (#78)
  - `lib/columns/plugins/x-search/server.ts`, `news-search/server.ts`, `facebook/server.ts`, `instagram/server.ts`, `google-news/server.ts`: each trims `config.query` and throws `"Search query is required."` on blank/whitespace. Matches the guard already in place for the `farcaster` and `bing` columns. Also strips leading/trailing whitespace from the query sent upstream. (+20/−14)

---

## aaronjmars/aeon-agent

### Internal: Operational Polish

**What this is:** Three fixes to the agent's own tooling — correct git attribution on cross-repo commits, cleaner notification output, and input validation on the `skill-runs` audit script.

**Under the hood**
- `c1a7930` — fix(attribution): always commit cross-repo work as aeonframework (#114): `.github/workflows/aeon.yml` and `chain-runner.yml` now set `git config --global user.name/email` before any step, so clones spawned mid-run (e.g. docs-sync's website clone) inherit the aeonframework identity instead of falling back to ad-hoc emails. (+8/−4)
- `c6e470e` — feat: validate --hours is a positive integer in skill-runs (#112): `scripts/skill-runs` guards the `--hours` arg with a positive-integer regex immediately after arg parsing; bad values now fail fast with a clear message instead of crashing inside date arithmetic. (+7/−0)
- `379a4f2` — docs-sync: hide PR link from notification output (#113): drops the `PR: <url>` line from the docs-sync notify template; memory/logs still record it for traceability. (+0/−3)

---

## Developer notes
- **New dependencies:** none (5 dependabot bumps: @tailwindcss/postcss 4.2.2→4.3.1, react/react-dom 19.2.4→19.2.7, @types/react 19.2.14→19.2.17, @types/node 22→26, typescript 5.9.3→6.0.3 — all apps/dashboard only)
- **Breaking changes:** none
- **New public surface:** `phylax-audit` skill (workflow_dispatch, disabled by default); `PanelError` component in dashboard; `slugify()` and `syncFields()` exported from dashboard lib utils/http
- **Tech debt added:** none visible in diffs

## Open threads
- `aaronjmars/aeon` #543 — docs: add apps/dashboard/README.md (open since 2026-06-23, today)
- `aaronjmars/aeon` #510 — Add LENS skill pack (ThoLynceus, stalled since 2026-06-19, ~4 days)
- `aaronjmars/aeon` #418 — feat(gateway): add BEAMR as LLM gateway (SahilParikh03, stalled since 2026-06-10, ~13 days)
- `aaronjmars/aeon-agent` #115 — fix: warn feature skill against compound-bash in temp dirs (open since 2026-06-22)
- `skills/phylax-audit`: registered but disabled (workflow_dispatch only) — not yet wired into `./add-skill`; wiring it as a required gate remains the top `repo-actions` pick

## Sources
- aaronjmars/aeon: ok
- aaronjmars/aeon-agent: ok
- aaronjmars/minitor: ok
- gh api events: fail (null — events paginate window likely empty; fell back to commits)
- gh api commits: ok
- gh pr list: ok
- bot-filtered: 55 (5 dependabot PRs + ~50 aeon-agent automation chore/scheduler commits)
- diff-truncated: 1 (c024edb — 33.6KB patch, read by file stats + PR description)
