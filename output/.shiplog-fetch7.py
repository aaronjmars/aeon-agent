import os, subprocess, json

env = os.environ.copy()
env['GH_TOKEN'] = env.get('GH_GLOBAL') or env.get('GITHUB_TOKEN', '')
SINCE = "2026-08-31T23:01:05Z"

def gh(args, timeout=90):
    r = subprocess.run(["gh"] + args, env=env, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

repos = ["aaronjmars/aeon-website", "aaronjmars/aeon-vuln", "aaronjmars/aeon-onchain",
         "aaronjmars/aeon-bd", "aaronjmars/aeon-data", "aaronjmars/miniaeon", "aaronjmars/aeon-agent"]
for repo in repos:
    code, out, err = gh(["api", f"repos/{repo}/pulls", "-X", "GET", "-f", "state=closed", "-f", "sort=updated",
                          "-f", "direction=desc", "--paginate",
                          "--jq", f'.[] | select(.merged_at != null and .merged_at > "{SINCE}") | .number'])
    n = len([l for l in out.splitlines() if l.strip()]) if code == 0 else None
    print(f"{repo}: merged={n} err={err[:100] if code != 0 else ''}")
