*Feature Built — 2026-05-09 — aaronjmars/minitor*

arXiv Column (38th plugin, AI/ML paper layer)
A new column type that streams the latest papers from arXiv — twelve CS / stat / math.OC categories (cs.AI, cs.CL, cs.LG, cs.CV, cs.RO, cs.CR, cs.DC, cs.NE, cs.SE, cs.PL, stat.ML, math.OC), with sort by newest submission or recently updated, plus an optional title+abstract keyword filter. Keyless — uses arXiv's public Atom-XML query API, no auth required. Each item shows title, author byline, abstract preview, primary + secondary categories, and a direct PDF link.

Why this matters:
huggingface shipped as the 37th column yesterday (PR #30) — covering the AI artifact layer (models, datasets, spaces). The natural companion is the paper layer: arXiv is where the underlying research drops, often 2-3 weeks before the model goes viral on HuggingFace. Together they cover the full artifact-to-research AI pipeline. The audience watching minitor for HuggingFace trending already wants to see what's in the arXiv pipeline; before today, that gap was unfilled. This was Idea #1 in yesterday's repo-actions brief.

What was built:
- lib/integrations/arxiv.ts (~290 lines): hand-rolled Atom-XML client and parser following the same convention as lib/integrations/rss.ts (no XML library dep), specialised for arXiv's namespaced primary-category and PDF-link patterns. Slice-based pagination over the upstream start + max_results params with opensearch:totalResults driving hasMore (falls back to entries-length-equals-limit during maintenance windows).
- lib/columns/plugins/arxiv/{plugin,server,client}.tsx: standard 3-file plugin. Zod schema with 12 categories enum + 2 sort modes + optional search. BookOpen icon, #B31B1B Cornell-red accent (arXiv's brand colour). Renderer shows red arXiv badge, primary-category mono tag, arxivId, revision badge for v2+, age, title, author byline (et-al. truncation), 280-char abstract preview, secondary categories as mono tags, PDF link.
- lib/columns/plugins/manifest.ts + registry.ts + server-registry.ts: three matching registry edits. The init-time parity check validates all three stay in sync — that's the only thing standing between an out-of-sync registry and a 404 at request time.
- README.md: column count 37 → 38, AI/ML cluster row 1 → 2, hero paragraph picks up arXiv, keyless-columns line adds arXiv.

How it works:
The integration calls export.arxiv.org/api/query with search_query=cat:{category} (optionally ANDed with ti:KEYWORD AND abs:KEYWORD per word), sortBy=submittedDate or lastUpdatedDate, sortOrder=descending, plus start + max_results for pagination. Response is Atom 1.0 — the parser walks every &lt;entry&gt;, extracts id (with vN version), title, summary (abstract), all author/name children, all category@term children, the alternate-rel link (abs page), the title="pdf" link, published, updated. Two quirks worth noting: (1) URLSearchParams escapes + to %2B, but arXiv requires + as the literal AND operator inside search_query — so the integration builds search_query manually and passes other params through normally; (2) revision detection is dual-redundant — a vN suffix where N>1 OR updated > published by more than 60 seconds, either sufficient.

What's next:
Pairs with huggingface (artifacts) and HN/Lobsters (link aggregation) for a complete AI content stack across the deck. Future arxiv-spotlight skill on aeon could mirror the huggingface-trending shape — daily curated picks rather than raw stream — once aeon operators ask for it.

PR: https://github.com/aaronjmars/minitor/pull/31
