*Feature Built — 2026-05-08 — aaronjmars/aeon*

Hugging Face Trending skill
aeon just got a daily curated digest of the AI artifact layer — what's trending on Hugging Face today across models, datasets, and spaces. The skill mirrors the existing `github-trending` contract: instead of dumping the top 10 unfiltered, it filters noise, requires a one-line "why notable" per pick, tags momentum, clusters into five buckets, and surfaces a single Top pick — but it does this for HF artifacts rather than GitHub repos.

Why this matters:
aeon already has paper-pick + paper-digest (research/theory layer) and github-trending (repo/code layer) but had no skill for the AI artifact layer that lives between them. The Hub is where models land first (DeepSeek-R1, Llama, Qwen releases all surface there before mainstream coverage), datasets get attention before papers cite them, and Spaces are often the first runnable form of a fresh technique. Without this, aeon's daily AI-coverage was missing the floor of the stack that operators actually deploy from. Now papers (theory) → repos (code, github-trending) → HF Hub (artifacts, this skill) gives a complete daily picture of where the AI ecosystem's attention moved across all three layers.

What was built:
- skills/huggingface-trending/SKILL.md: Full 9-step skill spec — six noise filters (test/debug ids, low-signal gated repos, trivial fine-tunes, 3-day re-features, quantization-only forks under 500 likes, broken or scaffold spaces), required ≤18-word "why notable" line per survivor, momentum tags (DEBUT 7d / ACCELERATING / RETURNING 90d+ / HOLDOVER), five-bucket cluster cap (LLMs, Multimodal, Agents, Datasets, Spaces), single Top pick discipline, four-status exit taxonomy (HF_TRENDING_OK / QUIET / ERROR / BAD_VAR).
- aeon.yml: Registered enabled:false, schedule:"30 9 * * *", model:claude-sonnet-4-6 immediately after github-releases — the morning AI/dev intelligence block now closes with HF artifacts at 09:30 right after github-trending fires at 09:00.
- skills.json + generate-skills-json: Bumped total 111 → 112; mapped huggingface-trending to research category in the bash case so future regenerations stay in lockstep.
- README.md: Added to the Research & Content cluster row, count 17 → 18.

How it works:
Pure prompt / Markdown — no helper scripts, no new env vars, no new state files. The model walks the 9 steps, calling curl (or WebFetch on sandbox failure) against three keyless endpoints (`/api/{models,datasets,spaces}?sort=trendingScore&direction=-1`). The "why notable" gate is the load-bearing line of the prompt — it forces justification rather than description paraphrase. When the line can't be written concretely, the pick gets dropped. The filter is the feature, same discipline that makes github-trending land cleanly. Sandbox-safe via the documented curl-then-WebFetch fallback per CLAUDE.md guidance; single-source failures don't fail the run, only all-three exits HF_TRENDING_ERROR.

What's next:
Pairs with same-day minitor PR #30 — the running aeon agent gets the curated daily digest, a minitor dashboard gets the live feed. Once enabled in aeon.yml the skill ships its first article tomorrow morning. Natural follow-up after that is a `huggingface-papers` skill that taps `/api/daily_papers` for the paper-side equivalent.

PR: https://github.com/aaronjmars/aeon/pull/162
