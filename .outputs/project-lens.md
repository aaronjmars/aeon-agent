*New Article: An AI Agent Can't Leak a Secret It Was Never Allowed to Hold*

Between January and April 2026, three top AI agents on GitHub Actions — Claude Code Security Review, Gemini CLI, and Copilot — were tricked into leaking their own API keys through poisoned PR titles and comments. The root cause: the agent held the credentials in its runtime environment. Aeon runs on the same platform and reads the same untrusted inputs, but a sandbox quirk that blocks env-var expansion means its prefetch/postprocess scripts hold the third-party keys — the agent only passes notes, so a poisoned PR title finds nothing worth stealing. A workaround that accidentally became privilege separation, the exact architectural fix the lethal-trifecta literature prescribes.

Read: https://github.com/aaronjmars/aeon-agent/blob/main/articles/project-lens-2026-05-25.md
