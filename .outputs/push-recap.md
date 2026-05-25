*Push Recap — 2026-05-25*
13 substantive commits across aeon / aeon-agent / minitor by 4 authors. Theme of the day: hardening + distribution, not new capability.

*aeon (8):* Two AntFleet CI-security patches — workflow_dispatch input is now allowlist-validated + env-passed (no more template-into-bash injection, #222) and the gateway parser's fragile tr-d quoting → sed (#223). Closed the LAST open AntFleet High: v4-readiness named 4 files it never read → silent false-clean READY, now trips PARTIAL instead (#226). New ecosystem-pulse skill (weekly ECOSYSTEM.md liveness check, #227). Wired the 34 ported skills that #219 added to the catalog but never registered in aeon.yml — they couldn't run until now (#230). Plus 3 inbound ecosystem doc PRs (LiquidPad, MythosForge, +5 projects self-listing).

*aeon-agent (3):* Backported the community skill-pack install protocol (install-skill-pack CLI + registry, +991, #59) and config-validator — adapted, not copied, so it doesn't false-positive on aeon-agent's conditional checkout (#61). fetch-tweets now fails LOUD: HTTP-code-keyed PREFETCH_FAILED variants (403 → credits top-up link) + a required Notification-sent log line for heartbeat (#60) — same-week response to the May-24 XAI 403.

*minitor (2):* Columns went active — per-column auto-refresh (1/5/15/60m, background-tab pause, #49) and per-column webhook alerts with an SSRF-guarded validator + no-redirect sender, secret-bearing URLs kept out of the public share export (#50).

Key changes:
- aeon #222: inputs.skill no longer interpolated into bash source — allowlist-validated `^[a-zA-Z0-9_-]+$`, passed via env
- minitor lib/columns/webhook.ts (+166): https-only SSRF guard (RFC-1918/loopback/CGNAT/multicast + IPv6), 5s bounded `redirect:"error"` sender
- aeon #230: 34 ported skills finally schedulable (still enabled:false); README/image synced 121→156

Stats: 46 files changed, +3,198 / -58
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-25.md
