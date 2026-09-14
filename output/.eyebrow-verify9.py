import json,hashlib,subprocess,base64
up={x['discoveredFrom']:x for x in json.load(open('output/.up-eyebrowlock.json'))['artifacts']}
def fetch(path):
    r=subprocess.run(['gh','api',f'repos/aeonfun/aeon/contents/{path}?ref=95142d19705ca379815e7fc9493a497ee0504e8d','--jq','.content'],capture_output=True,text=True)
    return base64.b64decode(r.stdout.strip())
skills=['aeon-update','changelog','competitor-monitor','deploy-uni-hook','github-trending','vuln-scanner','compute-resell','miroshark-matchday','submit-hook']
allok=True
for s in skills:
    df=f'skills/{s}/SKILL.md'
    a=up[df]
    files=[f['path'] for f in a['files']]
    b=fetch(df)
    plain=hashlib.sha256(b).hexdigest()
    smd=[f for f in a['files'] if f['path']=='SKILL.md'][0]['hash']
    ok = (files==['SKILL.md']) and (plain==smd)
    allok = allok and ok
    print(s, 'files=',files, 'hashmatch=', plain==smd, 'caps=', a.get('capabilities'))
print('ALL OK:', allok)
