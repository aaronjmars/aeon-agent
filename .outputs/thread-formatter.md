*Thread Draft — 2026-06-17*
Topic: validate-pack.sh — pre-flight validator for community skill packs (PR #495)

1/ aeon ships a pre-flight validator for community skill packs. validate-pack.sh — broken slugs, missing SKILL.md, invalid capabilities, path traversal — caught before you open a PR.

2/ packs install into aeon via PR. the validator logic lived inside install-skill-pack.sh — Actions only. zero way to check locally before opening a PR.

3/ validate-pack.sh runs the same checks as install-skill-pack locally. malformed JSON, bad slugs, path traversal (no ..), absent SKILL.md, off-taxonomy capabilities — all exit 1. capability taxonomy pulled from install-skill-pack at runtime, never hardcoded.

4/ pack template (#494) and validate-pack.sh (#495) shipped back to back. the template says what to include. the validator says whether it's correct. together they close the pre-PR gap — submitters know before the maintainer looks.

5/ validate-pack.sh for aaronjmars/aeon — PR #495: https://github.com/aaronjmars/aeon/pull/495

(article: articles/thread-2026-06-17.md)
