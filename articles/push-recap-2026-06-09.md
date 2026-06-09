# Push Recap — 2026-06-09

## Overview

Today was the largest push day this fork has audited: ~33 substantive commits across the three watched repos, dominated by aeon, where Aaron and the framework merged a roughly 20-PR dashboard rebuild on top of yesterday's ecosystem-links/vigil-revoke/star-milestone-dispatch landings. The headline: **skills can now consume MCP servers during runs** (opt-in via `.mcp.json`), and the dashboard learned to provision MCP servers + secrets without touching any workflow YAML. Alongside it, **STRATEGY.md** shipped as a north-star artifact imported into every skill's base context, the four sub-apps (`dashboard/`, `mcp-server/`, `a2a-server/`, `webhook/`) moved into `apps/`, the Telegram poller stopped processing messages twice, the Telegram instant-mode worker became a one-click Cloudflare deploy, and the dashboard's skill catalog reconciled to 195 across the canonical 8 categories. aeon-agent shipped its 24th and 25th consecutive same-day backports and consolidated the runner-hook restriction into CLAUDE.md. Minitor added per-deck drag-to-reorder and a full j/k/`/`/c/Esc keyboard nav layer.

**Stats:** ~33 substantive commits, ~250+ files touched, ~3,200+ net lines added.

---

## aaronjmars/aeon

