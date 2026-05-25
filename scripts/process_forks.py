#!/usr/bin/env python3
"""Process all 86 forks and extract enabled skills from aeon.yml"""
import subprocess
import json
import base64
import re

FORKS = [
    "AFHUNTLY/aeon", "UIZorrot/aeon", "masteramatajj-source/aeon", "yehorcallmedai-maker/aeon",
    "sooyooshq/aeon", "liquidpadbot/aeon", "shiyankuan-crypto/aeon", "lawbworld-tech/aeon",
    "luazhizhan/aeon", "imthefounder/aeon", "sherwoodagent/aeon", "gitlawbounty/aeon",
    "bweick/aeon", "0xShak/aeon", "taekwonv89/aeon", "svenakira/aeon",
    "happycamper-stix/aeon", "ryjin111/aeon", "cersei420/aeon", "wx888/aeon",
    "jonathanjoseph20/aeon", "fleet-watcher/aeon", "danbuildss/aeon", "smolboon/aeon",
    "0xMal0u/aeon", "youpsla/aeon", "PyroFire-Labs/larry", "LiamVisionary/aeon",
    "bitcoiner-lab/aeon", "antfleet-ops/aeon", "forge-executive/forge-executive",
    "DABAGElover/aeon", "levi-oss-code/aeon", "damo-nu11/aeon-minebean", "We3In/vvvkerrnel",
    "We3In/vvvkernel-skills-up", "We3In/aeon", "abhirajprasad/aeon", "coinhome190-spec/aeon",
    "VibeSan7/aeon", "anomit/aeon", "enzoonchain/aeon", "sinan33644061-lab/aeon",
    "wuyu663/aeon", "DevZenPro/aeon", "AntFleet/aeon-bench", "foreverxdord/aeon",
    "oxkaiba/aeon", "baseddevoloper/vvvkernel-skills", "Azh1er/aeon", "takanafur/aeon",
    "KevinFreistroffer/aeon", "0xMortimer/aeon", "lioapple/aeon", "ashneil12/aeon",
    "jiamicuisi-a11y/aeon", "madebyshun/blueagent-aeon", "meichuanyi/aeon", "johnny5OO/aeon",
    "speend/aeon", "amandi99/aeon", "Daniel-DDV/aeon", "usiclabs/aeon", "Danypsy/aeon",
    "Da6hkin/aeon", "theipgirl/aeon", "traewang/aeon-contrib", "itr010038/aeon",
    "varun86/aeon", "fsgaleti-create/aeon", "Boodszw/Boodszw_Bread", "jimimased/aeon",
    "Aldine/aeon", "ether-btc/aeon", "FreyjasWrath/aeon", "infrareactive/aeon",
    "CNZSMJ/aeon", "eugene-gourevitch/aeon", "adarshhalan/aeon", "tomscaria/aeon",
    "yugo-engineer/aeon", "pezetel/aeon", "gcampton/aeon", "AmithKumar1/aeon",
]

def extract_enabled_skills(content):
    """Extract enabled skills from aeon.yml content (skills section only)."""
    # Find the skills section
    skills_match = re.search(r'^skills:\s*\n((?:[ \t]+.*\n?)*)', content, re.MULTILINE)
    if not skills_match:
        return None  # No skills section

    skills_block = skills_match.group(1)

    # Find inline format: skill-name: { enabled: true, ...}
    inline = re.findall(r'^[ \t]+([a-z][a-z0-9_-]+):\s*\{[^}]*enabled:\s*true', skills_block, re.MULTILINE)
    # Find multiline format
    multi = re.findall(r'^[ \t]+([a-z][a-z0-9_-]+):\s*\n(?:[ \t]+.*\n)*?[ \t]+enabled:\s*true', skills_block, re.MULTILINE)

    return list(dict.fromkeys(inline + multi))

def fetch_aeon_yml(fork):
    """Fetch aeon.yml from a fork via gh api."""
    result = subprocess.run(
        ["gh", "api", f"repos/{fork}/contents/aeon.yml", "--jq", ".content"],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0 or not result.stdout.strip() or result.stdout.strip() == "null":
        return None

    try:
        content_b64 = result.stdout.strip()
        # Handle multi-line base64
        content_b64_clean = content_b64.replace('\n', '').replace('"', '')
        decoded = base64.b64decode(content_b64_clean).decode('utf-8', errors='replace')
        return decoded
    except Exception as e:
        print(f"  Decode error for {fork}: {e}")
        return None

per_fork = {}
no_yaml_forks = []
readable_forks = []
skill_counts = {}

for i, fork in enumerate(FORKS):
    print(f"[{i+1}/{len(FORKS)}] Processing {fork}...")

    content = fetch_aeon_yml(fork)
    if content is None:
        per_fork[fork] = "NO_YAML"
        no_yaml_forks.append(fork)
        print(f"  -> NO_YAML")
        continue

    skills = extract_enabled_skills(content)
    if skills is None:
        per_fork[fork] = []
        readable_forks.append(fork)
        print(f"  -> NO_SKILLS_SECTION (empty list)")
    else:
        per_fork[fork] = skills
        readable_forks.append(fork)
        for skill in skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
        print(f"  -> {skills}")

# Final summary
print("\n" + "="*60)
print("RESULTS")
print("="*60)

summary = {
    "readable_forks": len(readable_forks),
    "no_yaml_forks": len(no_yaml_forks),
    "skill_counts": dict(sorted(skill_counts.items(), key=lambda x: -x[1])),
    "per_fork": per_fork
}

print(json.dumps(summary, indent=2))
