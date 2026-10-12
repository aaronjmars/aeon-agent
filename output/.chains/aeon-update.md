ℹ️ aeon-update: 27 commits → PR #259

*aeon-update ⭐ 2026-10-12*
synced 27 upstream commits → PR #259

upstream `aeonfun/aeon` is 27 ahead (`1a7f07e..df013db`, 10-05→10-10). 184 files applied clean, 5 need a hand-merge.

mostly the **hosted MCP server** (drive your agent from ChatGPT/Claude/Cursor at www.aeon.fun/connect/mcp), the **Haiku 5.5** tier move, CI hardening (apt-hang fix, harness-adapter snapshot, npm-cache restore-keys drop), a Biome formatter, and plugin-manifest cleanup. 3 files 3-way auto-merged, 2 retired, catalogs + eyebrowlock reconciled.

manual (not written): `.github/workflows/aeon.yml` is the one worth pulling in by hand — it ships the apt-hang guard + harness-snapshot run-loop fixes, but overlaps your local workflow edits. also `.github/README.md`, `CHANGELOG.md`, `llms.txt`, `docs/examples/README.md` — all your instance narrative sitting on the same lines upstream added hosted-MCP pointers.

all gates green locally: eyebrow verify --ci (rc0), validate-config, validate-skill-packs, categories, parity, skill-sync. baseline moves to `df013db` on merge.

PR: https://github.com/aaronjmars/aeon-agent/pull/259

🔗 https://github.com/aaronjmars/aeon-agent/pull/259