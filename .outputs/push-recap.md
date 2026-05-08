*Push Recap — 2026-05-08*
3 substantive commits across aeon (2) and minitor (1) — aeon-agent saw only routine cron noise.

*Hugging Face surface, two repos same morning:* aeon PR #162 ships `huggingface-trending` skill (curated trending HF models/datasets/spaces, mirrors github-trending's contract — six noise filters, "why notable" gate, momentum tags, 5-bucket clustering, single Top pick). Minitor PR #30 ships matching live column — 37th type, first consumer of the dormant `ai` ColumnCategory. Together they complete aeon's AI ecosystem triple alongside paper-pick (theory) and github-trending (code).

*Stalled fork-PR finally landed:* aeon PR #156 (tomscaria, open 102h, the single stalled-PR heartbeat had been flagging) wires `reply-maker` into `prefetch-xai.sh` — sixth shared-helper consumer. Closes the sandbox-blocked-curl path; reply-maker can now actually return candidates from CI.

Key changes:
- `skills/huggingface-trending/SKILL.md` (+179): keyless `/api/{models,datasets,spaces}?sort=trendingScore`, schema-drift safe across 3 resource types, 4-status exit taxonomy
- `lib/integrations/huggingface.ts` + 3-file plugin (+512): HF yellow `#FFD21F` brand chip, conditional downloads field for spaces, per-resource permalink builder
- `scripts/prefetch-xai.sh` reply-maker case (+21): numeric var → list ID, @-prefix → handle w/ `allowed_x_handles`, else → topic

Stats: 15 files changed, +751/-8 lines (excluding 32 cron auto-commits in aeon-agent)
Full recap: https://github.com/aaronjmars/aeon-agent/blob/main/articles/push-recap-2026-05-08.md
