# Repo Action Ideas — 2026-05-30

*Generated from analysis of aaronjmars/aeon (464⭐, 142 forks, 16 open issues), aaronjmars/aeon-agent, and aaronjmars/minitor.*

---

## Context

**aeon** is accelerating on two fronts simultaneously: external contributor inflow (10+ open PRs from HoundFlow, MandateSeal, antfleet-ops, rsavitt) and infrastructure maturation (capabilities taxonomy CI check just shipped, skill-packs.json manifest gaining structured fields). The .x402books/wallets.json file declaring treasury + deployer addresses on Base was merged yesterday — the first signal that aeon is thinking about on-chain agent economics. The PR queue is deep enough that a human reviewer working alone is going to fall behind.

**aeon-agent** completed its 17th consecutive same-day-after backport today (fork-health-score). The upstream gap detector idea below would close the feedback loop that currently lives only in the operator's memory.

**minitor** shipped tab groups (#53) and column collapse (#55, open PR) in the same 24h window, tightening the deck-density UX axis. PR #54 (expose CoinGecko demo API key in settings) is open and signals a gap in API key discoverability — but with 47+ column types already shipping and no open feature requests, the most impactful next move is giving analysts a way out: raw data export.

---

### 1. x402 Wallet Balance Tracker
**Type:** Integration
**Effort:** Small (hours)
**Impact:** The .x402books/wallets.json file (merged 2026-05-29, PR #273) declares a treasury wallet (`0xf1e958...`) and a deployer wallet (`0x67976c...`) on Base. Right now aeon knows its token price but not how much ETH or USDC the agent itself holds. As x402 HTTP micropayments become a real use pattern for AI agents paying for API access or tipping contributors, the agent needs visibility into its own liquidity. Adding a balance line to the daily token-report makes that visible without a new cron slot.

**How:**
1. New step in `skills/token-report/SKILL.md` — read `.x402books/wallets.json` via `gh api repos/aaronjmars/aeon/contents/.x402books/wallets.json --jq '.content' | base64 -d` to get addresses.
2. Query Base chain ETH balance per address via BaseScan API (`WebFetch https://api.basescan.org/api?module=account&action=balance&address=0x...&apikey=free`) as primary; ALCHEMY_API_KEY eth_getBalance call as secondary if configured.
3. Add a "## Treasury" subsection to the token-report article and notification — one line per wallet: address (abbreviated), role, ETH balance. Alert if treasury ETH drops below 0.01 ETH (gas reserve floor).

---

### 2. Skill Capabilities Coverage Map
**Type:** Community / DX
**Effort:** Small (hours)
**Impact:** AntFleet PRs #267 (secrets_required) and #268 (capabilities array) just landed, giving skill-packs.json a structured vocabulary. The CI parity check (PR #304, merged today) locks the 6-value taxonomy. The next logical step is a read-only audit skill that answers "which capabilities does this operator's aeon instance actually cover?" — a weekly matrix grouping enabled skills by capability tier, flagging any capability in the taxonomy that has zero enabled coverage. Helps operators discover skill gaps before they matter in production.

**How:**
1. New `skills/capabilities-map/SKILL.md` — read `skills.json` to enumerate all installed skills; read `skill-packs.json` to extract capabilities arrays.
2. Cross-reference against `aeon.yml` to determine which skills are enabled vs. disabled.
3. Produce a weekly article with a markdown table: rows = 6 locked capability values, columns = {installed skills covering it (enabled) / installed skills covering it (disabled) / gaps}. Notify only if a capability tier has zero enabled coverage (actionable signal, not noise).

---

### 3. PR Merge-Priority Digest
**Type:** Feature
**Effort:** Medium (1-2 days)
**Impact:** Ten external PRs are open on aaronjmars/aeon right now — HoundFlow's 6 investigation skills (#281-#287), MandateSeal's Guard pack (#295), antfleet-ops' wallet/fork notes (#302-#303), rsavitt's atlas skill (#305). The pr-skill-triage skill can evaluate individual skill PRs, but there's no skill that surveys the full open queue, groups by risk tier, and surfaces the safest merge candidates first. At the current contribution velocity, a human reviewer working through the list manually will fall behind.

**How:**
1. New `skills/pr-merge-queue/SKILL.md` — workflow_dispatch, takes optional `repo` var (defaults to aaronjmars/aeon). Query open PRs via `gh api repos/{repo}/pulls?state=open&per_page=50`.
2. Categorize by touched files: PRs changing only `docs/` or `README*` → FAST_TRACK; PRs changing `.github/workflows/` → INFRA_REVIEW; PRs changing `skills/*/SKILL.md` → invoke `skills/skill-security-scan/scan.sh` and report PASS/WARN/BLOCK verdict; PRs touching `install-skill-pack` or `aeon.yml` → CORE_REVIEW.
3. Emit Telegram digest with four buckets (FAST_TRACK / INFRA_REVIEW / SKILL_PASS / SKILL_WARN_OR_BLOCK), each sorted by PR age descending. One line per PR: number, title, author, age, verdict. Operator can merge FAST_TRACK PRs immediately; others have a clear action.

---

### 4. Upstream-Gap Detector (aeon-agent)
**Type:** DX
**Effort:** Small (hours)
**Impact:** The 17-consecutive-day same-day-after backport chain is running purely on the operator knowing what to look for in upstream. If a skill merges in aeon on a day when the operator's attention is elsewhere, it could sit unbackported for days with no signal. A weekly read-only skill that diffs `skills/` in aeon-agent against upstream aaronjmars/aeon and outputs a sorted queue (by upstream merge date) makes the gap explicit and eliminates the risk of silent drift — especially relevant as the upstream pipeline accelerates with external contributors.

**How:**
1. New `skills/upstream-gap/SKILL.md` — read local `skills/` directory entries; compare against `gh api repos/aaronjmars/aeon/contents/skills --jq '[.[].name]'` to get upstream skill names.
2. For each skill present upstream but absent locally, fetch upstream merge date: `gh api repos/aaronjmars/aeon/commits?path=skills/{name}/SKILL.md --jq '.[0].commit.committer.date'`.
3. Sort by merge date ascending (oldest gap first). Article: table with columns: skill name, upstream merged date, days pending. Notify if any skill has been pending > 48h. Write state to `memory/topics/upstream-gap-state.json` so the weekly diff can surface new arrivals vs. long-stale entries.

---

### 5. Column Data Export (minitor)
**Type:** Feature
**Effort:** Small (hours)
**Impact:** Minitor now has 47+ column types — crypto prices, GitHub signals, social feeds, news, DeFi TVL. Power users and analysts who use it as a monitoring hub frequently want the raw fetched data for spreadsheets, re-processing, or archiving, but there's no export path today. A "Download items (JSON)" option in the column More menu gives them a one-click out with zero DB changes or new server actions required — data is already in the Zustand store.

**How:**
1. Add `downloadColumnItems(columnId: string, columnTitle: string)` to `lib/store/use-deck-store.ts` — reads the column's cached items array from store state, serializes to JSON, calls `URL.createObjectURL(new Blob([JSON.stringify(items, null, 2)], {type: 'application/json'}))`, triggers a synthetic `<a download>` click, then revokes the object URL.
2. Add "Download items (JSON)" entry to the More dropdown in `components/column/column-card.tsx` — use `DownloadIcon` from lucide-react; show the option only when the column has at least 1 fetched item (disabled + tooltip "No items loaded yet" otherwise).
3. Filename format: `{columnTitle}-{YYYY-MM-DD}.json` — include the column title slug + date so downloaded files self-document when accumulated over time.
