*Push Recap — 2026-05-22*
aeon (3) + aeon-agent (2) + minitor (1) — 6 commits by 2 authors (@aaronjmars 4, AntFleet 2)

Community Skill Pack install protocol: aeon shipped ./install-skill-pack CLI + skills-pack.json manifest schema (PR #213, +720 lines) closing Issue #185's implied install gap; AntFleet/aeon-skills added to trusted-sources 23 min later (PR #211) — first third-party pack to clear fast-path install, same-window operator validation.

Fleet-state hardening: AntFleet bench review caught two latent bugs in skills/fleet-state (PR #207) — empty-history abort under set -euo pipefail when contributor-spotlight has never run, and a Sandbox note that claimed no gh api calls while Step 2 made two; both fixed in one commit with explicit PARENT_OVERRIDE escape hatch documented.

macOS scanner backport: aeon-agent PR #56 verbatim-backports upstream PRs #186 (Bash 3.2 array-emptiness) + #197 (POSIX-ERE \s/\b → [[:space:]] + ($|[^[:alnum:]_-])); 28 patterns rewritten across HIGH/MEDIUM/LOW arrays — closes silent-degradation hazard for every macOS operator (BSD grep was treating PCRE escapes as literals; eval\s, rm\s+-rf\s+/, prompt-injection patterns all no-op'd).

Self-improve word boundary: aeon-agent PR #57 fixes ./notify substring matcher in aeon.yml that silently swallowed real notifications containing test/trace/ping/debug inside another word ("Latest token-report", "Shipping 3 PRs", "Tracer code", "Pinging operator"); threshold lowered 120→60, two heredoc blocks patched.

Minitor onboarding gap: PR #47 ships four pre-baked deck templates (AI Research, Base Ecosystem, Crypto DeFi, Startup Tracker — last fully keyless) via onboarding screen + ⌘K command, served through existing DeckExport v1 + importDeck path (no new schema/route). Two clicks from blank install to live dashboard.

Key changes:
- install-skill-pack (+546 lines Bash, 5 flags including --list/--path/--branch/--yes/--force/--dry-run) — the first one-command install surface for community packs since the README section was added
- aeon-agent .github/workflows/aeon.yml notify heredoc: glob substring → bash regex word-boundary (^[^a-z]*(test|trace|ping|debug)([^a-z]|$)) in both inline + post-run pending-notify replay blocks
- minitor lib/deck-templates.ts (+273 lines, TS not JSON so brand color + lucide icon travel with payload) — DeckExport v1 schema unchanged, fifth template is a single-record PR

Stats: 13 files changed, +1582/-81 lines across 6 substantive commits
Full recap: articles/push-recap-2026-05-22.md (in aaronjmars/aeon-agent)
