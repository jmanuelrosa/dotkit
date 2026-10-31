# Security policy

## Reporting a vulnerability

Report vulnerabilities privately through [GitHub's private vulnerability reporting](https://github.com/jmanuelrosa/dotkit/security/advisories/new), not in a public issue.

Include what is affected (`ui.py`, `colors.py` or `bin/dotkit-vendor`), how to reproduce it, and the impact you expect.

## Scope

Consumers vendor copies of these modules, so a fix lands here first and reaches each consumer when it re-runs `bin/dotkit-vendor`.
