import json,hashlib,subprocess,base64
up=json.load(open('output/.up-eyebrowlock.json'))['artifacts']
U={x['discoveredFrom']:x for x in up}
def fetch(path):
    r=subprocess.run(['gh','api',f'repos/aeonfun/aeon/contents/{path}?ref=95142d19705ca379815e7fc9493a497ee0504e8d','--jq','.content'],capture_output=True,text=True)
    return base64.b64decode(r.stdout.strip())
targets=['skills/operator-scorecard/SKILL.md','.claude/skills/aeon/SKILL.md','skills/vuln-scanner/SKILL.md','skills/compute-resell/SKILL.md']
for t in targets:
    b=fetch(t)
    s=hashlib.sha256(b).hexdigest()
    lockhash=U[t]['files'][0]['hash']
    print(t, 'match' if s==lockhash else 'MISMATCH', s[:16], lockhash[:16])
