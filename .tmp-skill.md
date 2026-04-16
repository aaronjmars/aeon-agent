---
name: syndicate-article
description: Cross-post articles to Dev.to for wider developer reach
var: ""
tags: [content, growth]
---
> **${var}** — Filename of a specific article to syndicate (e.g. `repo-article-2026-04-16.md`). If empty, syndicates the most recently written article.

Cross-post Aeon articles to [Dev.to](https://dev.to) for organic developer discovery. Articles are published with a canonical URL pointing back to the GitHub Pages gallery, preserving SEO attribution.

## Prerequisites

- `DEVTO_API_KEY` — Dev.to API key. Generate at https://dev.to/settings/extensions (scroll to "DEV Community API Keys"). If not set, the skill logs a skip and exits silently — no error, no notification.

## Steps

1. **Check for API key** — verify `DEVTO_API_KEY` is available:
   ```bash
   if [ -z "$DEVTO_API_KEY" ]; then
     echo "SYNDICATE_SKIP: DEVTO_API_KEY not configured"
     exit 0
   fi
   ```
   If missing, log "SYNDICATE_SKIP: DEVTO_API_KEY not configured" to `memory/logs/${today}.md` and stop. Do NOT send any notification.

2. **Select the article to syndicate:**
   - If `${var}` is set, use `articles/${var}` directly.
   - Otherwise, find the most recently modified `.md` file in `articles/` (excluding `feed.xml` and `.gitkeep`):
     ```bash
     ls -t articles/*.md 2>/dev/null | head -1
     ```
   - If no articles exist, log "SYNDICATE_SKIP: no articles found" and stop.

3. **Check for duplicates** — before posting, check if this article was already syndicated:
   - Search the last 7 days of `memory/logs/` for `SYNDICATED:` entries containing this filename.
   - If found, log "SYNDICATE_SKIP: already syndicated {filename}" and stop.

4. **Parse the article:**
   - **Title**: Extract from the first `# Heading` line. If the article has Jekyll frontmatter with a `title:` field, use that instead.
   - **Body**: Everything after the first heading (or after frontmatter if present). Clean up any Jekyll-specific liquid tags.
   - **Date**: Extract `YYYY-MM-DD` from the filename using regex `([0-9]{4}-[0-9]{2}-[0-9]{2})`.
   - **Slug**: Everything before the date in the filename, with trailing hyphens removed.

5. **Determine tags** from the filename slug (max 4 tags for Dev.to):
   - `repo-article`, `article` → `ai, github, automation, agents`
   - `token-report`, `token-alert`, `defi-overview`, `defi-monitor` → `crypto, defi, blockchain, trading`
   - `changelog`, `push-recap`, `weekly-shiplog` → `opensource, devops, changelog, github`
   - `digest`, `rss-digest`, `hacker-news` → `news, tech, ai, digest`
   - `deep-research`, `research-brief`, `paper-pick` → `research, ai, machinelearning, papers`
   - `technical-explainer` → `tutorial, ai, explainer, programming`
   - Everything else → `ai, automation, agents, programming`

6. **Build the canonical URL** pointing to the GitHub Pages post:
   ```
   https://aaronjmars.github.io/aeon/articles/YYYY/MM/DD/<slug>/
   ```
   Where `<slug>` is derived the same way `update-gallery` builds Jekyll post filenames: title lowercased, spaces replaced with hyphens, special characters removed, truncated to 50 chars.

7. **Post to Dev.to** using WebFetch (not curl, due to sandbox auth limitations):
   - Use WebFetch to POST to `https://dev.to/api/articles` with headers:
     - `Content-Type: application/json`
     - `api-key: <DEVTO_API_KEY>`
   - Request body:
     ```json
     {
       "article": {
         "title": "<extracted title>",
         "body_markdown": "<article body>",
         "published": true,
         "tags": ["tag1", "tag2", "tag3", "tag4"],
         "canonical_url": "<github pages URL>",
         "series": "Aeon"
       }
     }
     ```
   - Parse the response for the `url` field (the Dev.to article URL) and `id`.
   - **If WebFetch cannot send POST requests with custom headers**, fall back to the post-process pattern (see Sandbox note).

8. **Handle errors:**
   - If the API returns 422 (title already taken / duplicate), log "SYNDICATE_SKIP: article already exists on Dev.to" and stop gracefully.
   - If the API returns 401, log "SYNDICATE_ERROR: DEVTO_API_KEY is invalid" and stop.
   - If any other error, log the status code and response body.

9. **Log the result** to `memory/logs/${today}.md`:
   ```
   SYNDICATED: {filename} → {devto_url}
   ```

10. **Send notification** via `./notify`:
    ```
    Article syndicated to Dev.to

    "{article title}" is now live on Dev.to, reaching 1M+ developers beyond our GitHub Pages audience.

    Dev.to: {devto_url}
    Original: {canonical_url}
    ```

## Sandbox note

The Dev.to API requires `DEVTO_API_KEY` in request headers. Since the sandbox blocks env var expansion in curl headers, use **WebFetch** for the API call — WebFetch can make authenticated HTTP requests. If WebFetch cannot pass custom headers, fall back to the post-process pattern: write the request payload to `.pending-devto/post.json` and let `scripts/postprocess-devto.sh` execute the actual API call after Claude finishes.
