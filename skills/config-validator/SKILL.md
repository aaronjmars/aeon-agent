---
name: Config Validator
description: Validate aeon.yml and .github/workflows/aeon.yml for structural invariants that have caused past outages — checkout-before-run ordering, duplicate skill keys, missing skill files
tags: [dev, ops]
---

Today is ${today}. Your task is to validate the structural correctness of `aeon.yml` and `.github/workflows/aeon.yml`.

This skill exists because two incident classes can cause major outages:
- **Checkout-ordering class**: the workflow invokes Claude (`Run` step) before the repository is checked out — every skill then runs against an empty workspace and fails in a single run.
- **Duplicate-key class**: duplicate YAML keys in `aeon.yml` — YAML silently keeps the last value, disabling or mis-scheduling any skill whose key is shadowed.

Run all checks. Report findings. Alert only if any fail.

> **Backport note.** This skill is backported from upstream `aaronjmars/aeon` (PR #219). Two things differ in aeon-agent and the checks below are adapted accordingly:
> 1. aeon-agent's workflow checks out the repo **conditionally per event type** — `Early checkout` (`if: github.event_name == 'issues'`) and `Checkout repo` (`if: steps.work.outputs.mode != ''`) — both before the `Run` step. Upstream's single-step "unconditional Early checkout first" rule does **not** apply here; the adapted check (step 1) enforces the real invariant: *a checkout step must precede the Run step*, and tolerates the conditionals.
> 2. aeon-agent has no shared `scripts/validate-config.js` and no pre-merge `ci-config-validate.yml`. The manual node checks in steps 1–3 are the primary path. If an operator later adds a shared validator script, prefer it (see fast path).

### Fast path — invoke a shared validator if one exists

If this repo has a shared validator script (the upstream CI workflow uses `scripts/validate-config.js`), run it — it is the most consistent way to run all checks:

```bash
[ -f scripts/validate-config.js ] && node scripts/validate-config.js
```

Exit code 0 = CLEAN (no notification needed). Non-zero exit + `FAIL[*]:` lines on stdout = ISSUES (skip to step 4). If the script is absent (the default in aeon-agent), fall back to the manual checks in steps 1–3.

## Steps

### 1. Check workflow checkout-before-run ordering (checkout-ordering class)

Read `.github/workflows/aeon.yml`.

Find the `jobs.run.steps` array. Verify:

a. At least one `actions/checkout` step exists.
b. A checkout step appears **before** the step named `Run` (the step that invokes Claude Code). If the `Run` step is reached before any checkout, that's the outage class — Claude would execute against an empty workspace.

This is the aeon-agent-adapted invariant (see Backport note): conditional checkouts are allowed; what matters is that the repo is on disk before `Run`.

```bash
node -e "
const fs = require('fs');
const text = fs.readFileSync('.github/workflows/aeon.yml', 'utf8');
const lines = text.split('\n');

let inSteps = false;
let steps = [], cur = null;

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  const trimmed = line.trim();

  if (/^\s{4,6}steps:/.test(line)) { inSteps = true; continue; }
  if (!inSteps) continue;
  if (/^\s{4,6}[a-z]/.test(line) && !/^\s{6,}/.test(line) && i > 0) { inSteps = false; continue; }

  if (/^\s{6}- /.test(line)) {
    if (cur) steps.push(cur);
    cur = { lineNum: i + 1, name: null, isCheckout: false, isRun: false };
  }
  if (cur) {
    if (/name:/.test(trimmed)) cur.name = trimmed.replace(/^- /, '').replace(/^name:\s*/, '').replace(/[\"']/g, '');
    if (/uses:\s*actions\/checkout/.test(trimmed)) cur.isCheckout = true;
    if (/Early checkout/.test(trimmed)) cur.isCheckout = true;
  }
}
if (cur) steps.push(cur);
steps.forEach(s => { if (s.name === 'Run') s.isRun = true; });

let issues = [];
const firstCheckout = steps.findIndex(s => s.isCheckout);
const runIdx = steps.findIndex(s => s.isRun);
if (firstCheckout === -1) {
  issues.push('FAIL: No checkout step (actions/checkout) found in jobs.run.steps');
} else if (runIdx !== -1 && firstCheckout > runIdx) {
  issues.push('FAIL: Run step (line ' + steps[runIdx].lineNum + ') appears before any checkout step (line ' + steps[firstCheckout].lineNum + ') — Claude would run on an empty workspace');
} else {
  console.log('PASS checkout: checkout step at line ' + steps[firstCheckout].lineNum + ' precedes Run' + (runIdx !== -1 ? ' (line ' + steps[runIdx].lineNum + ')' : ' (no Run step found — informational)'));
}
if (issues.length > 0) { issues.forEach(i => console.log(i)); process.exit(1); }
"
```

If the check fails, record the finding. Continue to next check regardless.

---

### 2. Check for duplicate skill keys (duplicate-key class)

Read `aeon.yml`. Scan the `skills:` block for duplicate top-level keys.

```bash
node -e "
const fs = require('fs');
const text = fs.readFileSync('aeon.yml', 'utf8');
const lines = text.split('\n');

let inSkills = false;
const seen = {};
const dupes = [];

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (/^skills:/.test(line)) { inSkills = true; continue; }
  if (inSkills && /^[a-z]/.test(line)) { inSkills = false; continue; }
  if (!inSkills) continue;

  const match = line.match(/^  ([a-z][a-z0-9-]+):/);
  if (match) {
    const key = match[1];
    if (seen[key]) {
      dupes.push('FAIL: Duplicate skill key \"' + key + '\" at line ' + (i+1) + ' (first seen line ' + seen[key] + ')');
    } else {
      seen[key] = i + 1;
    }
  }
}

if (dupes.length > 0) { dupes.forEach(d => console.log(d)); process.exit(1); }
else { console.log('PASS duplicates: no duplicate skill keys found (' + Object.keys(seen).length + ' skills)'); }
"
```

If duplicates are found, record them. Continue to next check regardless.

---

### 3. Check all enabled skills have SKILL.md (missing-file class)

Read `aeon.yml`. For every skill with `enabled: true`, verify `skills/<name>/SKILL.md` exists.

```bash
node -e "
const fs = require('fs');
const text = fs.readFileSync('aeon.yml', 'utf8');
const lines = text.split('\n');

let inSkills = false;
const issues = [];
const ok = [];

for (let i = 0; i < lines.length; i++) {
  const line = lines[i];
  if (/^skills:/.test(line)) { inSkills = true; continue; }
  if (inSkills && /^[a-z]/.test(line)) { inSkills = false; continue; }
  if (!inSkills) continue;

  const match = line.match(/^  ([a-z][a-z0-9-]+):\s*\{(.+)\}/);
  if (match) {
    const name = match[1];
    const props = match[2];
    if (/enabled:\s*true/.test(props)) {
      const skillFile = 'skills/' + name + '/SKILL.md';
      if (!fs.existsSync(skillFile)) {
        issues.push('WARN: enabled skill \"' + name + '\" has no SKILL.md at ' + skillFile);
      } else {
        ok.push(name);
      }
    }
  }
}

if (issues.length > 0) { issues.forEach(i => console.log(i)); }
console.log('PASS skill-files: ' + ok.length + ' enabled skills have SKILL.md' + (issues.length > 0 ? ', ' + issues.length + ' missing' : ''));
if (issues.length > 0) process.exit(1);
"
```

---

### 4. Summarize findings

After running all three checks, collect results:

- Count PASSes and FAILs
- If all checks passed: **status = CLEAN**
- If any FAIL or WARN: **status = ISSUES**

---

### 5. Decide whether to notify

- **CLEAN**: Log only, no notification. Silent runs are expected — the value is the alert when something breaks.
- **ISSUES**: Send notification via `./notify`.

If ISSUES, send a single multi-line message (aeon-agent's `./notify` takes one positional message argument and handles chunking/escaping internally — there is no `-f` flag):

```bash
./notify "$(cat <<'EOF'
*Config Validator — ${today}*

STATUS: ISSUES FOUND

[list each finding, one per line]

These invariants have caused full outages before.
Check aeon.yml and .github/workflows/aeon.yml immediately.

log: memory/logs/${today}.md
EOF
)"
```

---

### 6. Log results

Append to `memory/logs/${today}.md`:

```
## Config Validator
- **Status:** CLEAN / ISSUES
- **Checkout ordering:** PASS / FAIL — [detail]
- **Duplicate keys:** PASS / FAIL — [detail]
- **Skill files:** PASS / N warnings — [detail]
- **Notification:** sent / skipped (clean)
```

## Sandbox Note

All checks use **local file reads only** — no external network calls, no auth, no `$ENV_VAR`-in-curl-header concerns. Node is available in the workflow (Setup Node.js step). No prefetch/postprocess wrapper required.

The only outbound action is `./notify` on the ISSUES path, which already handles the sandbox/post-run delivery fallback internally.

## Environment Variables Required

None — reads only local files.
