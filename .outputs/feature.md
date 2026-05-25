*Feature Built — 2026-05-25 — aaronjmars/minitor*

Per-Column Alert Webhooks
Minitor columns can now POST to a webhook when alert keywords match. Set keywords on a column, add an https URL, and every time a refresh pulls in new items matching those keywords, Minitor fires a JSON payload to that URL — Slack, Discord, Zapier, n8n, anything. It's the difference between "I'll see it if I'm looking at the dashboard" and "I get pinged the moment it happens."

Why this matters:
Alert keywords (added in PR #41) only gave a yellow ring and a badge count — passive signals that require someone watching the screen. For serious monitoring — infra alerts, competitor launches, token moves, security CVEs — visual-only isn't enough. This adds the missing layer between "I see it" and "I'm notified," and it works with every one of Minitor's column types because it sits at the column level, not inside any plugin. It was the May-24 repo-actions idea #5 (idea #4, a Bluesky column, was already merged on main).

What was built:
- drizzle/0002_notify_webhook.sql (+ journal + snapshot): a nullable notify_webhook_url column.
- lib/columns/webhook.ts: an SSRF-guarded URL validator (https-only; blocks localhost and private/internal IP ranges) plus a bounded, fire-and-forget sender that refuses redirects and logs only to the server console.
- app/actions.ts: a server action to save the URL, and webhook firing wired into the fetch-persist path so it only triggers on genuinely new matching items.
- Configure dialog: an "Alert webhook URL" field that appears once keywords are set, with live validation.

How it works:
The webhook fires server-side inside persistFetchedItems, keyed strictly on new arrivals — re-fetching items you've already seen never re-notifies. The payload carries the column id/title/type, the matched items (id, url, text, which keywords fired), and a timestamp. A deliberate security choice: the webhook URL is never included in deck exports or share links, because a webhook URL often embeds a secret token and the same export feeds the public share link — leaking it would hand that secret to anyone the deck is shared with. It stays in the database and is re-entered on import.

What's next:
Could add a payload signing secret (HMAC header) so receivers can verify authenticity, and a per-column delivery-status indicator. Note: the Next 16 build/type-check couldn't run in the offline build sandbox, so the change was verified by manual review.

PR: https://github.com/aaronjmars/minitor/pull/50
