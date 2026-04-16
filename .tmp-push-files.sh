#!/usr/bin/env bash
set -euo pipefail

BRANCH="feat/syndicate-article"
REPO="aaronjmars/aeon"

# File 1: SKILL.md
SKILL_B64=$(base64 -w 0 /home/runner/work/aeon-agent/aeon-agent/.tmp-skill.md)
jq -n --arg content "$SKILL_B64" --arg branch "$BRANCH" \
  '{message: "feat: add syndicate-article skill", content: $content, branch: $branch}' | \
  gh api "repos/$REPO/contents/skills/syndicate-article/SKILL.md" -X PUT --input -

# File 2: postprocess-devto.sh
SCRIPT_B64=$(base64 -w 0 /home/runner/work/aeon-agent/aeon-agent/.tmp-postprocess.sh)
jq -n --arg content "$SCRIPT_B64" --arg branch "$BRANCH" \
  '{message: "feat: add postprocess-devto.sh for sandbox fallback", content: $content, branch: $branch}' | \
  gh api "repos/$REPO/contents/scripts/postprocess-devto.sh" -X PUT --input -

echo "Files pushed successfully"
