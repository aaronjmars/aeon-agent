*Repo Action Ideas — 2026-05-14*
Generated from analysis of aaronjmars/aeon (313⭐, 50 forks), aaronjmars/aeon-agent (62 skills), and aaronjmars/minitor (43 column types). Pipeline was starved — this run seeds tomorrow's feature.

1. Product Hunt Launch Skill (Content, Small)
   Drafts the full PH asset package (tagline, description, comments, bullets) from internal repo state — no external API. Writes a ready-to-submit launch doc and sends it for operator review.

2. Skill Enabler (Feature, Small)
   Takes a comma-separated slug list via var, validates each against aeon.yml, patches enabled: false → true, and opens a PR — directly closes the 'switch is still off' gap flagged in three consecutive repo-articles.

3. Fork Skill Gap (Community, Medium)
   Weekly Sunday skill that diffs each POWER/ACTIVE fork's skills.json against upstream, surfaces the top 3 forks by missing-skill count, and links to a full gap table — pulls fork operators toward upstream adoption without requiring action on their side.

4. Column Keyword Alerts (Feature, Medium)
   Adds an optional alertKeywords field to any Minitor column; matched items get a yellow highlight ring and the column header shows a badge count. Purely client-side — works with all 43 existing column types on day one.

5. Deck Export / Import (DX, Small)
   Serializes a Minitor deck's column list to JSON (copy to clipboard via ⌘K) and re-creates it from a pasted blob — zero infrastructure change, enables community deck sharing.

Full details: https://github.com/aaronjmars/aeon-agent/blob/main/articles/repo-actions-2026-05-14.md
