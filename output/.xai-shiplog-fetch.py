#!/usr/bin/env python3
"""shiplog: fetch X sources via X.AI responses API (x_search tool). One file per source."""
import json, os, sys, urllib.request, urllib.error

KEY = os.environ.get("XAI_API_KEY", "")
WINDOW_SD, WINDOW_TD = "2026-08-24", "2026-08-31"
OUTDIR = os.path.dirname(os.path.abspath(__file__))

SOURCES = {
    "operator": {
        "payload": {
            "model": "grok-4.6",
            "input": [{"role": "user", "content": (
                "Search X for posts by @aaronjmars between " + WINDOW_SD + " and " + WINDOW_TD + ". "
                "Return each post with full text, date, type (original|reply|RT - an RT text starts with \"RT @\"), "
                "exact engagement counts (likes, retweets, replies; 0 if unknown), and the direct link "
                "https://x.com/aaronjmars/status/ID. Return chronological.")}],
            "tools": [{"type": "x_search"}],
        },
    },
    "projects": {
        "payload": {
            "model": "grok-4.6",
            "input": [{"role": "user", "content": (
                "Search X for posts between " + WINDOW_SD + " and " + WINDOW_TD + " from these accounts: "
                "@aeonframework @miroshark_. Focus on launches, announcements, and any brag about a security "
                "fix merged into another project. For each: @handle, full text, date, exact engagement counts "
                "(likes, retweets, replies; 0 if unknown), and the direct link https://x.com/handle/status/ID. "
                "Skip retweets of others.")}],
            "tools": [{"type": "x_search"}],
        },
    },
    "ecosystem": {
        "payload": {
            "model": "grok-4.6",
            "input": [{"role": "user", "content": (
                "Search X between " + WINDOW_SD + " and " + WINDOW_TD + " for posts from these recap/scout "
                "accounts: @buildonbase @Base_Insights @BaseHubHB @PremierBase that mention any of these "
                "products: Aeon, Miroshark. Return each mention with @handle, follower_count, full text, date, "
                "and the direct link https://x.com/handle/status/ID - recaps, rankings, partner shares.")}],
            "tools": [{"type": "x_search"}],
        },
    },
}

def fetch(name, payload):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.x.ai/v1/responses",
        data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + KEY},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=150) as resp:
            data = resp.read()
            code = resp.status
    except urllib.error.HTTPError as e:
        data = e.read() if hasattr(e, "read") else b""
        code = e.code
    except Exception as e:
        return name, "error:" + type(e).__name__, 0, ""
    out = os.path.join(OUTDIR, ".xai-shiplog-" + name + ".json")
    with open(out, "wb") as f:
        f.write(data)
    return name, code, len(data), out

if not KEY:
    print("key-unset")
    sys.exit(0)

if len(sys.argv) > 1:
    SOURCES = {k: v for k, v in SOURCES.items() if k in sys.argv[1:]}

results = []
for name, cfg in SOURCES.items():
    n, code, nbytes, path = fetch(name, cfg["payload"])
    results.append((n, code, nbytes, path))
    print("xai http=%s bytes=%d src=%s" % (code, nbytes, name), flush=True)
