# .github — Organizational Governance Repository

This repository defines organizational governance for the `celfons` GitHub organization.
It contains no product code. Its purpose is to act as the control plane for AI-agent-driven
SAST vulnerability remediation.

---

## Purpose

- Defines how AI agents must behave when remediating security vulnerabilities
- Stores reusable remediation rules as the single source of truth
- Hosts GitHub Actions workflows that enrich and validate security issues

This repository does **not** define product behavior. It defines **organizational rules**.

---

## How SAST Issues Are Created

SAST vulnerability issues are created automatically via the GitHub API:

```
Aikido (SAST scan) → Jira → GitHub API → Issue in this repository
```

- The issue body is **raw and immutable** — it is technical evidence from the scanner
- The body is **never modified** by any workflow, agent, or human
- The body is **not** a behavioral contract; it is forensic input

---

## How Agents Consume Issues

Agents do **not** read UI templates or GitHub Issue Forms.
They follow:

1. **Labels** — determine scope, tool, and readiness
2. **Comments** — receive enrichment context (pinned by workflow)
3. **Rules** — read from `SECURITY/RULES/` in this repository
4. **Issue body** — read as raw technical evidence only

---

## Execution Flow

```
Issue opened (via API)
  → workflow: enrich-sast-issue.yml
      → adds labels: agent, agent:security, sast, tool:aikido
      → adds pinned comment with execution context
      → adds label: agent:ready
  → Agent reads labels + comment + rules
  → Agent produces minimal fix
  → PR in product repository (code fix)
  → Optional PR in this repository (new/updated rule)
```

---

## Rules

- Agents follow `AGENT/BEHAVIOR.md`
- Vulnerability-class rules live in `SECURITY/RULES/`
- Tool-specific interpretation lives in `SECURITY/TOOLS/`
- No automation may generate or modify rules without a reviewed pull request to this repository
- Product repositories must **not** duplicate rules defined here