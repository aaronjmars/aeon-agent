*Push Recap — 2026-06-09*
33 substantive commits across aeon/aeon-agent/minitor — biggest push day this fork has audited.

*aeon (~27 commits):* Dashboard rebuilt to provision MCP servers + secrets in one screen. Skills can now call MCP servers during runs (opt-in via .mcp.json) — runner resolves every ${VAR} from repo secrets, discards the blob before any skill code runs, gracefully skips MCP on unset vars instead of crashing the step. Sub-apps (dashboard/, mcp-server/, a2a-server/, webhook/) moved into apps/. STRATEGY.md shipped + @-imported into CLAUDE.md so every skill run inherits the operator's north-star. Telegram poller stopped double-dispatching on ack-failure; instant-mode Worker became one-click Cloudflare deploy. Skill count reconciled to 195 across 8 canonical categories. Seven-PR cleanup chain (types, error masking, dead imports, decorative comments) made dents 1/7 and 2/7. show-hn-draft prompt refreshed for the 500⭐ auto-fire — aeon at 496⭐, ~Jun-11.

*aeon-agent (3 PRs):* ecosystem-links backport (#87, 24th consecutive), runner-hook restriction consolidated into CLAUDE.md (#89), install-from-atrium backported (#90, 25th — first non-SKILL.md backport in the chain, unblocks atrium-catalog-watcher).

*minitor (3 PRs):* Per-deck drag-to-reorder via @dnd-kit (#65). Full j/k///c/Esc keyboard nav (#66, rung 10 on the UX axis). Same-day follow-up (#67) stands down the nav handler during an active dnd-kit keyboard drag so KeyboardSensor exclusively owns arrows/Escape until drop.

Key changes:
- aeon #372/#378/#381: MCP runtime + auto-resolve + inline secret-set per server row
- aeon #370/#371: STRATEGY.md + @-import in CLAUDE.md + dashboard editor
- aeon #376: 129-file restructure moving 4 sub-apps under apps/

Stats: ~250+ files touched, ~3,200+ net lines added.
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-06-09.md
