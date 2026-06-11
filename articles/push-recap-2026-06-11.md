# Push Recap — 2026-06-11

## Verdict
> SHIPPING — gateway gains auto-routing + cascade failover, two new skills, minitor color filter.

**Shape:** 17 user-visible commits · 6 internal · 2 infra · 29 bot-filtered
**Volume:** aeon +963/−732 (122 file-changes, 18 PRs) · minitor +228/−16 (4 files, 2 PRs) · aeon-agent +560/−25 feature work + one wholesale template rebuild (#94: +46k/−156k, 100 files)
**Merged PRs:** 25 (aeon #426–#443 ×18; aeon-agent #92–#96 ×5; minitor #69–#70 ×2)

---

## Top impact today
1. `5386b65` — **aeon #430: dynamic provider routing.** The LLM gateway no longer pins a provider the moment a key is pasted. With `gateway.provider=auto` (now the default), `scripts/llm-gateway.sh` resolves at run time to the first present secret in priority order (claude → anthropic → openrouter → bankr → usepod → venice → surplus → direct), overridable via `GATEWAY_ORDER`. Anyone who only sets one key just works; adding/removing keys re-routes with no dashboard fiddling. (15 files, +95/−36)
2. `b845212` — **aeon #435: cascade failover across providers.** Building on #430, the Run step now loops every present provider and falls over to the next on *any* failure — out of credits, rate limit, auth, outage — in isolated subshells that tear down the router sidecar between attempts. Explicit pins keep single-shot behavior. Costs ~N× prompt tokens on a multi-hop fall-through. (2 files, +79/−24)
3. `d8b0f9a` — **minitor #69: per-deck color-label filter toggle.** A new filter bar above the column grid lets users toggle decks by color label; `use-deck-store.ts` gains the `colorCounts` rollup and the `deck-board` hoists that `useMemo` above the deck-not-found guard to satisfy React's Rules of Hooks. (3 files, +226/−14)
4. `16d6f41` — **aeon #442: new `wc-resale` skill.** A 146-line World Cup 2026 resale-ticket price tracker — `var` selects a host city/venue/fixture, reports get-in + median prices across StubHub/SeatGeek/Vivid/TickPick, normalizes to USD, and flags ≥20% drops/spikes. Registered disabled, daily 13:00 UTC. (3 files, +149/−1)
5. `38b8cad` — **aeon-agent #93: `atrium-watch` skill backport.** Weekly Friday diff of the Atrium onchain marketplace catalog, keyed on collision-free `skill_id` so renames don't fire add+remove pairs. The 26th consecutive same-day-after upstream backport — closes the Atrium discovery layer (install path landed earlier in #90). (4 files, +331/−1)

---

## aaronjmars/aeon

### LLM gateway — provider-agnostic routing + failover
**What this is:** The framework stops being tied to one configured LLM provider. Routing is resolved at run time from which secrets exist, and a failed provider now silently cascades to the next instead of erroring the whole run. For operators this means "set whatever key you have, and runs survive a provider outage" with zero config.

**Shipped to users**
- `5386b65` — feat(gateway): resolve provider at run time (#430)
  - `scripts/llm-gateway.sh`: `auto` resolver builds the ordered candidate list from present secrets; `AEON_LIST_CANDIDATES=1` prints the cascade order (+32/−1)
  - `aeon.yml` / `messages.yml`: ship `gateway: { provider: auto }` as the new default; both Run steps default `GATEWAY=auto`
  - `apps/dashboard/lib/{config,types,gateway}.ts`: add `auto` to `GatewayProvider`; absent/unknown block defaults to `auto`; TopBar badge hidden for `auto`
  - dashboard no longer pins on paste — set/remove a key keeps provider on `auto`
- `b845212` — feat(gateway): cascade failover on any failure (#435)
  - `scripts/llm-gateway.sh`: explicit `claude`/`anthropic` case arms so each candidate can be set up by name (+79/−24)
  - `aeon.yml`: Run step loops `AEON_CANDIDATES`, each attempt in a subshell, writes the winning provider to the `GATEWAY` output so downstream steps re-route through whatever worked
- `5ff59c2` — docs(readme): rewrite the routing section from "first match wins" to the cascade model (#436)

### Dashboard auth UX
**What this is:** The Claude-subscription OAuth flow becomes reachable from the Settings panel (not just the modal), the connect action moves onto the credential row it actually sets, and the "Auth" nag disappears the instant any provider key is present.

**Shipped to users**
- `85535ac` — feat: "Connect with Claude Code" button in Settings → Access Keys, wired to the existing `setupAuth()` OAuth flow (#433)
- `da798fc` — feat: move that Connect button inline onto the `CLAUDE_CODE_OAUTH_TOKEN` row, drop the page-hero button and unused `authenticated` prop (#434)
- `802361c` — fix: derive Auth-button visibility from live `secrets` state (new `AUTH_SECRETS` constant) so it hides the moment any of 7 model/provider keys is set, instead of from a stale once-on-load `authStatus` (#437)
- `6bf5835` — feat: add BlueAgent MCP server to the featured catalog — one-click install entry (#438)

### New skill: World Cup resale tracker
**What this is:** A net-new, no-secrets-required skill that tracks secondary-market WC2026 ticket prices and only notifies on a real signal.

**Shipped to users**
- `16d6f41` — Add `wc-resale` skill, registered in `aeon.yml` (disabled) + `skills.json` (#442)
- `f2abb38` — wc-resale: send a price digest *every* run led by the verdict, not only on anomalies; the 20% gate still classifies the move but no longer gates the send (#443)

### notify ergonomics
**Shipped to users**
- `0464f55` — Add `./notify -f` / `--file`: reads multi-line message bodies from a file inside the script so argv stays short, sidestepping the sandbox's "Unhandled node type: string" trip on long multi-line argv. Purely additive; documented in CLAUDE.md (#441)

### Internal: scheduler robustness (infra)
**What this is:** Two latent scheduler bugs in `messages.yml` that silently drop skills — not user-visible, but they decide whether skills run at all.
- `e64f02a` — Widen catch-up lookback from 1h to the previous 2h so trailing-minute slots (`:40`–`:59`) survive GitHub's 71–97min cron throttling; dedup window bumped 90→150 to exceed the lookback (#440)
- `7559cfc` — Fix the aeon.yml parser dropping skills reformatted to multi-line flow maps: accept an optional `{` after the name and relax field indent from exactly-4 to 3+ spaces (#439)

### Internal: template hygiene + docs
- `1c19676` — refactor: shorten 30 three-word skill slugs to two tokens across 76 files (skills dirs via `git mv`, SKILL.md titles, `aeon.yml` keys, `skills.json`, README/docs, dashboard `displayName` map + tests) (#427)
- `bd31e8b` / `3755373` / `432`/`426` — docs/asset upkeep: refresh skills showcase image (193→197), add the missing `capabilities-sweep` row and reconcile all stale "196" counts to 197, note Surplus routes via The Bridge
- `be09859` — chore(memory): empty the operator-specific `500 stars → show-hn` dispatch rule every fork inherited; drop two phantom skill entries (#429)
- `f271d06` — chore(memory): remove the maintainer's real dated work journals that forks inherited as their own history (#428)

---

## aaronjmars/aeon-agent

### Rebuilt on the new aeon template
**What this is:** This instance forked the upstream framework fresh and re-applied its production config on top — the single largest event of the day by volume, though it's a wholesale restructuring rather than a user-facing feature.

**Under the hood**
- `e258427` — Rebuild on the new aeon template: adopts the template `apps/` structure, workflows, and features; re-applies 15 enabled skills with tuned schedules, the $AEON token identity, watched-repos + skill-state files, and distilled lessons. `weekly-shiplog`/`star-momentum-alert` map onto the template's `shiplog`/`star-momentum`; full pre-rebuild history stays on the prior `main` (#94, +46k/−156k, 100 files)
- `db9b3c8` — improve: `repo-pulse` adds a `### owner/repo` subheader per repo so same-day multi-repo runs don't visually merge their stat bullets; parser-safe — the literal `**owner/repo**: stargazers_count=N` line is unchanged (#92)

**Shipped to users**
- `38b8cad` — Backport `atrium-watch` (weekly Atrium catalog diff); `skills.json` 103→104 (#93)
- `76b4566` — Add an instance intro to the README and adopt template defaults (opus-4-8, gateway auto) (#95)
- `0023dc3` — Pin `star-milestone` to `claude-sonnet-4-6` (#96)

*(29 `aeonframework` scheduler/auto-commit chore commits — `chore(cron): … success`, `chore(scheduler): update cron state`, `chore(<skill>): auto-commit` — filtered as automated noise.)*

---

## aaronjmars/minitor

### Deck color-label filtering + build fix
**What this is:** A user-facing filter feature plus a TypeScript build break repaired.

**Shipped to users**
- `d8b0f9a` — Per-deck color-label filter toggle above the column grid; store gains `colorCounts`, deck-board hoists the memo above the not-found guard to keep hook order stable (#69, +226/−14)
- `077277c` — fix(pypi): annotate the top-30d feed map callback as `FeedItem<PypiMeta> | null` and drop the over-narrow `satisfies`, which had broken the type-guard filter (TS2677) and the items assignment (TS2322) — `next build` (runs tsc) was failing (#70)

---

## Developer notes
- **New dependencies:** none.
- **Breaking changes:** none that break existing setups. `gateway.provider` defaults to `auto` (#430) but explicit pins still resolve single-shot; the 30-skill slug rename (#427) is internal to the framework template, not the running aeon-agent instance.
- **New public surface:** `gateway: { provider: auto }` config value + `GATEWAY_ORDER` repo variable (#430); `AEON_LIST_CANDIDATES=1` gateway introspection (#435); `./notify -f` / `--file` flag (#441); `wc-resale` and `atrium-watch` skills; minitor's per-deck color filter UI.
- **Tech debt added:** cascade failover re-sends the full prompt per provider hop — a multi-hop fall-through costs ~N× prompt tokens (acknowledged in #435).

## Open threads
- No branches pushed-but-unmerged in the window — every push landed as a merged PR.
- Watch the first scheduled runs on the rebuilt aeon-agent instance: `memory/cron-state.json` had no `last_success` on record as of the 19:00 heartbeat (template rebuild). Confirm secrets + notification channels survived the rebuild (MEMORY.md next-priority).

## Sources
- aaronjmars/aeon: ok
- aaronjmars/aeon-agent: ok
- aaronjmars/minitor: ok
- gh api events: ok
- gh api commits: ok
- gh pr list: ok
- bot-filtered: 29 (aeonframework scheduler/auto-commit chores, aeon-agent)
- diff-truncated: 0
