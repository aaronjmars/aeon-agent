import json, shutil, os

# ---------- 1. eyebrowlock.json: swap 6 updated-skill entries verbatim from upstream HEAD ----------
loc = json.load(open('eyebrowlock.json'))
up  = json.load(open('output/.up-eyebrowlock.json'))
Uby = {a['discoveredFrom']: a for a in up['artifacts']}
swap = ['skills/aeon-update/SKILL.md','skills/changelog/SKILL.md','skills/competitor-monitor/SKILL.md',
        'skills/deploy-uni-hook/SKILL.md','skills/github-trending/SKILL.md','skills/vuln-scanner/SKILL.md']
n_swapped = 0
for i, a in enumerate(loc['artifacts']):
    df = a['discoveredFrom']
    if df in swap:
        assert df in Uby, f'missing upstream entry {df}'
        loc['artifacts'][i] = Uby[df]
        n_swapped += 1
assert n_swapped == len(swap), f'swapped {n_swapped} expected {len(swap)}'
out = json.dumps(loc, indent=2, ensure_ascii=True) + '\n'
open('eyebrowlock.json','w').write(out)
print('eyebrowlock: swapped', n_swapped, 'entries')

# ---------- 2. catalog/skills.json: update deploy-uni-hook (files,description) + vuln-scanner (files) ----------
sk = json.load(open('catalog/skills.json'))
usk = {s['slug']: s for s in json.load(open('output/.up-skills.json'))['skills']}
old_dep_desc = None
for s in sk['skills']:
    if s['slug'] == 'deploy-uni-hook':
        old_dep_desc = s['description']
        s['files'] = usk['deploy-uni-hook']['files']
        s['description'] = usk['deploy-uni-hook']['description']
    elif s['slug'] == 'vuln-scanner':
        s['files'] = usk['vuln-scanner']['files']
new_dep_desc = usk['deploy-uni-hook']['description']
open('catalog/skills.json','w').write(json.dumps(sk, separators=(',',':'), ensure_ascii=False))
print('skills.json: updated deploy-uni-hook + vuln-scanner; total stays', sk['total'])

# ---------- 3. catalog/packs.json: string-replace deploy-uni-hook description ----------
praw = open('catalog/packs.json').read()
assert old_dep_desc in praw, 'old deploy desc not found in packs.json'
praw2 = praw.replace(old_dep_desc, new_dep_desc)
open('catalog/packs.json','w').write(praw2)
print('packs.json: replaced deploy-uni-hook description; occurrences=', praw.count(old_dep_desc))

# ---------- 4. remove deferred new-skill dirs from working tree ----------
for d in ['skills/compute-resell','skills/miroshark-matchday','skills/submit-hook']:
    if os.path.isdir(d):
        shutil.rmtree(d); print('removed', d)
# also drop the two upstream new-skill svgs we CLEAN-ADDed (belong to deferred skills)
for f in ['docs/assets/skill-icons/compute-resell.svg','docs/assets/skill-icons/submit-hook.svg']:
    if os.path.exists(f):
        os.remove(f); print('removed', f)
print('DONE')
