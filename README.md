# .github — Organizational Governance Repository

This repository defines organizational governance for the `celfons` GitHub organization.
It contains no product code. Its purpose is to act as the control plane for AI-agent-driven
SAST vulnerability remediation.

---

## Purpose

- Defines how AI agents must behave when remediating security vulnerabilities
- Stores reusable remediation rules as the single source of truth
- Hosts GitHub Actions workflows that enrich, orchestrate, and validate security issues
- Maintains a living knowledge base of organizational patterns via the Context Mesh

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

## Full Execution Flow

```
Issue opened (via API)
  → enrich-sast-issue.yml
      → adds labels: agent, agent:security, sast, tool:aikido
      → pins enrichment comment with execution context
      → adds label: agent:ready

  → ai-agent-orchestration.yml — Job 1: Triage
      → uses gpt-4o-mini (GitHub Models) to identify relevant context-mesh files
      → adds label: triage-done

  → ai-agent-orchestration.yml — Job 2: Planner
      → uses gpt-4o (GitHub Models) to generate an action plan
      → posts plan as a comment (delimited by <!-- ai-agent-plan-start/end --> markers)
      → adds label: plan-ready
      → awaits human approval (label: ai-approved)

  → ai-agent-orchestration.yml — Job 3: Executor
      → triggered when label 'ai-approved' is added
      → uses GitHub Copilot agent to apply the plan
      → opens PR on branch ai-agent/issue-<number>-<timestamp>
      → adds label: executing

  → validate-agent-pr.yml
      → warns if the PR does not reference a SAST issue

  → Human reviews and merges PR in the product repository
  → Optional PR in this repository to add or update a rule in SECURITY/RULES/
```

```mermaid
flowchart TD
    A([Aikido SAST Scan]) --> B([Jira])
    B --> C([GitHub API])
    C --> D[Issue opened in .github]

    D --> E[enrich-sast-issue.yml]
    E --> E1[Adds labels:\nagent, agent:security,\nsast, tool:aikido]
    E1 --> E2[Pins enrichment comment\nwith execution context]
    E2 --> E3[Adds label: agent:ready]

    E3 --> F[ai-agent-orchestration.yml\nJob 1 — Triage]
    F --> F1[gpt-4o-mini identifies\nrelevant context-mesh files]
    F1 --> F2[Adds label: triage-done]

    F2 --> G[ai-agent-orchestration.yml\nJob 2 — Planner]
    G --> G1[gpt-4o generates\naction plan]
    G1 --> G2[Posts plan as comment\nai-agent-plan-start/end]
    G2 --> G3[Adds label: plan-ready]

    G3 --> H{Human Review}
    H -->|Approves| H1[Adds label: ai-approved]
    H -->|Rejects / requests changes| H2([End — plan revised\nor issue closed])

    H1 --> I[ai-agent-orchestration.yml\nJob 3 — Executor]
    I --> I1[GitHub Copilot agent\napplies the plan]
    I1 --> I2[Opens PR on branch\nai-agent/issue-N-timestamp]
    I2 --> I3[Adds label: executing]

    I2 --> J[validate-agent-pr.yml]
    J --> J1{PR references\nSAST issue?}
    J1 -->|No| J2[Warning posted on PR]
    J1 -->|Yes| J3[Validation passes]

    I3 --> K{Human reviews\nPR in product repo}
    K -->|Merges| L([Fix applied in\nproduct repository])
    K -->|Requests changes| I1

    L --> M{New rule\nneeded?}
    M -->|Yes| N[PR to add/update rule\nin SECURITY/RULES/]
    N --> O([Rule merged into\ngovernance repository])
    M -->|No| P([Flow complete])
```

---

## Label State Machine

Issues progress through these states in order:

| Label | Set by | Meaning |
|---|---|---|
| `agent` | enrich-sast-issue | Issue is assigned to an agent |
| `agent:security` | enrich-sast-issue | Issue is a security task |
| `sast` | enrich-sast-issue | Issue originates from a static analysis scan |
| `tool:aikido` | enrich-sast-issue | Finding was produced by Aikido |
| `agent:ready` | enrich-sast-issue | Issue is enriched and ready for orchestration |
| `triage-done` | ai-agent-orchestration (Job 1) | Context files identified |
| `plan-ready` | ai-agent-orchestration (Job 2) | Action plan generated; awaiting human approval |
| `ai-approved` | Human | Plan approved; triggers the executor job |
| `executing` | ai-agent-orchestration (Job 3) | Executor agent is generating the solution |

---

## Workflows

| Workflow | Trigger | Purpose |
|---|---|---|
| `enrich-sast-issue.yml` | Issue opened | Labels the issue and pins the enrichment comment |
| `ai-agent-orchestration.yml` | Issue opened / labeled | Runs the Triage → Planner → Executor pipeline |
| `validate-agent-pr.yml` | PR opened / updated | Warns if the PR does not reference a SAST issue |
| `context-mesh-sanitization.yml` | Weekly (Sunday 00:00 UTC) | Reviews merged PRs and updates the knowledge base |

---

## Context Mesh

The `context-mesh/` directory contains a living knowledge base consumed by the Triage and Planner agents.

- **`context-mesh/knowledge-base.md`** — Curated remediation patterns and organizational conventions
- **`context-mesh/scripts/trim-context.py`** — Utility to cap context to a token budget before sending to the model
- Updated weekly via `context-mesh-sanitization.yml`; changes are always submitted as a pull request for human review

---

## Rules and Governance

- Agents follow `AGENT/BEHAVIOR.md`
- Vulnerability-class rules live in `SECURITY/RULES/`
- Tool-specific interpretation lives in `SECURITY/TOOLS/`
- Security philosophy and architecture are described in `SECURITY/OVERVIEW.md`
- No automation may generate or modify rules without a reviewed pull request to this repository
- Product repositories must **not** duplicate rules defined here
- All automated PRs must reference the originating issue with `Closes #<number>`