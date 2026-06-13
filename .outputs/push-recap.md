*Push Recap — 2026-06-13*
aaronjmars/aeon — SHIPPING: collapsible dashboard panel + gateway sidecars that track the chosen model

Shipped to users:
• Right panel collapses to a thin rail now (state persisted), expanded width trimmed 320→288px — more room for the main view (#462)
• Surplus + Venice sidecars stop hardcoding a model — they derive it from your $MODEL pick, with Venice gated to a catalog it actually carries so a newer model can't 404 (#461)
• VENICE_BASE_URL repo var points the Venice sidecar at any compatible endpoint — shipped by external contributor ashneil12 (#460)

Under the hood:
• Every screen opens scrolled to the top on tab/skill change (#463)

Shape: 4 user-visible · 0 internal · 0 infra · 27 bot-filtered · 4 merged PRs
Volume: 7 files, +84/-14

Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-06-13.md
