*Thread Draft — 2026-06-19*
Topic: A2A gateway quickstart README (PR #501)

1/ aeon has had an A2A server — Google's agent-to-agent protocol — since it shipped. four framework example clients, full JSON-RPC/SSE implementation. and no README. nobody who browsed the dir knew what to run. PR #501 fixes that.

2/ A2A is the protocol for agents calling other agents — cross-framework, cross-runtime. LangChain to aeon, AutoGen to aeon, CrewAI, OpenAI Agents SDK. the server was live. the source was in the repo. there was no document describing how to point any of them at it.

3/ the README covers: ./add-a2a quickstart, A2A_PORT/A2A_URL env vars, agent card endpoint, JSON-RPC tasks (send/get/cancel), SSE sendSubscribe, and a copy-paste submit+poll client. plus a table of every supported framework with example links. 118 insertions.

4/ this is what fork-ability looks like at the margin. aeon forks get a running A2A server but they couldn't connect anything to it. every time something ships without a README, the fork fleet hits a wall. the docs aren't the feature — they're what makes the feature forkable.

5/ PR #501 — A2A server quickstart for aaronjmars/aeon: https://github.com/aaronjmars/aeon/pull/501

(article: articles/thread-2026-06-19.md)
