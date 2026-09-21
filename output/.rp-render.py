import re

def clean(s):
    if s is None:
        return None
    s = s.replace('\r\n', ' ').replace('\r', ' ').replace('\n', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    return s if s else None

def fmt_followers(n):
    if n is None or n < 10:
        return None
    if n < 1000:
        return f"{n} followers"
    return f"{n/1000:.1f}k followers"

def truncate_bio(b, limit=140):
    b = clean(b)
    if b is None:
        return None
    if len(b) <= limit:
        return b
    cut = b[:limit].rsplit(' ', 1)[0]
    return cut + "…"

def card(p):
    login = p['login']
    name = clean(p.get('name'))
    location = clean(p.get('location'))
    company = clean(p.get('company'))
    blog = p.get('blog') or None
    if blog and blog.strip() == '':
        blog = None
    html_url = p.get('html_url')
    if blog and html_url and blog.rstrip('/') == html_url.rstrip('/'):
        blog = None
    twitter = p.get('twitter')
    followers = p.get('followers', 0)
    repos = p.get('public_repos')
    bio = truncate_bio(p.get('bio'))
    notable = (followers or 0) >= 100 or (repos or 0) >= 20

    parts = [f"github.com/{login}"]
    if name:
        parts[0] += f" — {name}"
    segs = []
    if location:
        segs.append(f"📍 {location}")
    if company:
        segs.append(f"🏢 {company}")
    if repos is not None:
        segs.append(f"{repos} repos")
    if blog:
        segs.append(f"🌐 {blog}")
    if twitter:
        segs.append(f"🐦 @{twitter}")
    f = fmt_followers(followers)
    if f:
        segs.append(f)
    line = parts[0]
    if segs:
        line += " · " + " · ".join(segs)
    out = line
    if bio:
        out += f'\n  "{bio}"'
    return out, notable

import json, sys
data = json.loads(sys.stdin.read())
for p in data:
    c, notable = card(p)
    print(f"[{'NOTABLE' if notable else 'plain'}] {p['login']}")
    print(c)
    print("---")
