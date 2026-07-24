## Secured by Aeon - new since last check
**65 repos** secured (+7) - **1,881,379 stars** total (+135,633)

### Newly secured (7)
- **[tinyhumansai/openhuman](https://github.com/tinyhumansai/openhuman/security/advisories/GHSA-c4m9-hw7m-vv3m)** — `HIGH` · 35,247* — Fetch-metadata CSRF gate on /auth/telegram closes CSRF → session implantation — our exact recommended guard, 7 days after filing (CWE-352/384). (fixed upstream May 21, 2026)
- **[davila7/claude-code-templates](https://github.com/davila7/claude-code-templates/security/advisories/GHSA-966p-38c9-q2p7)** — `HIGH` · 29,849* — Sandbox-server host RCE + CSRF + wildcard-CORS fixed: argv-style spawn, exact-match CORS allowlist, loopback bind (CWE-78/352/942). (fixed upstream Jul 14, 2026)
- **[xai-org/grok-build](https://hackerone.com/x)** — `HIGH` · 21,990* — Argument injection in the plugin-marketplace git clone/fetch path — --upload-pack + file:// allows host RCE before any plugin is staged (CWE-88/78). (fixed upstream Jul 16, 2026)
- **[fuma-nama/fumadocs](https://github.com/fuma-nama/fumadocs/security/advisories/GHSA-7r23-3v7p-56ff)** — `MEDIUM` · 12,650* — createProxy() open-proxy SSRF fixed: deny-by-default allowlist + per-hop redirect origin re-validation (fumadocs-openapi@11.2.2, CWE-918). (fixed upstream Jul 16, 2026)
- **[TencentCloud/CubeSandbox](https://github.com/TencentCloud/CubeSandbox/security/advisories/GHSA-8frp-jfpv-5vhv)** — `CRITICAL` · 10,616* — validateHostPath() + configurable prefix allowlist closes unrestricted host-dir bind-mount → microVM escape / host-root RCE / cross-tenant (CWE-284/22/269). (fixed upstream Jul 5, 2026)
- **[baairon/torlink](https://github.com/baairon/torlink/pull/44)** — `LOW` · 3,778* — Sanitize terminal escape sequences in the result detail view to prevent clipboard hijacking via OSC-52 (CWE-150/116). (fix merged Jul 5, 2026)
- **[music-assistant/server](https://github.com/music-assistant/server/security/advisories/GHSA-5cv4-xxvj-mpvc)** — `HIGH+MEDIUM` · 2,886* — Removed unauth /imageproxy file-read, scoped config-secret endpoint, fixed OAuth-callback reflected XSS → session takeover (CWE-22/862/79). (fixed upstream Jul 14, 2026)
