import re
t = open('articles/project-lens-2026-06-16.md').read()
main = t.split('\n---\n*Sources')[0]
print("Word count (excl sources):", len(main.split()))
banned = ['revolutionary','groundbreaking','game-chang','paradigm shift','disrupt',
          'unlocks','empowers','the future of','leverag','at scale','democratiz']
print("Banned hits:", [b for b in banned if re.search(b, t, re.I)] or "NONE")
lines = t.splitlines()
paras = [p for p in main.split('\n\n') if p.strip()]
first2 = ' '.join(paras[1:3])
print("Title:", lines[0])
print("'aeon' in title:", 'aeon' in lines[0].lower())
print("'aeon' in first 2 paras:", 'aeon' in first2.lower())
ext = re.findall(r'\]\((https?://[^)]+)\)', main)
print("Inline links in body:", len(ext))
print("Distinct domains in body:", sorted(set(re.findall(r'https?://([^/)]+)', main))))
