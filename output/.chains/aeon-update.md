✅ aeon-update: PR #193

**aeon-update — 2026-08-24**
Synced 43 upstream commits → PR #193

`aeonfun/aeon` `b1d9079..b7a909a`. **83 files applied cleanly** (25 new, 54 modified incl. 10 3-way merges, 4 removed); **5 need a manual merge**.

Highlights: new `fx` Vercel harness + generated `harnesses.json` manifest, `scripts/audit.sh` + `dry-run.sh` gate, Codex plugin (LICENSE/README/SECURITY), dashboard MCP-secret auto-allowlist, webhook update_id dedupe, secretcurl argv hardening.

Manual: `.github/workflows/aeon.yml` · `ci-tests.yml` · `messages.yml` (your local narrowing overlaps upstream's SHA-pin/allowlist edits) · `CHANGELOG.md` · `llms.txt` (upstream added, divergent local copy). `aeon.yml` config changes surfaced in the PR body, not auto-applied.

Baseline advances to `b7a909a` when you merge.

PR: https://github.com/aaronjmars/aeon-agent/pull/193

🔗 https://github.com/aaronjmars/aeon-agent/pull/193