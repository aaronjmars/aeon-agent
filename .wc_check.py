t = open('articles/project-lens-2026-06-12.md').read()
body = t.split('\n---\n*Sources:*')[0]
lines = [l for l in body.splitlines() if not l.startswith('# ')]
body = '\n'.join(lines)
print('BODY WORDS:', len(body.split()))
banned = ['revolutionary', 'groundbreaking', 'game-changing', 'paradigm shift',
          'disrupting', 'unlocks', 'empowers', 'the future of', 'leverag',
          'at scale', 'democratiz']
low = t.lower()
hits = [b for b in banned if b in low]
print('BANNED HITS:', hits or 'NONE')
