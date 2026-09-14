import json
loc=json.load(open('eyebrowlock.json'))['artifacts']
up=json.load(open('output/.up-eyebrowlock.json'))['artifacts']
def df(a): return sorted(x['discoveredFrom'] for x in a)
nonskill_local=[d for d in df(loc) if not d.startswith('skills/')]
print('LOCAL non-skills/ artifacts:', nonskill_local)
nonskill_up=[d for d in df(up) if not d.startswith('skills/')]
print('UP non-skills/ artifacts:', nonskill_up)
