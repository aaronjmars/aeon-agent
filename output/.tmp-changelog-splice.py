import io
import re
import sys

PATH = "/tmp/aeon-website-changelog/app/changelog-data.ts"
BLOCK = "/home/runner/work/aeon-agent/aeon-agent/output/.tmp-changelog-block.txt"

NEW_PRS = [954, 980, 981, 982, 983, 984, 985, 986, 987, 988,
           989, 990, 991, 992, 993, 994, 995, 996, 997, 998]

src = io.open(PATH, encoding="utf-8").read()
block = io.open(BLOCK, encoding="utf-8").read()

anchor = '  // newest first - PREPEND new entries here, never rewrite existing ones\n'
if src.count(anchor) != 1:
    sys.exit("ABORT: anchor not found exactly once")

for n in NEW_PRS:
    if re.search(r'number: %d,' % n, src):
        sys.exit("ABORT: PR #%d already published" % n)

if 'date: "2026-08-31"' in src:
    sys.exit("ABORT: an entry dated 2026-08-31 already exists")

out = src.replace(anchor, anchor + block, 1)
io.open(PATH, "w", encoding="utf-8").write(out)
print("inserted %d chars after anchor; file now %d chars" % (len(block), len(out)))
