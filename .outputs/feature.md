*Feature Built — 2026-04-18*

Farcaster Syndication (Run 2)
Aeon articles now cross-post to Farcaster the same way they cross-post to Dev.to. The existing `syndicate-article` skill got a second channel — every article that runs through it can now land as a cast on Farcaster via Neynar, reaching the crypto-native audience that overlaps most directly with AEON token holders and DeFi users.

Why this matters:
Dev.to reaches developers. Farcaster reaches the people actually holding the token. With AEON up +109% in 7 days and the 200-star milestone imminent, the gap was a distribution one — not content. This is idea #2 from the Apr 16 repo-actions batch and the cleanest-scoped one left: piggybacks on the existing Dev.to post-process pattern, zero new infra, one new script. Channels are independent — set `DEVTO_API_KEY` and Dev.to activates; set `NEYNAR_SIGNER_UUID` and Farcaster activates; set both and every article fans out to both.

What was built:
- scripts/postprocess-farcaster.sh: new post-process hook. Reads `.pending-farcaster/*.json`, injects `NEYNAR_SIGNER_UUID` from env at POST time (so the signer never touches disk), POSTs to https://api.neynar.com/v2/farcaster/cast with `x-api-key: $NEYNAR_API_KEY`, cleans up payloads on success. Handles 400/422 (duplicate), 401/403 (auth), and other errors non-fatally.
- skills/syndicate-article/SKILL.md: rewritten to treat Dev.to and Farcaster as independent channels with per-channel duplicate detection (SYNDICATED: vs FARCAST: log markers). If one channel is already posted, the other still runs. Writes the Farcaster payload (text + embed URL, no signer) to `.pending-farcaster/<slug>-<date>.json` during its run.
- .github/workflows/aeon.yml: passes `NEYNAR_SIGNER_UUID` to the Claude step and passes `DEVTO_API_KEY`, `NEYNAR_API_KEY`, `NEYNAR_SIGNER_UUID` to the post-process step. Drive-by fix: `DEVTO_API_KEY` was missing from the post-process env block entirely, so `postprocess-devto.sh` had been silently skipping every run.
- dashboard/app/api/secrets/route.ts: adds `NEYNAR_API_KEY` and `NEYNAR_SIGNER_UUID` to the Distribution group so operators can configure them from the dashboard Secrets panel alongside `DEVTO_API_KEY`.
- .gitignore: adds `.pending-devto/` and `.pending-farcaster/` so failed payloads never accidentally land in a commit.

How it works:
The skill never calls Neynar inline. During its run it just writes a JSON payload — cast text (`New post: <title>\n\n<url>`) plus an embed URL — to `.pending-farcaster/`. After Claude finishes, the workflow's post-process step runs every `scripts/postprocess-*.sh` hook; `postprocess-farcaster.sh` picks up the payload, injects the signer UUID at the last possible moment, POSTs to Neynar, and deletes the file on success. This mirrors the Dev.to pattern exactly and sidesteps the sandbox's env-var-in-curl-headers limitation. The signer UUID — the credential that actually controls which Farcaster account posts — is never written to disk, never committed, and only exists in the GitHub Actions runner env for the duration of the post-process step.

What's next:
Could add channel posting (`channel_id: "aeon"`) once a dedicated Farcaster channel exists, or fan Farcaster syndication out to a second publisher skill (repo-article, changelog) rather than only the article pipeline. The next unbuilt repo-actions ideas are Dashboard Live Feed (SSE for dashboard/outputs/) and Public Status Page (30-day skill health at docs/status.md).

PR: https://github.com/aaronjmars/aeon/pull/40
