import base64, json

with open('/home/runner/work/aeon-agent/aeon-agent/deep-research-skill.md', 'rb') as f:
    content = base64.b64encode(f.read()).decode()

payload = {
    "message": "feat: add Deep Research skill",
    "content": content,
    "branch": "feat/deep-research-skill"
}

with open('/home/runner/work/aeon-agent/aeon-agent/gh-payload.json', 'w') as f:
    json.dump(payload, f)

print("Payload written, content length:", len(content))
