import json
up={x['discoveredFrom']:x for x in json.load(open('output/.up-eyebrowlock.json'))['artifacts']}
loc={x['discoveredFrom']:x for x in json.load(open('eyebrowlock.json'))['artifacts']}
print('=== UPSTREAM .claude/skills/aeon ===')
print(json.dumps(up['.claude/skills/aeon/SKILL.md'],indent=1))
print('=== LOCAL .claude/skills/aeon ===')
print(json.dumps(loc['.claude/skills/aeon/SKILL.md'],indent=1))
