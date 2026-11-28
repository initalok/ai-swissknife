# Security Policy

## Scope
This policy covers:
1. Vulnerabilities in the `src/swissknife/` CLI, managed-block syncer, or GitHub Actions workflows.
2. Compromised, malicious, or credential-exfiltrating external links/packages referenced in `catalog/registry/*.yaml`.

## Reporting a Vulnerability
Please **do not** open a public GitHub Issue for security vulnerabilities or compromised upstream links.

Use GitHub's **Private Vulnerability Reporting** under the repository's **Security → Advisories → Report a vulnerability** tab. Include:
- The affected file, entry ID, or workflow.
- Reproduction steps or primary-source evidence of the risk.

## Response Expectations
This is a solo-maintained repository. Reports are reviewed on a best-effort basis, typically within 72 hours. Confirmed compromised links are immediately removed or quarantined into `retired` and excluded from `llms.txt`.
