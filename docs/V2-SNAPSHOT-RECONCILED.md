# Reconciliation: pasted v2 snapshot vs live state (25.11, final)

The pasted v2 document is a valid historical snapshot but is stale. Live verification results:

| Pasted item | Live status | Evidence |
|---|---|---|
| Surypus PR #258/#259 waiting, main build broken (issues #8/#9) | DONE | #258/#259/#261/#262/#263/#264 merged; issues #8/#9 CLOSED; all check runs on current main success |
| Tenant/JWT negative tests pending (issue #1) | DONE | issue #1 CLOSED; real HS256 fixtures, issuer check, registered `sub` parsing |
| GITLEAKS_LICENSE issue #2 | DONE | issue #2 CLOSED; security scan uses `GITHUB_TOKEN`; env secret exists in portfolio |
| UAW-001 JSON state (issue #3 context) | DONE | PR #3 merged: SQLite/WAL, crash tests; UAW-004…007 merged too |
| Wagtail template/license (issue #4) | DONE | issue #4 CLOSED; deterministic template validator in CI |
| Monorepo CI not required / pip-Dependabot red | DONE | PR #7 merged, Monorepo CI green on main, 9 required checks |
| Hardware inventory INF-001 | DONE (draft) | `artifacts/INF-001-hardware-inventory.md` |
| Docker bugs in Compose | DONE | PR #264: PORT=8080, 8080:8080, worker removed; review verdict in `docs/SUR-DOCKER-REVIEW.md` |
| SEC-002 870/133 alerts | PARTIAL | `artifacts/SEC-002-triage.md`; dismissal API now needs `delete_repo` + delegated dismissal (see `BLOCKER-RESOLUTION.md`) |
| WEB-005 Vercel/CircleCI | OPEN | external service configuration, no repo change can close it |
| NEO-007 media rights | OPEN | owner decision |
| Private Ansible branch protection | OPEN | issue #10: platform plan/public-repo decision |

## Current CI snapshot

Latest main runs: uaw, integral-philosophy, allunity-wagtail, personal site, Linux-Serv-Ansible, package-maximizer, ai-orchestration-platform — all success. Surypus current main: all check runs success, no failures.

## Definition of Done applied

No item is marked DONE on the basis of the pasted text alone. Each DONE requires a merged PR, a green required check, a test result or a verified API response, as recorded in `PLAN-CLOSURE.md`.
