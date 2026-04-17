*Push Recap — 2026-04-17*
aeon-agent — 14 commits, aeon — 1 commit, 2 authors

Fetch Tweets Pipeline Overhaul (8 commits): The fetch-tweets skill went from 4+ days of FETCH_TWEETS_EMPTY to reliably returning 10+ tweets per run. Rebuilt the entire pipeline: cache-first XAI reads, broadened OR-based search queries, a Python post-filter for false positive bare-word matches, and persistent dedup via seen-file that survives log rotation.

Tweet Allocator $AEON Rewards (4 commits): New skill distributes $10/day in $AEON to top tweeters. Rapid iteration from USDC to native $AEON denomination, Bankr wallet as single verification gate (no more unverified pending states), and required-token filter to prevent off-topic rewards.

Skill Dependency Graph (1 commit, aeon repo): New meta-skill generates a Mermaid map of all 91 skills grouped by category. 73/91 fully independent, 5-skill self-healing loop, 4-skill content pipeline highlighted.

Infrastructure Fixes (2 commits): Telegram notifications switched from legacy Markdown to HTML mode — underscores in handles no longer eaten. Chain-runner .outputs/ unignored so skill outputs pass between steps.

Key changes:
- scripts/filter-xai-tweets.py — new 110-line post-filter drops bare-word aeon matches from Grok results
- scripts/prefetch-bankr.sh — new 133-line script pre-fetches Bankr wallets outside sandbox
- skills/tweet-allocator/SKILL.md — simplified from 201 to 114 lines, Bankr wallet is the only gate
- docs/skill-graph.md — 245-line Mermaid diagram with 91 nodes and 18 dependency edges

Stats: ~15 files changed, +1,050/-250 lines
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-04-17.md
