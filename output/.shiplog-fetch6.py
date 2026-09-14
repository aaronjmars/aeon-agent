import os, subprocess, json

env = os.environ.copy()
env['GH_TOKEN'] = env.get('GH_GLOBAL') or env.get('GITHUB_TOKEN', '')
SINCE = "2026-08-31T23:01:05Z"

def gh(args, timeout=90):
    r = subprocess.run(["gh"] + args, env=env, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

for repo in ["aeonfun/univ4-hooks", "aeonfun/minitor"]:
    print("===", repo)
    code, out, err = gh(["api", f"repos/{repo}/pulls", "-X", "GET", "-f", "state=closed", "-f", "sort=updated",
                          "-f", "direction=desc", "--paginate",
                          "--jq", f'.[] | select(.merged_at != null and .merged_at > "{SINCE}") | [.number, .user.login, .title] | @tsv'])
    print(out)
    print(err[:200])
