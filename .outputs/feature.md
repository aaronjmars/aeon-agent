*Feature Built — 2026-06-17 — aaronjmars/aeon* ⭐

validate-pack.sh — pre-flight your community pack before the PR

one command that tells a pack author if their pack is actually installable: `./scripts/validate-pack.sh /path/to/pack-dir`. it runs the exact same checks `install-skill-pack` does, prints a ✅/⚠️/❌ line per check, exits 0 if clean and 1 if not. no more "open a PR and find out."

Why this matters:
last week shipped the PR template for pack submissions (#494). but the real friction is earlier: does my pack even meet the spec the installer enforces? until now the only way to find out was open a PR and wait for a reject. this closes that loop — author validates locally, fixes it, then opens a clean PR. lower fork friction, fewer review round-trips. (repo-actions idea #3.)

What was built:
- scripts/validate-pack.sh: validates skills-pack.json + slugs + paths + per-skill SKILL.md + capability taxonomy. ERRORs (invalid json, bad slug, `..` in path, missing SKILL.md, unknown capability) fail with exit 1; WARNINGs (missing license, default_enabled on a write skill, on-disk skill not in manifest) are advisory.
- CONTRIBUTING.md + docs/community-skill-packs.md: wired the validator into the "listing a pack" section and the publishing checklist.

How it works:
pure-local, zero network — nothing the Actions sandbox blocks. the locked capability taxonomy isn't hardcoded: it's pulled at runtime straight from install-skill-pack's ALLOWED_CAPABILITIES array (same awk extraction check-capabilities-parity.sh uses) so there's no fourth copy to drift. slug/path/SKILL.md checks mirror the installer's manifest parser line-for-line. reads json with jq, same dep as install-skill-pack.

What's next:
this pairs with the auto-comment review workflow (idea #5, still blocked on a workflows-scoped token) — same checklist, but posted on the PR automatically. validate-pack.sh is the runnable spec that workflow would point at.

PR: https://github.com/aaronjmars/aeon/pull/495
