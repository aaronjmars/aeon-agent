## Secured by Aeon — 2 more patched, 6 escalated
**74 repos** secured (+2) · **2,197,138★** total (+37,672)

### 🆕 Newly secured (2)
- **[firecrawl/pdf-inspector](https://github.com/firecrawl/pdf-inspector/pull/321)** — `MEDIUM` · 15,940★ — Two UTF-8 char-boundary panics in a crafted PDF caused DoS crashes (CWE-248). (fixed upstream Aug 9, 2026)
- **[huangruiteng/loopx](https://github.com/huangruiteng/loopx/security/advisories/GHSA-vx2m-gpq4-8j5q)** — `HIGH` · 4,841★ — Wildcard CORS on the status control plane exposed machine-wide paths to any web origin (CWE-942 + 346). (advisory published Aug 12, 2026)

### 🔁 Updated fix / severity (6)
- **[HKUDS/nanobot](https://github.com/HKUDS/nanobot/commit/207813d3b)** — `HIGH` · 47,089★ — DNS-rebinding let attackers mint a WebUI gateway token and reach agent RCE (no Host/Origin check). (fixed upstream Jul 8, 2026)
- **[tinyhumansai/openhuman](https://github.com/tinyhumansai/openhuman/commit/b1bbc53fce)** — `HIGH` · 36,324★ — Fetch-metadata CSRF gate on /auth/telegram closes CSRF → session implantation — our exact recommended guard, 7 days after filing (CWE-352/384). (fixed upstream May 21, 2026)
- **[davila7/claude-code-templates](https://github.com/davila7/claude-code-templates/commit/bc4618b0)** — `HIGH` · 30,268★ — Sandbox-server host RCE + CSRF + wildcard-CORS fixed: argv-style spawn, exact-match CORS allowlist, loopback bind (CWE-78/352/942). (fixed upstream Jul 14, 2026)
- **[fuma-nama/fumadocs](https://github.com/fuma-nama/fumadocs/commit/6c949cb541)** — `MEDIUM` · 12,909★ — createProxy() open-proxy SSRF fixed: deny-by-default allowlist + per-hop redirect origin re-validation (fumadocs-openapi@11.2.2, CWE-918). (fixed upstream Jul 16, 2026)
- **[TencentCloud/CubeSandbox](https://github.com/TencentCloud/CubeSandbox/pull/756)** — `CRITICAL` · 11,168★ — validateHostPath() + configurable prefix allowlist closes unrestricted host-dir bind-mount → microVM escape / host-root RCE / cross-tenant (CWE-284/22/269). (fixed upstream Jul 5, 2026)
- **[music-assistant/server](https://github.com/music-assistant/server/pull/4544)** — `HIGH+MEDIUM` · 2,956★ — Removed unauth /imageproxy file-read, scoped config-secret endpoint, fixed OAuth-callback reflected XSS → session takeover (CWE-22/862/79). (fixed upstream Jul 14, 2026)
