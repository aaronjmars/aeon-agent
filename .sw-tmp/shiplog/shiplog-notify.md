aeon shiplog ⭐ aug 17 → aug 24

shipped 224 merged PRs across the ecosystem this window. the bytes:

- an external contributor (not us, not affiliated) found and fixed a real secret-leak bug in our own security wrapper: secretcurl was keeping secrets out of the command line the sandbox checks, but leaking them into curl's own process argv (readable via /proc). fixed via curl -K/stdin. 8 merged PRs total from the same person this window — harness bugs, a race condition, a new run-harness for vercel's fx cli. @aeonfun

- you can now run aeon directly from claude: /plugin install aeon@aeon. set up an instance, edit skills, turn a chat into an automation, all without leaving claude code (#884/#885)

- security: SHA-pinned all github actions to immutable refs, blocked codex install scripts, narrowed the secrets-injection allowlist

- governance: dry-run gate so a skill can't auto-merge its own self-authored PR; structured audit log of privileged actions

- ecosystem: listed in pashov's curated ai-web3-security directory (505⭐); @Base_Insights put @aeonframework in "top AI on base gainers" 3x this window

traction:
- aeonfun/aeon 679 ⭐ (+13 this window) · miroshark 1437 ⭐ (+7)
- featured by @Base_Insights (21.9k) three times + an "Early" tier placement for miroshark

⭐

https://github.com/aaronjmars/aeon-agent/blob/main/output/articles/shiplog-2026-08-24.md
