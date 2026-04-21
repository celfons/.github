# Security Overview

This document describes the security philosophy and architecture for the `celfons` organization.

---

## Philosophy

Security vulnerabilities are treated as engineering issues, not compliance checkboxes.
Remediation is automated where possible, auditable always, and governed by explicit rules.

The goal is deterministic, minimal, and reviewable fixes — not heroics or wholesale rewrites.

---

## Separation of Concerns

| Concept | Location | Mutable by agents? |
|---|---|---|
| Vulnerability evidence | Issue body (created via API) | No |
| Execution context | Pinned issue comment (added by workflow) | No |
| Remediation rules | `SECURITY/RULES/` in this repo | Only via reviewed PR |
| Tool interpretation | `SECURITY/TOOLS/` in this repo | Only via reviewed PR |
| Agent behavior contract | `AGENT/BEHAVIOR.md` in this repo | Only via reviewed PR |

Evidence (the issue body) is never the source of rules.
Rules live here and grow only through reviewed pull requests.

---

## Vulnerability Pipeline

```
Scanner (Aikido) detects finding
  → Jira ticket created
  → GitHub issue created via API (body = raw scanner evidence)
  → Workflow enriches issue (labels + pinned comment)
  → Agent reads labels, comment, and rules
  → Agent produces minimal fix
  → PR in product repo
  → Optional PR in this repo for new/updated rule
```

---

## Supported Vulnerability Classes

| Class | Rule File |
|---|---|
| SQL Injection (SQLI) | [`SECURITY/RULES/SAST-SQLI.md`](RULES/SAST-SQLI.md) |
| Cross-Site Scripting (XSS) | [`SECURITY/RULES/SAST-XSS.md`](RULES/SAST-XSS.md) |
| Remote Code Execution (RCE) | [`SECURITY/RULES/SAST-RCE.md`](RULES/SAST-RCE.md) |

---

## Governance Principles

- This repository is the **single source** of organizational security knowledge
- No rule may be created or modified without a reviewed pull request
- No automation may write rules
- Product repositories must not duplicate rules defined here
- All decisions are auditable via git history
