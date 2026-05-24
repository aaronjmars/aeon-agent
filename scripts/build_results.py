#!/usr/bin/env python3
"""Build final JSON results from collected fork data."""
import json

per_fork = {
    "AFHUNTLY/aeon": ["heartbeat"],
    "UIZorrot/aeon": ["heartbeat"],
    "masteramatajj-source/aeon": ["heartbeat"],
    "yehorcallmedai-maker/aeon": ["heartbeat"],
    "sooyooshq/aeon": ["heartbeat"],
    "liquidpadbot/aeon": ["heartbeat"],
    "shiyankuan-crypto/aeon": ["heartbeat"],
    "lawbworld-tech/aeon": ["lawb-pool-monitor", "heartbeat"],
    "luazhizhan/aeon": ["heartbeat"],
    "imthefounder/aeon": ["heartbeat"],
    "sherwoodagent/aeon": ["heartbeat"],
    "gitlawbounty/aeon": ["heartbeat"],
    "bweick/aeon": ["heartbeat"],
    "0xShak/aeon": ["heartbeat"],
    "taekwonv89/aeon": ["morning-brief", "token-movers", "token-report", "price-threshold-alert", "market-context-refresh", "narrative-tracker", "reg-monitor", "self-improve", "reflect", "evening-recap", "cost-report", "weekly-review", "heartbeat"],
    "svenakira/aeon": ["heartbeat"],
    "happycamper-stix/aeon": ["heartbeat"],
    "ryjin111/aeon": ["heartbeat"],
    "cersei420/aeon": ["crypto-research", "fitness-tracker", "heartbeat"],
    "wx888/aeon": ["heartbeat"],
    "jonathanjoseph20/aeon": [],  # only channels/telegram have enabled:true, no skills
    "fleet-watcher/aeon": ["heartbeat"],
    "danbuildss/aeon": ["heartbeat"],
    "smolboon/aeon": ["heartbeat"],
    "0xMal0u/aeon": ["morning-brief", "on-chain-monitor", "narrative-tracker", "refresh-x", "competitor-launch-radar", "show-hn-draft", "product-hunt-launch", "heartbeat"],
    "youpsla/aeon": ["heartbeat"],
    "PyroFire-Labs/larry": ["heartbeat"],
    "LiamVisionary/aeon": ["heartbeat"],
    "bitcoiner-lab/aeon": ["heartbeat"],
    "antfleet-ops/aeon": ["heartbeat"],
    "forge-executive/forge-executive": ["monitor-polymarket", "morning-brief", "research-brief", "thread-formatter", "write-tweet", "market-context-refresh", "evening-recap", "heartbeat", "cost-report"],
    "DABAGElover/aeon": ["heartbeat"],
    "levi-oss-code/aeon": ["heartbeat"],
    "damo-nu11/aeon-minebean": ["mine-bean", "heartbeat"],
    "We3In/vvvkerrnel": ["heartbeat"],
    "We3In/vvvkernel-skills-up": ["heartbeat"],
    "We3In/aeon": ["heartbeat"],
    "abhirajprasad/aeon": ["heartbeat"],
    "coinhome190-spec/aeon": ["heartbeat"],
    "VibeSan7/aeon": ["morning-brief", "pr-review", "research-brief", "deep-research", "skill-health", "heartbeat"],
    "anomit/aeon": ["powerloom-bds", "heartbeat"],
    "enzoonchain/aeon": ["heartbeat", "skill-health", "cost-report", "token-movers", "defi-monitor", "on-chain-monitor", "morning-brief"],
    "sinan33644061-lab/aeon": ["heartbeat"],
    "wuyu663/aeon": ["heartbeat"],
    "DevZenPro/aeon": ["token-movers", "monitor-runners", "market-context-refresh", "narrative-tracker", "aixbt-pulse", "heartbeat"],
    "AntFleet/aeon-bench": ["heartbeat"],
    "foreverxdord/aeon": ["heartbeat"],
    "oxkaiba/aeon": ["heartbeat"],
    "baseddevoloper/vvvkernel-skills": ["heartbeat"],
    "Azh1er/aeon": ["token-movers", "monitor-runners", "token-call", "market-context-refresh", "narrative-tracker", "aixbt-pulse", "perps-scan", "daily-ops-review", "perps-brief", "morning-macro", "heartbeat"],
    "takanafur/aeon": ["heartbeat"],
    "KevinFreistroffer/aeon": ["heartbeat"],
    "0xMortimer/aeon": ["heartbeat"],
    "lioapple/aeon": ["heartbeat"],
    "ashneil12/aeon": ["morning-brief", "token-movers", "repo-pulse", "hermesos-growth-desk", "hermesos-finance-risk-review", "cost-report", "weekly-shiplog", "posthog-session-analyzer", "hermesos-backup-restore-watch", "proxmox-capacity", "fleet-sweep", "heartbeat"],
    "jiamicuisi-a11y/aeon": ["heartbeat"],
    "madebyshun/blueagent-aeon": ["github-monitor", "token-movers", "distribute-tokens", "token-pick", "narrative-tracker", "deep-research", "heartbeat"],
    "meichuanyi/aeon": ["heartbeat"],
    "johnny5OO/aeon": ["heartbeat"],
    "speend/aeon": ["heartbeat"],
    "amandi99/aeon": ["heartbeat"],
    "Daniel-DDV/aeon": ["heartbeat"],
    "usiclabs/aeon": ["heartbeat"],
    "Danypsy/aeon": ["heartbeat"],
    "Da6hkin/aeon": ["heartbeat"],
    "theipgirl/aeon": ["morning-brief", "hacker-news-digest", "stale-lead-report", "competitor-watch", "eric-sharpe-prep", "threads-ip-post", "deep-research", "idea-capture", "goal-tracker", "skill-health", "action-converter", "weekly-review", "omi-sync", "heartbeat"],
    "traewang/aeon-contrib": ["heartbeat"],
    "itr010038/aeon": ["token-alert", "token-movers", "on-chain-monitor", "monitor-polymarket", "token-pick", "token-report", "market-context-refresh", "narrative-tracker", "polymarket-comments", "unlock-monitor", "research-feed-writer", "meme-context-writer", "skill-health", "self-improve", "skill-repair", "evening-recap", "heartbeat"],
    "varun86/aeon": ["heartbeat"],
    "fsgaleti-create/aeon": ["heartbeat"],
    "Boodszw/Boodszw_Bread": ["token-alert", "token-movers", "on-chain-monitor", "defi-monitor", "monitor-polymarket", "monitor-kalshi", "token-pick", "token-report", "market-context-refresh", "narrative-tracker", "skill-health", "cost-report", "heartbeat"],
    "jimimased/aeon": ["heartbeat"],
    "Aldine/aeon": ["heartbeat"],
    "ether-btc/aeon": ["github-upstream-tracker", "heartbeat"],
    "FreyjasWrath/aeon": ["heartbeat"],
    "infrareactive/aeon": ["heartbeat"],
    "CNZSMJ/aeon": ["heartbeat"],
    "eugene-gourevitch/aeon": ["heartbeat"],
    "adarshhalan/aeon": ["heartbeat"],
    "tomscaria/aeon": ["morning-brief", "daily-routine", "rss-digest", "hacker-news-digest", "paper-digest", "reddit-digest", "telegram-digest", "token-alert", "token-movers", "on-chain-monitor", "defi-monitor", "treasury-info", "distribute-tokens", "defi-overview", "monitor-polymarket", "monitor-kalshi", "monitor-runners", "token-pick", "token-report", "market-context-refresh", "narrative-tracker", "polymarket-comments", "deep-research", "last30", "paper-pick", "vuln-scanner", "config-audit", "deploy-prototype", "autoresearch", "create-skill", "fetch-tweets", "refresh-x", "list-digest", "write-tweet", "reply-maker", "tweet-roundup", "agent-buzz", "channel-recap", "goal-tracker", "skill-health", "monetize-revenant", "tool-builder", "skill-repair", "evening-recap", "cost-report", "session-learner", "spawn-instance", "workflow-security-audit", "task-planner", "auto-workflow", "onboard", "heartbeat"],
    "yugo-engineer/aeon": ["heartbeat"],
    "pezetel/aeon": ["github-trending", "heartbeat"],
    "gcampton/aeon": ["heartbeat"],
    "AmithKumar1/aeon": ["heartbeat"],
}

# Count skill occurrences
skill_counts = {}
no_yaml_forks = []
readable_forks = []

for fork, skills in per_fork.items():
    if skills == "NO_YAML":
        no_yaml_forks.append(fork)
    else:
        readable_forks.append(fork)
        for skill in skills:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1

# Sort by count descending
skill_counts_sorted = dict(sorted(skill_counts.items(), key=lambda x: -x[1]))

result = {
    "readable_forks": len(readable_forks),
    "no_yaml_forks": len(no_yaml_forks),
    "skill_counts": skill_counts_sorted,
    "per_fork": per_fork
}

print(json.dumps(result, indent=2))
