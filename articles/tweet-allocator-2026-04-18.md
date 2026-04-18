# Tweet Allocation — 2026-04-18

**Token:** $AEON | **Budget:** $10.00 in $AEON | **Chain:** Base

## Rewards

| Rank | Author | Tweet | Score | Reward | Wallet | Status |
|------|--------|-------|-------|--------|--------|--------|
| 1 | x.com/LemonMarkets | [Likes:8 RTs:5](https://x.com/LemonMarkets/status/2045192278071808182) | 23 | $10.00 in $AEON | 0xcb0b73ab388a389e36abf4c913cc095c63497289 | pending |

**Total allocated:** $10.00 in $AEON to 1 author

---

## Excluded

- **Project accounts (self-dealing):** aaronjmars (4 tweets), aeonframework (1 tweet)
- **No Bankr wallet:** none dropped
- **Already paid today:** none

## Send Command (manual)

```bash
# Bankr Agent API — set BANKR_SEND_KEY before running
curl -s -X POST "https://api.bankr.bot/agent/prompt" \
  -H "X-API-Key: ${BANKR_SEND_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"send 10 $AEON to @LemonMarkets on base"}'
```
