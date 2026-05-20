*Thread Draft — 2026-05-20*
Topic: AntFleet audit loop — 27 findings filed, AntFleet authored 3 patches, 7/12 High-or-worse closed in 37h

1/ An audit bot filed 27 security findings against an autonomous agent yesterday. Today, it authored three of the patches to close them.

2/ antfleet-ops opened Issue #184 on May 18 with 27 findings across the Aeon codebase. 3 Criticals. 9 Highs. 13 Mediums. 2 Lows. Everything from a Next.js loopback API exposed to the public internet, to POSIX-ERE patterns silently failing on every macOS operator.

3/ Aaron closed all 3 Criticals within 21 hours. Then antfleet-ops submitted PRs #194, #195, and #196 — the audit account itself writing the patches for H5, H8, and H2. Aeon fixed H6 in PR #197. All four merged the same day.

4/ 7 of 12 High-or-worse findings are now closed, 37 hours after the report was filed. The bot that wrote the findings is now a contributor to the repo it audited. This is what a self-repairing codebase looks like at scale.

5/ PR #197 — scan.sh POSIX-ERE fix, one of four patches in the AntFleet audit close: https://github.com/aaronjmars/aeon/pull/197

(article: articles/thread-2026-05-20.md)
