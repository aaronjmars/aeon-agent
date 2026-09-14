import json, glob, os, subprocess

# 1. JSON parse checks
for f in ['catalog/skills.json','catalog/packs.json','eyebrowlock.json',
          'catalog/skill-icons.json','apps/webhook/package.json','apps/webhook/package-lock.json']:
    json.load(open(f)); print('JSON ok:', f)

# 2. coverage gate replica: every skills/*/SKILL.md has an eyebrowlock discoveredFrom entry
lock=json.load(open('eyebrowlock.json'))
dfs={a['discoveredFrom'] for a in lock['artifacts']}
skill_dirs=sorted(glob.glob('skills/*/SKILL.md'))
missing=[f for f in skill_dirs if f not in dfs]
print('skill dirs on disk:', len(skill_dirs), '| coverage missing:', missing)

# 3. skills.json total vs disk
sk=json.load(open('catalog/skills.json'))
print('skills.json total:', sk['total'], '| catalog entries:', len(sk['skills']), '| disk skill dirs:', len(skill_dirs))

# 4. verify the 6 swapped eyebrow entries match upstream verbatim
up={a['discoveredFrom']:a for a in json.load(open('output/.up-eyebrowlock.json'))['artifacts']}
locby={a['discoveredFrom']:a for a in lock['artifacts']}
swap=['skills/aeon-update/SKILL.md','skills/changelog/SKILL.md','skills/competitor-monitor/SKILL.md',
      'skills/deploy-uni-hook/SKILL.md','skills/github-trending/SKILL.md','skills/vuln-scanner/SKILL.md']
for s in swap:
    print('swap ok', s, locby[s]==up[s])

# 5. deferred skills absent from eyebrowlock & catalog
for s in ['compute-resell','miroshark-matchday','submit-hook']:
    inlock=f'skills/{s}/SKILL.md' in dfs
    incat=any(x['slug']==s for x in sk['skills'])
    ondisk=os.path.isdir(f'skills/{s}')
    print(f'deferred {s}: lock={inlock} catalog={incat} disk={ondisk}')

# 6. catalog updates present
for x in sk['skills']:
    if x['slug'] in ('deploy-uni-hook','vuln-scanner'):
        print(x['slug'],'files=',x['files'])
