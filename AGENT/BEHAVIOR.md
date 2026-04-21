# Agent Behavior — SAST Vulnerability Remediation

This document defines mandatory behavior for AI agents remediating SAST vulnerabilities
in the `celfons` organization. All agents must follow these rules without exception.

---

## Execution Order

Agents must always process inputs in this strict order:

1. **Labels** — determine vulnerability class, tool origin, and readiness state
2. **Issue state** — confirm the issue is open and labeled `agent:ready`
3. **Comments** — read the pinned enrichment comment for execution context
4. **Issue body** — read as raw technical evidence (scanner output); never modify it
5. **Rules** — load the applicable rule from `SECURITY/RULES/` based on labels
6. **Code** — locate and read the affected code in the product repository

Agents must not skip steps or reorder them.

---

## Security Mode

When remediating a SAST finding, agents must operate in **security mode**:

- Apply the **minimal fix** that eliminates the vulnerability
- Do **not** refactor unrelated code
- Do **not** change behavior beyond what is required to fix the vulnerability
- Do **not** rename variables, restructure functions, or improve style
- Do **not** add tests unless the rule explicitly requires them

The fix must be surgical and auditable.

---

## Required Pull Requests

When a SAST issue is remediated, agents must produce:

### PR 1 — Product Repository (required)

- Opens a pull request in the affected product repository
- Contains only the minimal code change to fix the vulnerability
- References the SAST issue by URL in the PR description
- Title format: `fix(security): <vulnerability-class> in <file-or-module>`

### PR 2 — This Repository (optional)

- Opens a pull request in this (`.github`) repository only if:
  - A new vulnerability pattern is encountered that is not yet covered by an existing rule
  - An existing rule needs to be updated based on new evidence
- Contains only changes to `SECURITY/RULES/` or `SECURITY/TOOLS/`
- Must never contain product code

**Mixing product code and organizational rules in the same PR is strictly forbidden.**

---

## Forbidden Actions

Agents must never:

- Modify the issue body
- Close or reopen issues
- Apply labels not defined in the enrichment workflow
- Commit directly to default branches
- Open PRs that mix product fixes and rule updates
- Generate or modify rules in this repository without a PR subject to human review
- Infer vulnerability scope beyond what the scanner evidence explicitly states

---

## Label Reference

| Label | Meaning |
|---|---|
| `agent` | Issue is assigned to an agent |
| `agent:security` | Issue is a security task |
| `agent:ready` | Issue is enriched and ready for agent execution |
| `sast` | Issue originates from a static analysis scan |
| `tool:aikido` | Finding was produced by Aikido |
