# Changelog - Week of 2026-10-08

*Window: 2026-10-01 → 2026-10-08 · Sources: aeonfun/aeon=ok, aeonfun/minitor=empty, aeonfun/opendia=ok, aeonfun/soul.md=empty*

## aeonfun/aeon

> **Highlights:** Onboarding got a real fast path - `aeon init`, `aeon auth`, and a one-shot dashboard connect flow that now leads with the hosted Aeon Connect option - alongside October's model lineup (Sonnet/Opus 5.5, Grok 4.7, GPT-6 Luna, Kimi K2.6, GLM 5.3, Cursor Auto) across every harness. A same-week security sweep closed a sandbox parent-rename escape, pinned third-party harness installers, and hardened the secrets allowlist.

### Security
- Closed a sandbox escape where a read-only run could rename a protected directory's parent to make the read-only mount point at attacker-controlled data, since `--ro-bind` only pins the exact path named. ([#1132](https://github.com/aeonfun/aeon/pull/1132))
- Pinned third-party harness installers and locked later-step paths against supply-chain tampering; a coordinated audit batch also hardened the dashboard bind address, workflow-injection surface, `secretcurl`, webhook intake, and the secrets allowlist. ([#1122](https://github.com/aeonfun/aeon/pull/1122), [#1114](https://github.com/aeonfun/aeon/pull/1114), [#1116](https://github.com/aeonfun/aeon/pull/1116))
- The secret tripwire now catches GitHub's new stateless `ghs_` installation-token format, which it previously missed. ([#1177](https://github.com/aeonfun/aeon/pull/1177))

### Added
- New `aeon init` CLI command with a credential manifest and a drift test, plus `aeon auth --harness claude-code`, to make first-run setup scriptable instead of manual. ([#1158](https://github.com/aeonfun/aeon/pull/1158), [#1133](https://github.com/aeonfun/aeon/pull/1133))
- Dashboard onboarding: one-shot model connect with a live connect-check and setup checklist, a mobile-friendly layout, and an HQ view that explains failed runs instead of just a silent post-connect test run. ([#1157](https://github.com/aeonfun/aeon/pull/1157), [#1154](https://github.com/aeonfun/aeon/pull/1154), [#1160](https://github.com/aeonfun/aeon/pull/1160))
- October's model lineup landed across every harness - Sonnet/Opus 5.5, Grok 4.7, GPT-6 Luna, Kimi K2.6, GLM 5.3, Cursor Auto - plus MCP support wired into pi and a three-model Codex picker in the dashboard. ([#1124](https://github.com/aeonfun/aeon/pull/1124), [#1131](https://github.com/aeonfun/aeon/pull/1131), [#1139](https://github.com/aeonfun/aeon/pull/1139))
- Every run now reports which `STRATEGY.md`, soul, and MCP config it loaded, and the run summary shows which model actually ran. ([#1147](https://github.com/aeonfun/aeon/pull/1147), [#1141](https://github.com/aeonfun/aeon/pull/1141))
- New README section on being "private by design," with a privacy comparison. ([#1166](https://github.com/aeonfun/aeon/pull/1166))
- Community skill packs added to the catalog: Epoch, Messaging, and "bon travail." ([#1168](https://github.com/aeonfun/aeon/pull/1168), [#1164](https://github.com/aeonfun/aeon/pull/1164), [#1167](https://github.com/aeonfun/aeon/pull/1167) by @Svector-anu)

### Changed
- Onboarding docs now lead with the hosted Aeon Connect flow instead of self-host-first, and point to the hosted MCP server at aeon.fun/connect/mcp. ([#1163](https://github.com/aeonfun/aeon/pull/1163), [#1192](https://github.com/aeonfun/aeon/pull/1192))
- Model pickers trimmed across the board (3 Claude models, 2 Codex models, fewer pi/vibe/hermes/kimi/grok choices), and the haiku tier moved to Claude Haiku 5.5. ([#1138](https://github.com/aeonfun/aeon/pull/1138), [#1146](https://github.com/aeonfun/aeon/pull/1146), [#1161](https://github.com/aeonfun/aeon/pull/1161), [#1189](https://github.com/aeonfun/aeon/pull/1189))
- Every harness CLI bumped to latest (grok 1.x, kimi 2.x, ccr 3.x) with a CI smoke test per harness. ([#1125](https://github.com/aeonfun/aeon/pull/1125))

### Removed
- Dropped `install-from-atrium` and 8 dead/low-value community skill packs from the catalog. ([#1156](https://github.com/aeonfun/aeon/pull/1156), [#1155](https://github.com/aeonfun/aeon/pull/1155))

### Fixed
- A CI step hang (`apt-get update`) was killing unrelated read-only skill runs; the harness now runs from a snapshot so a skill that syncs its own harness-adapter can't break its own run. ([#1186](https://github.com/aeonfun/aeon/pull/1186), [#1180](https://github.com/aeonfun/aeon/pull/1180))
- MCP server runs now use the resolved model and a real 1800s timeout instead of an undefined cron, and the base MCP server gives scheduled runs a real task. ([#1191](https://github.com/aeonfun/aeon/pull/1191), [#1190](https://github.com/aeonfun/aeon/pull/1190), [#1150](https://github.com/aeonfun/aeon/pull/1150))
- Dashboard: Strategy/Soul reload after a successful builder run, long instance titles no longer overflow, and `next dev` no longer writes files the PUSH button would accidentally commit. ([#1153](https://github.com/aeonfun/aeon/pull/1153), [#1136](https://github.com/aeonfun/aeon/pull/1136), [#1159](https://github.com/aeonfun/aeon/pull/1159))
- Scheduler/workflow reliability: failed-run retries and breaker probes stay on the skill's own cadence, concurrent state survives commit/push retries, and `messages.yml` post-run state stays off feature branches. ([#1119](https://github.com/aeonfun/aeon/pull/1119), [#1117](https://github.com/aeonfun/aeon/pull/1117), [#1120](https://github.com/aeonfun/aeon/pull/1120))
- Model-mapping bugs fixed (dispatch ids, `GROK_MODEL`, hermes default, dry-run, scorecard pricing); Codex now honours the picked model on a ChatGPT login instead of silently falling back. ([#1123](https://github.com/aeonfun/aeon/pull/1123), [#1144](https://github.com/aeonfun/aeon/pull/1144))
- Two external-contributor fixes: PR review/auto-merge now checks GitHub before re-reviewing or reporting a stale merge, and the `feature` skill checks for an open PR before branching and verifies `Closes #N`. ([#1128](https://github.com/aeonfun/aeon/pull/1128), [#1126](https://github.com/aeonfun/aeon/pull/1126) by @Svector-anu)
- Read-only skills no longer double-log, and dropping `restore-keys` on the Claude Code npm cache means CI pin bumps actually install. ([#1121](https://github.com/aeonfun/aeon/pull/1121), [#1169](https://github.com/aeonfun/aeon/pull/1169))

*Internal: 22 commits hidden (plugin-directory manifests, docs syncs, skill-doc refreshes, CI workflow tuning, tests). Bots filtered: 5 (dependabot).*

---

## aeonfun/opendia

> **Highlights:** Two patch releases shipped this week (v1.1.3, v1.1.4) - a dependency security patch and three small bug fixes, no new features.

### Security
- Patched a brace-expansion vulnerability in the browser extension's dependency chain; upstream `node-forge` doesn't have a fix yet, so this is a local workaround. ([#88](https://github.com/aeonfun/opendia/pull/88))

### Changed
- Slimmed the DXT bundle size. ([#87](https://github.com/aeonfun/opendia/pull/87))

### Fixed
- The DXT package now actually applies `user_config` settings to the server, `get_page_links` treats subdomains as internal, and the MCP server advertises its real package version. ([#86](https://github.com/aeonfun/opendia/pull/86), [#83](https://github.com/aeonfun/opendia/pull/83), [#82](https://github.com/aeonfun/opendia/pull/82))

*Internal: 2 commits hidden (v1.1.3 and v1.1.4 release bumps). Bots filtered: 1 (dependabot).*

---

## aeonfun/minitor

No user-facing changes this week; 0 internal commits.

---

## aeonfun/soul.md

No user-facing changes this week; 0 internal commits.
