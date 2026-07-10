---
type: Article
---

# Push Recap — 2026-06-21

## Verdict
> SHIPPING — Charon policy pack in registry, MCP docs ship, Dependabot first run

**Shape:** 2 user-visible commits · 4 internal · 3 infra · 10 bot-filtered
**Volume:** ~25 files changed, ~500 lines across 9 non-automation commits by 2 authors
**Merged PRs:** 7 human (#511 Charon AEON skill pack; #512 MCP server README; #513 Dependabot config; #526 dashboard dedupe; #527 ecosystem logo fixes; #528 ecosystem additions; #109 CLAUDE.md sandbox doc) + 12 dependabot = 19 total

---

## Top impact today
1. `25d2544` — MCP server README ships. Adds a full quickstart to `apps/mcp-server/` — `./add-mcp` flags, `aeon-<slug>` tool naming contract, Claude Desktop config snippet, `test_connection.py` round-trip, how-it-works — closing the onboarding gap the A2A gateway had before #501. (2 files, +99/−0)
2. `78656c0` — Dependabot activates. New `.github/dependabot.yml` — 5 update blocks (github-actions + 4 npm apps), weekly Monday schedule — and within hours fires 12 PRs that all merge the same day, including a TypeScript 5→6 major bump. (1 file, +70/−0)
3. `1f08cd9` — Charon joins the skill registry. External contributor CharonAI-code adds `charon-setup` + `charon-policy` to `skill-packs.json` — repo-local policy enforcement for Aeon runs, no secrets required, community trust. (2 files, +16/−1)

---

## aaronjmars/aeon

### Developer Surface Expansion

**What this is:** Two onboarding gaps close on the same day. The MCP server now has a README documenting its quickstart, tool naming, and Claude Desktop wiring — matching the A2A gateway docs from last week. Separately, the community skill registry gains its first policy-enforcement pack, from an external contributor.

**Shipped to users**
- `25d2544` — docs: add apps/mcp-server/README.md with quickstart and Claude Desktop config (#512)
  - `apps/mcp-server/README.md`: New file — documents `./add-mcp` flags (`--desktop`, `--build-only`, `--uninstall`), tool naming convention (`aeon-<slug>` + generated description format), `var` contract, Claude Desktop JSON config snippet, `test_connection.py` round-trip, and how-it-works (stdio/StdioServerTransport, `skills.json` discovery). (+99/−0)
  - `README.md`: One-line pointer added to the MCP section, mirroring the existing A2A link. (+1/−0)
- `1f08cd9` — Add Charon AEON skill pack (#511) by CharonAI-code
  - `skill-packs.json`: New registry entry — `CharonAI-code/charon`, path `skills/aeon`, 2 skills (`charon-setup`, `charon-policy`), capabilities `external_api`+`writes_external_host`, no required secrets, MIT license. (+15/−1)
  - `README.md`: Row added to the community packs table. (+1/−0)

### Dependency Hygiene (infra)

**What this is:** The Dependabot config that Aeon shipped yesterday (#513, merged 12:42 UTC) triggered 12 automated PRs within the same hour — all merged by 14:00 UTC. Two required human attention: TypeScript 5.9.3→6.0.3 on both mcp-server and a2a-server included a one-line tsconfig fix (`compilerOptions.types: ["node"]`) because TS6 dropped implicit `@types/node` globals under NodeNext. The fix was co-authored into the PR. Everything else was pure version bumps.

**Infra**
- `78656c0` — chore: add Dependabot for npm apps and GitHub Actions (#513)
  - `.github/dependabot.yml`: New file — 5 update blocks (github-actions root + npm for dashboard, mcp-server, a2a-server, webhook), weekly Monday, 5-PR limit, `chore(deps)`/`chore(deps-dev)` prefix. (+70/−0)
- `d527022` — chore(deps-dev): bump typescript 5.9.3→6.0.3 in /apps/mcp-server + tsconfig fix (#518)
  - `apps/mcp-server/tsconfig.json`: Added `"types": ["node"]` — TS6 NodeNext no longer auto-includes `@types/node` without this field. (+1/−0)
- `6eb1720` — chore(deps-dev): bump typescript 5.9.3→6.0.3 in /apps/a2a-server + tsconfig fix (#521)
  - `apps/a2a-server/tsconfig.json`: Same `types: ["node"]` fix applied. (+1/−0)

**Under the hood** *(remaining 10 dependabot merges — pure package.json/lock/workflow bumps, bot-filtered)*
- actions/checkout 4→7, actions/setup-node 5→6, @types/node 22→26 (mcp) and 20→26 (a2a), gsap 3.14.2→3.15.0, tailwindcss 4.2.2→4.3.1, next 16.2.6→16.2.9, yaml 2.8.3→2.9.0, @json-render/shadcn 0.15→0.19, wrangler 4.98→4.103. Bot-filtered: 10.

### Internal: Ecosystem & Dashboard Maintenance

- `6d0ee90` — docs(ecosystem): add ClawHunter, Glim.sh, Lens, LiteBeam, Simmer (#528): 4 new entries to `ECOSYSTEM.md` (the project registry). (+5/−0)
- `be96a3e` — docs(ecosystem): update NÜMETAL and GitKernal logo URLs (#527): Fixes 2 stale Twitter profile image URLs in ECOSYSTEM.md. (+2/−2)
- `2ba612e` — chore(dashboard): align @json-render/core + react on ^0.19 to dedupe (#526): `apps/dashboard/package.json` bumps core+react from ^0.15 to ^0.19, matching the shadcn pin from #516 — collapses two copies of `@json-render/core` in the lockfile into one. (+11/−47 in lockfile)

---

## aaronjmars/aeon-agent

### Internal: Sandbox Rule Documented

- `f535d61` — fix: document compound-bash-command sandbox denial in CLAUDE.md (#109)
  - `CLAUDE.md`: Adds item 3 to Sandbox Limitations — "One operation per Bash call" — covering `&&`/`;`/pipe/subshell/`$VAR` auto-denial. The rule was in MEMORY.md (read on demand per skill) but not in CLAUDE.md (always in context for every run). Evidence cited: feature run 27617695161 lost 4 turns to denied chains. (+3/−1 net in CLAUDE.md itself)

---

## Developer notes
- **New dependencies:** none added (only bumps)
- **Breaking changes:** TypeScript 6.0.3 required `compilerOptions.types: ["node"]` in both mcp-server and a2a-server tsconfigs — one-line fix included in the PR.
- **New public surface:** `charon-setup` and `charon-policy` skills now installable via `./install-skill-pack CharonAI-code/charon --path skills/aeon`; `apps/mcp-server/README.md` now documents the MCP tool contract.
- **Tech debt added:** none

## Open threads
- PR #418 (feat(gateway): add BEAMR as LLM gateway) — stalled since 2026-06-16, last updated 06-16T14:31Z. Flagged in prior heartbeat.
- PR #510 (community skill pack, unknown pack) — external contributor PR, status unknown from this run.

## Sources
- aaronjmars/aeon: ok
- aaronjmars/aeon-agent: ok
- aaronjmars/minitor: ok (empty — 0 commits in window)
- gh api events: partial (jq null iteration, fell back to commits API)
- gh api commits: ok
- gh pr list: ok
- bot-filtered: 10 (aaronjmars/aeon pure dep bumps) + ~22 automation commits (aaronjmars/aeon-agent chore(cron)/scheduler)
- diff-truncated: 0
