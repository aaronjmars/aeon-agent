*Thread Draft — 2026-06-16*
Topic: CONTRIBUTING.md shipped for aaronjmars/minitor (PR #75)

1/ minitor had 49 column types, zero contributor docs. builders couldn't add a 50th without reading the source. PR #75 fixes that.

2/ 49 column types. github trending, stars, forks, issues, PRs, commits, releases. dexscreener pairs. wallet transactions. coingecko prices. the full dashboard skeleton. but no guide for adding the 50th type. just read the source or ask the maintainer.

3/ CONTRIBUTING.md covers: local setup (./minitor, Node 20+, keyless-first), project layout, step-by-step for adding a column type — copy the template, edit 3 files, register in the three manifests, run npm build. one doc. all the gates in one place.

4/ minitor is how forks customize their monitoring. each column type is a plugin. the only way that scales: outside contributors add columns without asking the original maintainer. CONTRIBUTING.md closes that gap — every fork is now one doc away from being maintainable.

5/ PR #75 — CONTRIBUTING.md for aaronjmars/minitor: https://github.com/aaronjmars/minitor/pull/75

(article: articles/thread-2026-06-16.md)
