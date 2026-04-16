#!/usr/bin/env python3
"""Push files to GitHub branch via Contents API."""
import base64
import json
import subprocess
import sys

BRANCH = "feat/syndicate-article"
REPO = "aaronjmars/aeon"

def read_and_encode(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

def push_file(repo_path, local_path, message):
    content = read_and_encode(local_path)
    payload = json.dumps({
        "message": message,
        "content": content,
        "branch": BRANCH,
    })
    result = subprocess.run(
        ["gh", "api", f"repos/{REPO}/contents/{repo_path}", "-X", "PUT", "--input", "-"],
        input=payload,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"ERROR pushing {repo_path}: {result.stderr}", file=sys.stderr)
        return False
    data = json.loads(result.stdout)
    print(f"OK: {repo_path} -> {data['commit']['sha'][:7]}")
    return True

base = "/home/runner/work/aeon-agent/aeon-agent"

ok = True
ok = push_file(
    "skills/syndicate-article/SKILL.md",
    f"{base}/.tmp-skill.md",
    "feat: add syndicate-article skill"
) and ok

ok = push_file(
    "scripts/postprocess-devto.sh",
    f"{base}/.tmp-postprocess.sh",
    "feat: add postprocess-devto.sh for sandbox fallback"
) and ok

sys.exit(0 if ok else 1)