(~27 substantive commits since yesterday's recap. The bulk landed in two evening batches Jun-08 18:16–20:17 UTC and 21:16–21:22 UTC, then a Jun-09 morning–afternoon dashboard sweep 11:19–15:24 UTC.)

### Theme 1: MCP becomes a real surface — inbound runtime + dashboard provisioning

**Summary:** Aeon already exposed skills as MCP tools (outbound). Today it learned the inbound direction: skills running on GitHub Actions can call MCP servers (GitHub, databases, paid APIs). The dashboard learned to add servers and provision their secrets in one flow. Eight PRs add up to a complete provisioning surface.

**Commits:**

- `3ce86cc` — feat: let skills use MCP servers during runs (opt-in) (#372)
  - `.github/workflows/aeon.yml` (+23/-1) and `messages.yml` (+22/-1): when a repo-root `.mcp.json` exists, the runner invokes Claude with `--mcp-config .mcp.json --strict-mcp-config` and appends `mcp__<server>` to `--allowedTools` for each server. With no file, runs are byte-identical to before.
  - Safety valve: if the config references a `${VAR}` that is unset and has no `:-` default, the run **skips MCP with a warning** instead of letting Claude's parse-failure break the skill.
  - `.mcp.json.example` (new, +16): two working servers — `github` (uses the present `GITHUB_TOKEN`) and a no-auth stdio server.
  - `dashboard/components/McpPanel.tsx` (+200): list/add/remove servers, surfaces each server's `${VAR}` references and reminds the operator to set them.
  - `dashboard/app/api/mcp/route.ts` (+47): writes `.mcp.json` via the global gate that already proxies `/api/*`.

- `0c4aba5` — feat(mcp): auto-resolve any .mcp.json secret — no workflow editing (#378)
  - Preflight now resolves every `${VAR}` a project's `.mcp.json` references straight from the repo's secrets (`toJSON(secrets)`), exports it for the run, then **discards the blob before any skill code runs**. Set the secret in the dashboard and MCP just works — no per-name `env:` wiring in `aeon.yml/messages.yml`, and it works for any secret name no matter how the server was added.
  - Dashboard MCP tab gains an inline token-value field that stores the secret on add via `gh secret set`, so adding a server + its credential is a single step.

- `b5f33a6` — feat(dashboard): set an MCP server's secret inline on its row (#381)
  - Existing servers that reference an unset `${VAR}` were a dead end — the add-server form's value field only applied to brand-new servers. Each server row now renders its referenced secrets credential-style: password input + "Set" when unset (saves straight to GitHub via the same `gh secret set` path as Settings), green "✓ set" when present.

- `9f3f212` — fix(dashboard): the bearer token IS the secret — no secret-name field (#382)
  - Add-server form asked for a "bearer-token secret name" then a separate "value" — operators correctly pasted the token into the name field. Now HTTP servers have one optional "bearer token" field: the secret env-var is derived from the server name (`ctrl2` → `MCP_CTRL2_TOKEN`).

- `f662d6f` — fix(dashboard): MCP credential cleanup, enabled filter, 28 display (#384)
  - McpPanel: removing a server now deletes its panel-minted `MCP_<SLUG>_TOKEN` credential from GitHub (when no other server references it), with a confirm — previously the secret lingered.
  - LeftSidebar: new "Enabled" toggle that shows only on-duty skills.
  - HQOverview: `shrink-0/whitespace-nowrap` on two-digit category counts so labels like "Research & Content" no longer squeeze "28" onto two lines.

- `f20905f` — feat(dashboard): surface all skill API keys under 06 / Skill Keys (#385)
  - Global scan of `skills/` for external API keys. Added the 10 that were missing from the panel: `ETHERSCAN_API_KEY`, `BASESCAN_KEY`, `BANKR_API_KEY`, `VERCEL_TOKEN`, `REPLICATE_API_TOKEN`, `RESEND_API_KEY`, `LIQUIDPAD_API_KEY`, `ADMANAGE_API_KEY`, `SUPERNOTES_API_KEY`, `CONGRESS_GOV_API_KEY` — each with a signup/host hint verified from the skill's actual endpoints.
  - Moved `DEVTO_API_KEY` / `NEYNAR_API_KEY` / `NEYNAR_SIGNER_UUID` from the "Distribution" group (which `SecretsPanel` never renders) into "Skill Keys" so those three are settable from the UI at all.

- `5bba508` — fix(mcp): stop ${ALL_SECRETS:-{}} from corrupting the secrets JSON
  - bash closes `${...}` at the first `}`, so the intended `{}` default degraded to `{` and a stray `}` was appended to `ALL_SECRETS`. `jq` then failed with `Unmatched '}'` and the skill step died (exit 5) the **moment a `.mcp.json` existed** — exactly when MCP first got wired in. Guarded the empty case via a temp var.

- `2ac0fbd` — fix(dashboard): hide MCP row paste box while a token save is in flight
  - Per-row secret input only flipped to "✓ set" once the parent's `secrets` state updated after the `gh-secret-set` round-trip (~2s). In that window it cleared to its placeholder and looked broken. Threads the existing `busy[\`sec-<name>\`]` flag into `McpPanel` and renders "setting…" while pending.

- `0399e41` — feat(dashboard): Claude-subscription first, bigger Add Credential, Opus 4.7 (#379)
  - `AuthModal`: leads with "Use Claude Subscription" as the primary filled action; demotes the API-key form to secondary outlined below a divider. Adds Opus 4.7 to the model list.

**Impact:** Aeon went from "static set of self-contained skills" to "skills that can reach into a configurable MCP fabric the operator provisions from a UI." The provisioning round-trip is one screen — pick a server, paste a token, hit add. The runner picks it up next time the workflow fires, and unconfigured secrets degrade gracefully instead of crashing the step. The bash-substitution fix (`5bba508`) is critical — without it, `.mcp.json` would have killed `aeon.yml` on every run.

---

### Theme 2: STRATEGY.md — a north-star imported into every skill's base context

**Summary:** A two-PR pair adds a repo-root `STRATEGY.md` that every skill sees automatically via Claude Code's `@import`, plus a dashboard editor for it. Captures north-star metric, priorities, audience, hard constraints, optimize/avoid.

**Commits:**

- `feba6a7` — feat: STRATEGY.md — a north-star every skill follows (#370)
  - `STRATEGY.md` (new, +49): short, safe-when-unfilled template — neutral defaults plus an "unconfigured defaults" status line skills key off so they fall back to general judgment until the operator tailors it.
  - `CLAUDE.md` (+6): new `## Strategy` section with `@STRATEGY.md` import. Lands in every skill's base context with **no per-skill change**.
  - `onboard` (+14): validates `STRATEGY.md` — passes when customized, warns when missing or still on template defaults.
  - Caveat called out: `@`-import is Claude-Code-specific. A multi-harness runtime (roadmap #4) would need an equivalent injection or this silently no-ops there.

- `08defd4` — feat(dashboard): edit STRATEGY.md + Telegram instant-mode guide (#371)
  - New Strategy page (left-nav item): reads `STRATEGY.md` via `/api/strategy` (GET) into a textarea editor; Save writes it (PUT → `updateFile`/`createFile`) and flags `hasChanges` so the existing Push commits it. Shows customized-vs-template-defaults state and a soft length warning (it rides in context on every run).
  - Settings page gains an "Instant-mode guide" under Telegram: explains the Cloudflare Worker path to ~1s replies — deploy button prefilled with the fork's repo, Worker secrets listed, copy-able `setWebhook` command.

**Impact:** Skills no longer have to be told "your job is X" inside their SKILL.md prose — they read `STRATEGY.md` in their base context. The operator can rewrite their north-star from the dashboard without touching any skill or workflow.

---

### Theme 3: Repo restructure — sub-apps under `apps/`, templates dirs disambiguated

**Summary:** Largest blast-radius change of the day. The four sub-projects (`dashboard/`, `mcp-server/`, `a2a-server/`, `webhook/`) moved into `apps/`. Two confusable "templates" directories renamed.

**Commits:**

- `cd99804` — chore: group sub-apps under apps/, rename templates dirs (#376) — **129 files**, +113/-109
  - `dashboard/`, `mcp-server/`, `a2a-server/`, `webhook/` → `apps/`
  - `templates/` → `skill-templates/` (was confusable with `workflow-templates/`)
  - `workflows/` → `workflow-templates/` (collided with `.github/workflows/`)
  - `apps/mcp-server` & `apps/a2a-server` walk `__dirname/../../..` to repo root (was `../..`); both load all 195 skills at runtime.
  - `apps/dashboard` repo-root resolution bumped to `process.cwd()/../..` in `gh.ts` and the api/`{sync,outputs,skills,skills/[name]/run}` routes; `next build + 99 unit tests pass`.
  - `aeon`, `add-mcp`, `add-a2a`, `notify-jsonrender`, `new-from-template` path vars; `.github/workflows/aeon.yml` dashboard/outputs paths (incl. commit allowlist).
  - External URLs updated: Cloudflare deploy button → `tree/main/apps/webhook`; Smithery subfolder → `apps/mcp-server`.
  - Added `apps/mcp-server/.gitignore` (was missing; `dist/` was committable).

- `77333ad` — chore: declare MIT license in package manifests, update copyright name (#377)
  - `"license": "MIT"` added to all four `apps/*/package.json` files (was relying solely on root LICENSE).
  - `LICENSE` copyright holder: `Aaron Mars` → `Aaron Elijah Mars`.

**Impact:** Repo root now reads as `aeon/skills/ + aeon/apps/ + aeon.yml + CLAUDE.md + STRATEGY.md + MEMORY.md` — a much cleaner separation between the agent layer (skills) and the platform layer (apps). The cost was hand-bumping path resolution in three runtimes; the commit verified all three still resolve correctly.

---

### Theme 4: Telegram — instant-mode Worker, dedupe fix, no-op when webhook active

**Summary:** Telegram support went from "polling-only with a manually-deployable Worker docs snippet" to "one-click Cloudflare deploy + dedupe-safe poller."

**Commits:**

- `0a0bc5a` — feat(webhook): one-click Telegram instant-mode Worker (#368) — +221/-35 across 7 files
  - `webhook/src/worker.js` (new, +79): hardened relay — method + `secret_token` verification, JSON guard, chat-id allowlist, `update_id` in dispatch payload for webhook-mode dedupe, 200-on-ignore (so Telegram never redelivers), 502-on-failure (so it retries).
  - `webhook/wrangler.toml` + `package.json` (wrangler pinned to 4.98.0) + `.gitignore` + `README.md` (94 lines: Deploy-to-Cloudflare button, secret table, `setWebhook` instructions, polling coexistence).
  - Main README features the deploy button; `docs/telegram-instant.md` slimmed to a pointer so there's a single source of truth for the Worker code.

- `9b16b91` — fix(messages): stop Telegram messages being processed twice (#369)
  - The poller advanced the `getUpdates` offset with an unverified `curl … > /dev/null` after already collecting the messages, then dispatched them. If that ack silently failed (sandbox/transient), the next tick re-read the same updates and re-dispatched them — **duplicate processing**.
  - Fix: acknowledge BEFORE enqueuing. Collect Telegram messages into a temp array, advance the offset, and only merge them into the dispatch set once Telegram confirms `ok:true`. On ack failure the messages stay pending for the next tick (at-most-once).
  - Skip polling when a webhook is active: call `getWebhookInfo` first and skip the Telegram branch if a webhook URL is set — `getUpdates` 409s once instant mode is enabled, so the two no longer fight.
  - Security pass: confirmed all five workflows already carry least-privilege `permissions:` blocks and none use `set -x` or echo secrets.

- `7aff807` — ci: pin Claude Code CLI install to a known version (#367)
  - Both runner workflows ran `npm install -g @anthropic-ai/claude-code` unpinned. Pinned to `2.1.168` in `aeon.yml` and `messages.yml`. No behaviour change today; closes a supply-chain window where a freshly-published or compromised release would land with no review.

- `72469be` — fix(dashboard): migrate middleware→proxy, hide upstream-sync from feed (#373)
  - Next.js 16 deprecated the `middleware` file convention. Renamed `middleware.ts` → `proxy.ts` (config/matcher unchanged).
  - Filters "Sync from upstream" workflow runs out of `/api/runs` so they don't appear in Feed/Runs. Bumped run limit 20→30.

**Impact:** Telegram instant mode (sub-second replies via a Cloudflare Worker) is now a one-click deploy from the README. The poller stopped duplicating messages on ack-failure, and the polling branch noops itself when a webhook is configured. Pinning the Claude Code CLI closes a real supply-chain gap.

---

### Theme 5: Skill count + categories reconciled to 195 / 8

**Summary:** A single PR fixed an inventory discrepancy that had drifted across README (193), skills.json (194/195), filesystem (195 SKILL.md dirs), and dashboard (196). All sources now read 195.

**Commits:**

- `c78cab9` — feat(dashboard): reconcile skill count to 195 + 8-category UI + UX fixes (#383) — +160/-96 across 18 files
  - `aeon.yml`: added the two shipped-but-unlisted skills (`liquidpad-launch`, `vigil`).
  - `skills.json`: fixed stale total (194→195) and empty schedules.
  - `README`: 193→195 everywhere + table counts (Dev 36→37 +`ecosystem-links`, Onchain 14→15 +`vigil-revoke`).
  - `/api/skills`: ignores dirs without `SKILL.md` (drops the phantom `skills/security/data` dir that made the dashboard read 196).
  - `lib/constants.ts`: new `CATEGORIES` constant (Core, Research & Content, Dev & Code, Crypto & Markets, Onchain Security, Social & Writing, Productivity, Meta / Agent), replacing the ad-hoc `DEPARTMENTS` map. `LeftSidebar`/`HQOverview`/`SkillDetail`/`TopBar` group + label by category; HQ "Departments" → "Categories".
  - UI fixes: `SkillDetail` hero title scales font-size down by longest word so long names don't overflow; `TopBar` long titles truncate; analytics regex no longer false-matches `enabled:true` in comments; `/api/runs` filters CI runs (push/pull_request) out of feed + runs; category filter chips under Team (All + 8); + Hire moved into Team header; `Hire popup` closes on outside click.
  - `ECOSYSTEM.md`: added Azzle.
  - Follow-up flagged: `assets/skills-aeon-193.jpg` banner art still reads "193 SKILLS" — needs a design regen + filename rename (can't be edited in code).

**Impact:** Five sources of truth disagreed about how many skills exist. They now agree on 195. The dashboard's category grouping moved from "whatever was in `tags[0]`" to the canonical 8.

---

### Theme 6: Cleanup chain — types, dead imports, error masking, decorative comments

**Summary:** A seven-PR cleanup chain (numbered 1/7 through 7/7 in the original audit, of which 2/7 and #359–#365 landed today). The audit hit type weakness at JSON boundaries, error-masking that turned 500s into empty 200s, dead imports, decorative box-drawing comments, and a triplicated `REPO_ROOT` constant.

**Commits:**

- `a97f64d` — fix(dashboard): clear dead imports + latent tsc error, fix knip config (#359)
  - `utils.test.ts`: passes a valid `m`/`h` interval-unit to `buildCron` (was 0), clearing the only `tsc --noEmit` error.
  - `ImportModal.tsx`: drops unused `displayName` import. `config.ts`: drops unused `isSeq` + `type Document`. `knip.json`: marks `lib/catalog.ts` as an entry so knip stops false-flagging it.

- `ae626e8` — Cleanup 2/7: collapse dead watched-repos path, drop unused exports (#366)
  - `builder-map`, `feature`, `repo-revive` read `memory/topics/watched-repos.md` which **does not exist on disk**, while 25+ skills read `memory/watched-repos.md` which does. Converges the 3 outliers on the extant root file and removes the inverted "legacy" fallback.
  - De-exports 3 symbols with no external importers (knip-confirmed): `MEMORY_ROOT`, `GatewayConfig`, `TargetCursorProps`.

- `d77b8f4` — refactor(dashboard): consolidate triplicated REPO_ROOT into one export (#361)
  - `github.ts` and `memory.ts` each redefined `const REPO_ROOT = resolve(process.cwd(), '..')` byte-identical to the one `gh.ts` already exports. Imports it from `./gh` instead. `madge --circular` confirms clean.

- `409ef2b` — refactor(dashboard): bind API producers to central types, unify gh-run shapes (#362)
  - `/api/skills` GET annotated as `Skill[]`; `/api/secrets` typed `Omit<Secret,'isSet'>[]` → `Secret[]`. Three `gh-run` routes that each redefined an overlapping shape now share one `GhRunJson` source-of-truth in `lib/types.ts`, with each route `Pick<>`ing exactly the columns its `--json` flag requests.

- `035c92c` — refactor: strengthen weak types at JSON parse + JSON-RPC boundaries (#363) — +46/-23 across 8 files
  - The codebase has **zero** `any`/`as-any`/`@ts-ignore`. The real weakness was values TS types loosely at deserialization boundaries.
  - dashboard: types every untyped `await request.json()` (DOM types it `Promise<any>`) with a per-route body shape. `import/route.ts` surfaced that `repo`/`skills` were used unvalidated; added explicit 400 guards.
  - `github.ts`: replaces `process.env.X!` non-null assertions in `getConfig()` with an explicit throw; gives `updateFile`/`createFile` explicit `Promise<unknown>` returns.
  - `a2a-server` (input hardening): adds `asString`/`asNumber`/`isRecord`/`isA2AMessage` guards; replaces 8 unvalidated `as` casts on attacker-controllable JSON-RPC params. `params.message` was cast to `A2AMessage` then dereferenced as `.parts` with no check — malformed input now rejects cleanly instead of throwing.
  - `mcp-server`: narrows `request.params.arguments?.var` via `typeof` instead of `as string`.

- `abdc009` — fix(dashboard): surface gh failures instead of masking them as empty 200s (#364)
  - `GET /api/analytics` and `GET /api/runs` each wrapped their `gh-CLI` call + `JSON.parse` in a try whose catch returned HTTP 200 with zeroed/empty data — so a broken `gh` auth or schema change rendered as a **healthy-but-idle dashboard instead of an error**. Replaces both empty catches with `catch (error: unknown) { return { error: msg } at status 500 }`. Safe because both clients already branch on `r.ok`.

- `be7e38c` — style(dashboard): drop decorative box-drawing section banners (#365)
  - Removes 10 decorative `{/* ───── LABEL ───── */}` divider comments in `HQOverview`, `SkillDetail`, `SecretsPanel`. The numbered ones sat directly above `<Section index="01" label="Departments">` which already renders the index + label.

- `09abc2d` — fix(dashboard): make shift-schedule inputs readable
  - The interval/hour/minute inputs used `text-aeon-bg` (#0a0a0a) on a `bg-aeon-panel` (#111) surface — near-invisible dark-on-dark text. Switched to `text-aeon-fg`.

**Impact:** Type safety at the JSON deserialization boundary went from `Promise<any>` everywhere to per-route body shapes + guard functions. The a2a-server JSON-RPC parser will now reject malformed input cleanly instead of TypeError-ing. The dashboard's two "silent 200" paths now correctly surface 500s. One read of the same `REPO_ROOT` constant across the dashboard codebase.

---

### Theme 7: show-hn-draft prompt refresh for the imminent 500⭐ auto-fire

**Commits:**

- `f12b9fb` — feat: refresh show-hn-draft prompt context for 500⭐ auto-fire (#380)
  - Launch trigger reframed: 300-star horizon → 500-star auto-dispatch via `star-milestone` (PR #358 wired the rule map; aeon at 496⭐, ~3 days out at v7 ≈3.6/day).
  - Project-scale shorthand: "~250 stars, growing autonomous-agent narrative" → "~500 stars, ~165 forks, ~195 skills across 8 categories, external skill-packs ecosystem, onchain security layer".
  - Title example: "90+ skills" → "195 skills". Body §2 hint added: explicit pointer at the non-obvious capabilities the LLM should consider surfacing as the senior-engineer surprise — onchain security (vigil + wallet-risk-weekly + vigil-revoke), three install paths (clone + install-skill-pack + install-from-atrium), external skill-pack inflow (Nurstar / vigilcodes / HoundFlow / signa / Careful Finance / Mneme). Hard cap: pick ONE.
  - Launch checklist + edge case: 300-threshold language → next-round-number language (500, 750, 1000, …).
  - Mid-PR fix: aligned the prose "~195 skills" with the live README to avoid the discrepancy.

**Impact:** When `star-milestone` auto-dispatches `show-hn-draft` at 500⭐ (projected ~Jun 11), the draft will reflect the product as it actually exists today, not the early-May snapshot.

---

## aaronjmars/aeon-agent

### Theme 1: Three PR landings — ecosystem-links, runner-hook docs, install-from-atrium

**Summary:** The 24th and 25th consecutive same-day-after backports merged, plus the documentation consolidation flagged by yesterday's `self-improve` run.

**Commits:**

- `85f55a0` — feat: backport ecosystem-links — weekly Monday URL-health audit of ECOSYSTEM.md (#87) — +425/-1 across 4 files
  - Verbatim copy of upstream `skills/ecosystem-links/SKILL.md` (411 lines) from upstream PR #351, registered disabled at `55 11 * * 1` between `ecosystem-pulse` and `config-validator` (alpha order, Upstream sync section). `skills.json` total 101→102, category `research`.
  - **Mid-PR fix landed in the same PR**: the parser was a verbatim 3-column copy from upstream where `ECOSYSTEM.md` is `Logo | Project | Links`, but on aeon-agent the table is 2-column `Project | Links` (no logo column) — the parser extracted zero URLs and the audit was a silent no-op. Aligned the parser with the live `ecosystem-pulse` sibling on this fork (name = 1st cell, links = 2nd cell). Repointed the parser-shape parity note from the not-yet-backported `ecosystem-entrants` to `ecosystem-pulse`, and updated the image/logo design note to reflect the 2-column layout.

- `d1d26ae` — improve: document runner-hook restriction + phantom-template-var in CLAUDE.md (#89)
  - The runner-hook anti-pattern drove 6 consecutive `improve:` PRs (#63, #67, #71, #77, #81, #83) over 14 days, plus a 7th mid-PR fix on `mcp-pulse` PR #82 when the agent inherited a phantom `${today_minus_7}` template-variable reference from a `repo-actions` idea suggestion.
  - The class of bug is **"constraint isn't in CLAUDE.md"**, not "another skill needs the same patch". Adding the constraint to `CLAUDE.md` propagates it to all future skill runs system-wide.
  - Also fixes `aeon.yml` line 156 stale comment for `mcp-pulse` that STILL claimed it uses `${today_minus_7}` cutoff, even though the actual skill body explicitly debunks `${today_minus_7}` in 3 places.
  - Mid-PR fix landed: lead-in "Two patterns" → "Three patterns" after the third sandbox-limitation item was added.

- `b16ac25` — feat: backport install-from-atrium script (#90) — +94/-0
  - Verbatim copy of upstream aeon's `install-from-atrium` shell script (PR #335, merged 2026-06-03). Third skill install path alongside `./add-skill` (any GitHub repo) and `./install-skill-pack` (curated community packs). Fetches a skill from the Atrium onchain marketplace at `$ATRIUM_HOST/.well-known/skills`, runs the local `skill-security-scan` against it, records onchain provenance in `skills.lock` keyed by `atrium:0x<skill_id>`.
  - **First non-SKILL.md backport** in the 25-PR same-day-after chain. Repo-relative throughout; aeon-agent's directory layout matches upstream exactly on every path the script touches, so a byte-for-byte copy is the correct backport — no path rewrites, no notify-style translation, no `$(date ...)` substitution sites.
  - Mid-PR fix: in the `--list` branch, `curl | grep | sed` runs under `set -euo pipefail`. If grep matches nothing (empty marketplace or changed `index.json` shape) it exits 1 and pipefail aborts the script before the Install hint / exit 0. Wrapped only the grep in `{ ... || true; }` so an empty match is tolerated while a real curl network failure still propagates.
  - Unblocks `atrium-catalog-watcher` (upstream PR #342) as the natural 26th backport — yesterday's repo-actions article (#5) flagged this script as the explicit prerequisite.

**Impact:** The backport chain extends to 25 consecutive days. Atrium becomes a reachable install path. The runner-hook constraint is now in the system-wide preamble every skill run reads first, so the class of bug should stop recurring.

---

## aaronjmars/minitor

### Theme 1: Sidebar DnD + keyboard nav — three rungs in a single morning

**Summary:** Per-deck drag-to-reorder shipped first, then a full keyboard-nav layer landed and required an immediate follow-up to coexist with @dnd-kit's keyboard sensor.

**Commits:**

- `db8b883` — feat(sidebar): per-deck drag-to-reorder via @dnd-kit (#65) — +313/-170 in `components/sidebar-01/nav-decks.tsx`
  - `reorderDecks` has lived in the deck store + server action since the sidebar deck-list shipped (`lib/store/use-deck-store.ts:343` calls `serverReorderDecks`, `app/actions.ts` persists), but there was no UI affordance to call it.
  - Each deck row gets a `GripVertical` drag handle on the left, opacity-0 until group-hover, positioned `left-1.5 top-2.5 size-5` mirroring the existing More button on the right. Hold-and-drag reorders within `deckOrder` array; on drop, store fires `reorderDecks(newOrder)` and the server action persists.
  - Pointer activation distance 4px (same as deck-board column DnD) so a stray click on the handle won't fire a sort.
  - Per-deck JSX extracted into `SortableDeck` inner component using `useSortable({id: deck.id})` — mirrors the column-card DnD pattern.
  - Outer `DndContext` + `SortableContext` use `verticalListSortingStrategy` + `restrictToVerticalAxis` modifier (decks stack vertically; horizontal drag would be confusing).
  - Layout invariant: `SidebarGroupLabel pl-2 → pl-7` reserves 28px for the drag handle, mirror of the existing `pr-9` reservation for the More button. Reservation is constant (not toggled on hover) so deck names never reflow on mouse-enter.

- `9702d8c` — feat: deck keyboard navigation shortcuts (#66) — +209/-1 across 3 files
  - Shortcuts: `j` / `ArrowRight` → next visible column (wraps); `k` / `ArrowLeft` → previous (wraps); `/` → open focused column's inline search + focus input; `c` → toggle collapse; `Escape` → two-step (clear search → clear focus).
  - State: `focusedColumnId` + `pendingSearchOpen` added to `use-deck-store.ts` as view-state-only fields (NOT persisted, same lifetime as `collapsedColumnIds`/`searchByColumn`/`widthByColumn`). Both scrubbed in `deleteDeck` and `removeColumn`.
  - `pendingSearchOpen` is a **column id** (not a boolean) so a fast `j / j /` sequence lands on the second column's search box, not the first.
  - Window-level listener bails the instant the active element is an input/textarea/select/contenteditable — typing into a search box, configure dialog, or rename field never gets intercepted. Modifier presses (Ctrl/⌘/Alt) also bail so `⌘K` and friends still work.
  - Visual: `ring-2 ring-[color:var(--brand)]/60` on the focused column wrapper on both expanded and collapsed render paths (co-exists with the existing `isDragging` ring).
  - `requestAnimationFrame(() => element.scrollIntoView({inline: "nearest"}))` after `j/k` so the focus ring stays visible when the operator presses past the horizontal scroller edge.

- `183545d` — fix(deck): stand down keyboard nav during an active dnd-kit keyboard drag (#67)
  - **Same-day fix on PR #66.** The window-level `j/k/c/`/`Esc` handler bails when a text field is focused, but a `dnd-kit` keyboard drag (from PR #65) is driven from a `<button>` drag handle — so during an active keyboard reorder the same `ArrowLeft`/`ArrowRight`/`Escape` keys were handled by **both** the `KeyboardSensor` and the column-nav handler.
  - Tracks drag state in a ref (set on `onDragStart`, cleared on `onDragEnd`/`onDragCancel`) and bails the key handler while a drag is in progress, so the `KeyboardSensor` exclusively owns arrows/Escape until the column drops or the drag cancels.
  - A merely-focused (not dragging) handle still allows nav, since arrows don't start a drag — only Space/Enter does.

**Impact:** The per-column UX axis ticks to rung 10 (keyboard nav, after deck DnD at rung 9). Combined with the 8 previous per-column rungs (tab groups → collapse → export → search → pin → duplicate → column-color → width → deck-DnD → keyboard-nav), minitor's deck management has gone from "click everything, one column at a time" to "press j/k to walk the deck, / to search, c to collapse, Esc to leave" in 11 days. PR #67's same-day landing of the keyboard-vs-dnd-kit conflict shows the second-order interaction was caught and resolved in one flow.

---

## Developer Notes

- **New dependencies:** `wrangler` 4.98.0 pinned in `apps/webhook/package.json` (new package). `@anthropic-ai/claude-code` pinned to `2.1.168` in both runner workflows (`aeon.yml` + `messages.yml`).
- **New repo-root files:** `STRATEGY.md` (aeon). `install-from-atrium` (aeon-agent).
- **Breaking changes / repo restructure:** aeon's sub-apps moved from `repo-root/{dashboard,mcp-server,a2a-server,webhook}/` to `repo-root/apps/`. `templates/` → `skill-templates/`. `workflows/` → `workflow-templates/`. External URLs (Cloudflare deploy button, Smithery subfolder) updated to the new paths. Runtimes (mcp-server, a2a-server, dashboard) updated their repo-root resolution.
- **New runtime extension:** Skills can call MCP servers during runs when `.mcp.json` is present at repo root. Default `.mcp.json.example` ships a github + no-auth-stdio template.
- **New base-context import:** `CLAUDE.md` now `@`-imports `STRATEGY.md` → every skill sees the operator's north-star.
- **Architecture shifts:** Aeon's "static skills" model now has two reach-out hooks: (1) `STRATEGY.md` as a north-star imported into every skill's context, (2) MCP servers as a callable fabric. Both are dashboard-managed end-to-end.
- **Tech debt:** Banner art `apps/dashboard/assets/skills-aeon-193.jpg` still reads "193 SKILLS" — needs a design regen + filename rename, called out as follow-up in `c78cab9`. A multi-harness runtime would need an equivalent to Claude Code's `@`-import for `STRATEGY.md` (called out in `feba6a7`).

## What's Next

- **500⭐ trigger imminent:** aeon at 496⭐, v7 ≈3.6/day → ~Jun-11 (Thursday). `star-milestone` auto-dispatch (PR #358, yesterday) will fire `show-hn-draft` when it crosses. The prompt refresh (`f12b9fb`) reflects the product as it exists today (~195 skills / 8 categories / MCP / STRATEGY.md / Atrium install path).
- **`atrium-catalog-watcher` backport (aeon-agent):** unblocked by today's `install-from-atrium` backport. The natural 26th-link in the same-day-after chain.
- **MCP runtime field-testing:** the `.mcp.json` runtime path landed today with `.mcp.json.example` as the only test fixture in-repo. First in-the-wild use will be the first time the bash-substitution fix (`5bba508`) and the `${VAR}` resolver (`0c4aba5`) see a non-trivial config.
- **Cleanup chain remainders:** PRs #359 and #366 are labeled 1/7 and 2/7. Five more cleanup PRs are pending in the same series.
- **Banner art:** `skills-aeon-193.jpg` regen + rename. Flagged as a non-code follow-up in `c78cab9`.
- **Minitor per-deck axis:** with DnD, color, and keyboard nav landed, the per-deck rungs that remain reachable are: per-deck collapse-all, per-deck search-all, per-deck export. The per-column axis has slowed (10 rungs) — the deck axis is the natural next surface.
