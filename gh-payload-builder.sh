#!/bin/bash
SKILL_B64=$(base64 -w 0 /home/runner/work/aeon-agent/aeon-agent/deep-research-skill.md)
curl -s -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.v3+json" \
  "https://api.github.com/repos/aaronjmars/aeon/contents/skills/deep-research/SKILL.md" \
  -d "{\"message\":\"feat: add Deep Research skill\",\"content\":\"$SKILL_B64\",\"branch\":\"feat/deep-research-skill\"}" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('content',{}).get('path','error: '+str(d)))"
