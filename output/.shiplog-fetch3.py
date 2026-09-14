import os, subprocess, json, re
from collections import defaultdict

env = os.environ.copy()
env['GH_TOKEN'] = env.get('GH_GLOBAL') or env.get('GITHUB_TOKEN', '')

SINCE = "2026-08-31T23:01:05Z"
SINCE_DATE = "2026-08-31"
TODAY = "2026-09-14"
OPERATOR = "aaronjmars"

FLAGSHIP = ["aeonfun/aeon", "aeonfun/univ4-hooks"]
WATCHED_EXTRA = ["aeonfun/minitor", "aeonfun/opendia", "aeonfun/soul.md"]

def gh(args, timeout=90):
    r = subprocess.run(["gh"] + args, env=env, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

# commits + merged PRs per flagship/watched repo
for repo in FLAGSHIP + WATCHED_EXTRA:
    code, out, err = gh(["api", f"repos/{repo}/commits", "-X", "GET", "-f", f"since={SINCE}", "--paginate",
                          "--jq", ".[] | .sha"])
    n_commits = len([l for l in out.splitlines() if l.strip()]) if code == 0 else None
    code2, out2, err2 = gh(["api", f"repos/{repo}/pulls", "-X", "GET", "-f", "state=closed", "-f", "sort=updated",
                             "-f", "direction=desc", "--paginate",
                             "--jq", f'.[] | select(.merged_at != null and .merged_at > "{SINCE}") | .number'])
    n_merged = len([l for l in out2.splitlines() if l.strip()]) if code2 == 0 else None
    err_a = err[:80] if code != 0 else ""
    err_b = err2[:80] if code2 != 0 else ""
    print(f"{repo}: commits={n_commits} (err={err_a}) merged_prs={n_merged} (err={err_b})")

# star counts now
print("--- stars ---")
for repo in FLAGSHIP + WATCHED_EXTRA + ["MiroShark/MiroShark"]:
    code, out, err = gh(["api", f"repos/{repo}", "--jq", ".stargazers_count"])
    print(f"{repo}: stars={out} err={err[:80]}")
