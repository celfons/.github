# Aikido — Tool Interpretation Guide

This document defines how agents must interpret findings produced by Aikido SAST scans.

---

## What Aikido Provides

Aikido performs static analysis on source code and produces findings that include:

- **Rule ID** — the vulnerability class (e.g., `sql-injection`, `xss`, `rce`)
- **File path** — the source file where the finding was detected
- **Line number** — the specific line flagged
- **Snippet** — the code fragment that triggered the rule
- **Severity** — the scanner's risk classification (informational only)

This information is delivered as the raw issue body when GitHub issues are created via the API.

---

## What Agents Must Infer

Agents may infer only what is explicitly present in the Aikido finding:

- The affected file and line
- The specific code pattern that was flagged
- The vulnerability class, mapped to the corresponding rule in `SECURITY/RULES/`

---

## What Agents Must Not Infer

Agents must not:

- Assume the vulnerability is exploitable without reading the code
- Expand the scope of the fix beyond the flagged location without explicit evidence
- Trust the severity rating as a proxy for fix urgency or approach
- Assume that similar-looking code elsewhere is also vulnerable
- Skip reading the applicable rule because the finding "looks obvious"

---

## Mapping Aikido Rules to Organization Rules

| Aikido Rule ID | Organization Rule File |
|---|---|
| `sql-injection` | [`SECURITY/RULES/SAST-SQLI.md`](../RULES/SAST-SQLI.md) |
| `xss` | [`SECURITY/RULES/SAST-XSS.md`](../RULES/SAST-XSS.md) |
| `rce` | [`SECURITY/RULES/SAST-RCE.md`](../RULES/SAST-RCE.md) |

If the Aikido rule ID does not map to an existing rule, the agent must stop and open a PR
to this repository proposing a new rule before proceeding with any code change.

---

## Severity Guidance

Aikido severity levels are **informational**. They do not determine:

- Fix priority (that is determined by the organization's triage process)
- Fix approach (that is determined by the rule in `SECURITY/RULES/`)
- Whether to fix (that is determined by the `agent:ready` label)
