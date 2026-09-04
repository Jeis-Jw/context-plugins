# Security policy

## Reporting a vulnerability

Please report suspected vulnerabilities through [GitHub private vulnerability reporting](https://github.com/Jeis-Jw/context-plugins/security/advisories/new). Do not disclose exploit details, private repository paths, credentials, pending receipts, or user context in a public issue.

Security-sensitive areas include vault path containment, approval and lifecycle binding, runtime identity, CAS and lock enforcement, atomic writes and rollback, symlink handling, and protection against applying altered or replayed frozen material.

Include the affected plugin and version, host, Python version, a minimal reproduction, expected and actual behavior, and redacted diagnostic output. Remove secrets, usernames, home-directory paths, repository paths, and other local identifiers.

The project is a developer preview. Only the latest published release set receives security fixes; older previews may require upgrading. Acknowledgement and remediation timing depend on severity and maintainer availability, so no fixed response-time guarantee is made.
