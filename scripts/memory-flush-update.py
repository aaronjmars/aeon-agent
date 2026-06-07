#!/usr/bin/env python3
"""memory-flush-update: Apply targeted updates to MEMORY.md as part of the memory-flush skill."""

with open('memory/MEMORY.md', 'r') as f:
    content = f.read()

# 1. Update "Last consolidated" date
content = content.replace('*Last consolidated: 2026-06-03*', '*Last consolidated: 2026-06-07*')
print('Updated last-consolidated date')

# 2. Update archive note
content = content.replace(
    '*(Rows before 2026-05-30 archived to `memory/topics/skills-history.md`)*',
    '*(Rows before 2026-06-04 archived to `memory/topics/skills-history.md`)*'
)
print('Updated archive note')

# 3. Remove Skills Built rows with dates 2026-05-30 to 2026-06-03
dates_to_archive = {'2026-05-30', '2026-05-31', '2026-06-01', '2026-06-02', '2026-06-03'}
lines = content.split('\n')
new_lines = []
in_skills_built = False
archived_count = 0
for line in lines:
    if '## Skills Built' in line:
        in_skills_built = True
    elif line.startswith('## ') and in_skills_built and '## Skills Built' not in line:
        in_skills_built = False

    if in_skills_built and line.startswith('|') and not line.startswith('| Skill') and not line.startswith('|---'):
        parts = line.split('|')
        if len(parts) >= 3:
            date = parts[2].strip()
            if date in dates_to_archive:
                archived_count += 1
                continue
    new_lines.append(line)

content = '\n'.join(new_lines)
print(f'Archived {archived_count} rows from Skills Built table')

# 4a. Add Jun-05 project-lens article after Jun-05 repo-article
marker_05 = '| 2026-06-05 | Vigil Was Submitted To Aeon As A Security Scanner. The Maintainer Caught A Shell-Injection In Vigil On Review Round Four. | repo-article |'
if marker_05 in content:
    replacement_05 = marker_05 + '\n| 2026-06-05 | On May 21 The MCP Team Removed Sessions From The Protocol. The Agents Already In Production Have Seven Weeks. | project-lens |'
    content = content.replace(marker_05, replacement_05)
    print('Added Jun-05 project-lens article')
else:
    print('WARNING: Jun-05 repo-article marker not found')

# 4b. Add Jun-06 project-lens article after Jun-06 repo-article
marker_06 = '| 2026-06-06 | Aeon Has 193 Skills. Fifteen Of Them Are The Machine. Yesterday The Framework Labelled Them. | repo-article |'
if marker_06 in content:
    insert_06 = marker_06 + "\n| 2026-06-06 | Most AI Agent Projects Stop When You Close The Laptop. The Ones That Don't Are A Different Market. | project-lens |"
    content = content.replace(marker_06, insert_06)
    print('Added Jun-06 project-lens article')
else:
    print('WARNING: Jun-06 repo-article marker not found')

# 5. Update show-hn-draft star count in Next Priorities
old_hn = '- **URGENT** Enable show-hn-draft in aeon.yml \xe2\x80\x94 PR #151 (May 1); at 476⭐ (24 from 500); escalation sent Jun 3, next in 7d'
new_hn = '- **URGENT** Enable show-hn-draft in aeon.yml \xe2\x80\x94 PR #151 (May 1); at 490⭐ (10 from 500, projected Jun 11); next escalation Jun 10'
if old_hn in content:
    content = content.replace(old_hn, new_hn)
    print('Updated show-hn-draft star count')
else:
    # Try with ASCII em dash
    old_hn2 = 'Enable show-hn-draft in aeon.yml'
    if old_hn2 in content:
        print('WARNING: show-hn-draft line found but exact match failed - check encoding')
    else:
        print('WARNING: show-hn-draft priority line not found at all')

# 6. Update fork-cohort fork count
old_fork = 'Enable fork-cohort in aeon.yml \xe2\x80\x94 PR #152 (May 2); now 157+ forks \xe2\x80\x94 growing social proof'
new_fork = 'Enable fork-cohort in aeon.yml \xe2\x80\x94 PR #152 (May 2); now 166+ forks \xe2\x80\x94 growing social proof'
if old_fork in content:
    content = content.replace(old_fork, new_fork)
    print('Updated fork-cohort fork count')
else:
    old_fork2 = 'Enable fork-cohort in aeon.yml'
    if old_fork2 in content:
        print('WARNING: fork-cohort line found but exact match failed - check encoding')
    else:
        print('WARNING: fork-cohort priority line not found at all')

with open('memory/MEMORY.md', 'w') as f:
    f.write(content)

print('MEMORY.md written successfully')
