import re, json, sys, os, datetime
TODAY = "2026-08-12"
var = (sys.argv[1] if len(sys.argv) > 1 else "").strip().lower()
dry = var == "dry-run"; full = var == "full"
STATE = "memory/state/secured-repos.json"
html = open('.sw-tmp/security.html', encoding='utf-8', errors='replace').read()

rows = {}
for c in re.split(r'(?=<a class="page_row)', html):
    if not c.startswith('<a class="page_row'):
        continue
    al = re.search(r'aria-label="(.+?) - (.+?) severity, ([\d,]+) stars', c)
    if not al:
        continue
    href = (re.search(r'href="([^"]+)"', c) or [None, None])[1]
    note = (re.search(r'title="([^"]*)"', c) or [None, ''])[1]
    repo, sev, stars = al.group(1).strip(), al.group(2).strip(), int(al.group(3).replace(',', ''))
    rows[repo] = {"severity": sev, "stars": stars, "fix_url": href, "note": note}

if len(rows) == 0:
    print("PARSE_EMPTY")
    sys.exit(0)

total_stars = sum(r["stars"] for r in rows.values())
cur = {"updated_at": TODAY, "total_repos": len(rows),
       "total_stars": total_stars, "repos": rows}

prev = None
if os.path.exists(STATE):
    try:
        prev = json.load(open(STATE))
    except Exception:
        prev = None

if prev is None and not full:
    if not dry:
        json.dump(cur, open(STATE, "w"), indent=2)
    print("BASELINE")
    print(f"repos={len(rows)} stars={total_stars}")
    sys.exit(0)

prev_repos = (prev or {}).get("repos", {})
new  = [k for k in rows if k not in prev_repos]
changed = [k for k in rows if k in prev_repos and
           (rows[k]["fix_url"] != prev_repos[k].get("fix_url") or
            rows[k]["severity"] != prev_repos[k].get("severity"))]
gone = [k for k in prev_repos if k not in rows]

d_repos = len(rows) - (prev.get("total_repos", len(rows)) if prev else len(rows))
d_stars = total_stars - (prev.get("total_stars", total_stars) if prev else total_stars)

def sd(n): return f"+{n:,}" if n > 0 else (f"{n:,}" if n < 0 else "±0")
def row_line(k):
    r = rows[k]
    return f"- **[{k}]({r['fix_url']})** — `{r['severity']}` · {r['stars']:,}★ — {r['note']}"

report_repos = list(rows) if full else (new + changed)
has_signal = bool(report_repos) or (full and rows)

if not dry:
    json.dump(cur, open(STATE, "w"), indent=2)

if not has_signal:
    print("NO_CHANGE")
    print(f"repos={len(rows)} ({sd(d_repos)}) stars={total_stars} ({sd(d_stars)})")
    sys.exit(0)

L = []
title = "Secured by Aeon — full board" if full else "Secured by Aeon — new since last check"
L.append(f"## {title}")
L.append(f"**{len(rows)} repos** secured ({sd(d_repos)}) · **{total_stars:,}★** total ({sd(d_stars)})")
L.append("")
if full:
    for k in sorted(rows, key=lambda k: -rows[k]["stars"]):
        L.append(row_line(k))
else:
    if new:
        L.append(f"### \U0001f195 Newly secured ({len(new)})")
        for k in sorted(new, key=lambda k: -rows[k]["stars"]):
            L.append(row_line(k))
        L.append("")
    if changed:
        L.append(f"### \U0001f501 Updated fix / severity ({len(changed)})")
        for k in sorted(changed, key=lambda k: -rows[k]["stars"]):
            p = prev_repos[k]
            extra = ""
            if rows[k]["severity"] != p.get("severity"):
                extra = f" _(severity {p.get('severity')} → {rows[k]['severity']})_"
            L.append(row_line(k) + extra)
        L.append("")
if gone:
    L.append(f"_Dropped from board: {', '.join(sorted(gone))}_")
open('.sw-tmp/report.md', 'w').write("\n".join(L).rstrip() + "\n")
print("NOTIFY")
print(f"new={len(new)} changed={len(changed)} gone={len(gone)} repos={len(rows)}")
