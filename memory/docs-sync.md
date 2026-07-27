---
type: Reference
title: Docs Sync config
description: Config for the changelog skill's push-to mode — which product repo's merged PRs become the changelog, and which marketing-site repo to open the PR against.
---

# Docs Sync config

Config for the `changelog` skill in push-to mode (this file keeps its name — the
skill still reads `memory/docs-sync.md`). Defines which product repo's merged PRs
become the changelog, and which marketing-site repo to open the PR against.

- product_repo: aaronjmars/aeon
- website_repo: aaronjmars/aeon-website
- min_prs: 1
- lookback_days: 7
- draft: true
- git_user_name: aeonframework
- git_user_email: aeonframework@proton.me
