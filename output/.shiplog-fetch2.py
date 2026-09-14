import os, subprocess, json, sys
from collections import defaultdict

env = os.environ.copy()
env['GH_TOKEN'] = env.get('GH_GLOBAL') or env.get('GITHUB_TOKEN', '')

SINCE_DATE = "2026-08-31"
OPERATOR = "aaronjmars"

def gh(args, timeout=120):
    cmd = ["gh"] + args
    r = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

code, out, err = gh([
    "search", "prs", "--author", OPERATOR, "--created", f">={SINCE_DATE}",
    "--json", "number,title,repository,state,createdAt,url", "--limit", "1000"
])
print("code", code, "err", err[:300])
prs = json.loads(out)
print("TOTAL_PRS", len(prs))

by_repo = defaultdict(list)
for p in prs:
    by_repo[p['repository']['nameWithOwner']].append(p)

for repo, items in sorted(by_repo.items(), key=lambda x: -len(x[1])):
    merged = sum(1 for i in items if i['state'] == 'merged')
    openc = sum(1 for i in items if i['state'] == 'open')
    closed = sum(1 for i in items if i['state'] == 'closed')
    print(f"{repo}: total={len(items)} merged={merged} open={openc} closed={closed}")

with open("/home/runner/work/aeon-agent/aeon-agent/output/.shiplog-prs.json", "w") as f:
    json.dump(prs, f)
