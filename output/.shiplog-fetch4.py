import os, subprocess, json
from collections import Counter

env = os.environ.copy()
env['GH_TOKEN'] = env.get('GH_GLOBAL') or env.get('GITHUB_TOKEN', '')
SINCE = "2026-08-31T23:01:05Z"

def gh(args, timeout=90):
    r = subprocess.run(["gh"] + args, env=env, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

code, out, err = gh(["api", "repos/aeonfun/aeon/pulls", "-X", "GET", "-f", "state=closed", "-f", "sort=updated",
                      "-f", "direction=desc", "--paginate",
                      "--jq", f'.[] | select(.merged_at != null and .merged_at > "{SINCE}") | [.number, .user.login, .title] | @tsv'])
print("code", code, err[:200])
lines = [l for l in out.splitlines() if l.strip()]
print("count", len(lines))
authors = Counter()
for l in lines:
    parts = l.split("\t")
    authors[parts[1]] += 1
for a, c in authors.most_common():
    print(a, c)
