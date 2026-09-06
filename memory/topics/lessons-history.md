---
type: Reference
title: Lessons Learned Archive
description: Older/settled lessons rotated out of MEMORY.md's Lessons Learned section to keep it near budget.
---

# Lessons Learned Archive

Older or settled lessons rotated out of MEMORY.md's Lessons Learned section. Still true, just lower ongoing-reference value than what's kept active.

- Digest format: Markdown with clickable links, under 4000 chars. Always save files AND commit before logging.
- aeon.fun/security's scraper is brittle to upstream markup churn: a CSS-module class rename (`page_row__xxxxx` → `page-module__eEUUaa__row`, 2026-08-22) caused a silent 0/74 PARSE_EMPTY while `cron-state` still recorded `last_status: success` — exact-class selectors can fail without tripping failure detection. Match structurally (owner/repo-shaped capture, GitHub href) instead of by literal class name; secured-watch self-fixed both this and a separate RSC-hydration-payload regex false-positive by 2026-08-23.
