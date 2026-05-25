#!/usr/bin/env bash
# Process all forks and extract enabled skills from aeon.yml
set -uo pipefail

FORKS=(
"AFHUNTLY/aeon" "UIZorrot/aeon" "masteramatajj-source/aeon" "yehorcallmedai-maker/aeon"
"sooyooshq/aeon" "liquidpadbot/aeon" "shiyankuan-crypto/aeon" "lawbworld-tech/aeon"
"luazhizhan/aeon" "imthefounder/aeon" "sherwoodagent/aeon" "gitlawbounty/aeon"
"bweick/aeon" "0xShak/aeon" "taekwonv89/aeon" "svenakira/aeon"
"happycamper-stix/aeon" "ryjin111/aeon" "cersei420/aeon" "wx888/aeon"
"jonathanjoseph20/aeon" "fleet-watcher/aeon" "danbuildss/aeon" "smolboon/aeon"
"0xMal0u/aeon" "youpsla/aeon" "PyroFire-Labs/larry" "LiamVisionary/aeon"
"bitcoiner-lab/aeon" "antfleet-ops/aeon" "forge-executive/forge-executive"
"DABAGElover/aeon" "levi-oss-code/aeon" "damo-nu11/aeon-minebean" "We3In/vvvkerrnel"
"We3In/vvvkernel-skills-up" "We3In/aeon" "abhirajprasad/aeon" "coinhome190-spec/aeon"
"VibeSan7/aeon" "anomit/aeon" "enzoonchain/aeon" "sinan33644061-lab/aeon"
"wuyu663/aeon" "DevZenPro/aeon" "AntFleet/aeon-bench" "foreverxdord/aeon"
"oxkaiba/aeon" "baseddevoloper/vvvkernel-skills" "Azh1er/aeon" "takanafur/aeon"
"KevinFreistroffer/aeon" "0xMortimer/aeon" "lioapple/aeon" "ashneil12/aeon"
"jiamicuisi-a11y/aeon" "madebyshun/blueagent-aeon" "meichuanyi/aeon" "johnny5OO/aeon"
"speend/aeon" "amandi99/aeon" "Daniel-DDV/aeon" "usiclabs/aeon" "Danypsy/aeon"
"Da6hkin/aeon" "theipgirl/aeon" "traewang/aeon-contrib" "itr010038/aeon"
"varun86/aeon" "fsgaleti-create/aeon" "Boodszw/Boodszw_Bread" "jimimased/aeon"
"Aldine/aeon" "ether-btc/aeon" "FreyjasWrath/aeon" "infrareactive/aeon"
"CNZSMJ/aeon" "eugene-gourevitch/aeon" "adarshhalan/aeon" "tomscaria/aeon"
"yugo-engineer/aeon" "pezetel/aeon" "gcampton/aeon" "AmithKumar1/aeon"
)

OUTFILE="/tmp/forks-results.json"
echo "{}" > "$OUTFILE"

for fork in "${FORKS[@]}"; do
  echo "=== Processing: $fork ==="
  content=$(gh api "repos/${fork}/contents/aeon.yml" --jq '.content' 2>/dev/null || echo "")

  if [ -z "$content" ] || [ "$content" = "null" ]; then
    echo "  -> NO_YAML"
    # append to results
    python3 -c "
import json, sys
data = json.load(open('$OUTFILE'))
data['$fork'] = 'NO_YAML'
json.dump(data, open('$OUTFILE', 'w'))
"
    continue
  fi

  decoded=$(echo "$content" | base64 -d 2>/dev/null || echo "")
  if [ -z "$decoded" ]; then
    echo "  -> DECODE_ERROR"
    python3 -c "
import json, sys
data = json.load(open('$OUTFILE'))
data['$fork'] = 'DECODE_ERROR'
json.dump(data, open('$OUTFILE', 'w'))
"
    continue
  fi

  skills=$(echo "$decoded" | python3 -c "
import sys, re
content = sys.stdin.read()
skills_match = re.search(r'^skills:\s*\n((?:[ \t]+.*\n?)*)', content, re.MULTILINE)
if not skills_match:
    print('NO_SKILLS_SECTION')
    sys.exit(0)
skills_block = skills_match.group(1)
inline = re.findall(r'^[ \t]+([a-z][a-z0-9_-]+):\s*\{[^}]*enabled:\s*true', skills_block, re.MULTILINE)
multi = re.findall(r'^[ \t]+([a-z][a-z0-9_-]+):\s*\n(?:[ \t]+.*\n)*?[ \t]+enabled:\s*true', skills_block, re.MULTILINE)
all_skills = list(dict.fromkeys(inline + multi))
print('\n'.join(all_skills) if all_skills else 'NO_ENABLED_SKILLS')
" 2>/dev/null)

  echo "  -> Skills: $skills"

  python3 -c "
import json, sys
fork = '$fork'
skills_raw = '''$skills'''
data = json.load(open('$OUTFILE'))
if skills_raw.strip() in ('NO_SKILLS_SECTION', 'NO_ENABLED_SKILLS', ''):
    data[fork] = []
else:
    data[fork] = [s.strip() for s in skills_raw.strip().split('\n') if s.strip()]
json.dump(data, open('$OUTFILE', 'w'))
"
done

echo ""
echo "=== FINAL RESULTS ==="
cat "$OUTFILE"
