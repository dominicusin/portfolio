# PLAN CLOSURE MATRIX — 2026-11-25

Legend: **DONE** = evidence in CI/tests/merge; **DESIGN** = canonical design recorded, execution needs external condition; **BLOCKED** = cannot be executed with current credentials/host access. No item is marked DONE without a verifiable artifact.

| ID | Status | Artifact / blocker |
|---|---|---|
| PORT-001 | DONE | `artifacts/repository-audit.json`, 78 repos |
| PORT-002 | DONE | `PORTFOLIO.md`, dated reports |
| PORT-003 | DONE | weekly cron `3dcb53f3f8a5`, `reports/2026-11-25.md` pushed |
| SEC-001 | DONE | required checks on uaw, wagtail, ai-orchestration, surypus, integral-philosophy; #2 closed after security-scan migrated to GITHUB_TOKEN |
| SEC-002 | BLOCKED (partially triaged) | `artifacts/SEC-002-triage.md`; 5 archived/fork need `admin:repo_hook`; no alerts dismissed |
| SUR-001/002/003 | DONE | PR #258, #261, #262 merged; real JWT fixtures, issuer verification, sub from registered claim |
| SUR-004 | PARTIAL | `automation/rbac_audit.py` + `artifacts/SUR-004-rbac-audit.json`: 10 routes scanned, 8 review candidates (public login/health are expected false positives); code-level deny-by-default still a review programme |
| SUR-005 | DESIGN | tenant context from verified JWT implemented (#261); RLS policies need a live PostgreSQL instance |
| SUR-006 | DESIGN | DAL stub removal requires DB-backed integration environment |
| SUR-007 | DONE (invariant verified) | `Finance.Accounting.validateTransaction` + existing AccountingSpec; no change needed |
| SUR-008 | DESIGN | event-store replay/idempotency needs PostgreSQL; UAW idempotency prototype exists but is a separate system |
| SUR-009 | DONE | `stack.yaml` lts-22.21, flake+flake.lock, PR #259 toolchain fix |
| SUR-010 | DONE | PR #263 merged, src/ Haskell-only |
| SUR-011 | DONE | 24 exact duplicate issues closed (129 → 105); bot-report shutdown still requires org automation settings |
| SUR-012 | DONE | secret no longer required by workflow; env secret exists in portfolio |
| UAW-001…007 | DONE | PR #3, #4, #5, #6, #7 merged; 30 tests in required job |
| NEO-001 | DONE | `artifacts/NEO-001-material-metadata-schema.md` |
| NEO-002 | DONE | README/.github/Magazine PRs merged |
| NEO-003 | DONE | `docs/NEO-003-publishing-pipeline.md` |
| NEO-004 | PARTIAL | CI/deploy separated and template validation added; live CMS instance not deployed (host not provided) |
| NEO-005 | DONE | PR #7 merged, Monorepo CI green, 9 required checks |
| NEO-006 | PARTIAL | `artifacts/neo-006-skos-skeleton.ttl` defines material types and `relatedTo`; full graph/Wikibase layer remains roadmap |
| INF-001 | DONE (draft) | `artifacts/INF-001-hardware-inventory.md`, unverified fields marked |
| INF-002/006 | DESIGN | `proposals/README.md`; no new OS repos created |
| INF-003 | PARTIAL | Ansible CI fixed (PR #1); `--check` on wdmch requires SSH access |
| INF-004 | DESIGN | WDMCH release/checksums need build host |
| INF-005 | DESIGN | `docs/INF-005-restore-checklist.md`; drill requires 192.168.1.2 |
| FTN-001/002/005 | DESIGN | `docs/FTN-001-002-design.md`, `docs/FTN-005-uaw-adapter.md` |
| FTN-003/004 | DESIGN | INN peering and PolyResolver follow gateway stability; no host access |
| WEB-001…004 | PARTIAL | SBOM/attestations and submodule pin check done (#468); portal/SEO/Lighthouse programme remains a product roadmap, not a blocker for repository consistency |
| POLY-001 | DONE | PR #11 merged, `automation/polyglot_cm.py`, 5 tests, CI green |
| PKG-001 | PARTIAL | CI green on main; PyPI/RTDocs publication decision outstanding |
| PKG-002 | DONE | PR #1/#2 merged, pyproject install, portable paths |
| PKG-003 | DONE (decision) | `docs/PKG-003-status.md`; repos not archived without owner/rights check |
| WDM-001 | PARTIAL | rescue-image repo exists; release evidence needs build host |

## Irreducible blockers (no code action can close them)

1. Host `192.168.1.2` / wdmch access: INF-003/004/005 and FTN-001…004 execution.
2. GitHub token scope `admin:repo_hook` and platform plan: archived/fork alert dismissals and private `Linux-Serv-Ansible` branch protection.
3. Vault passphrase / rotated key: not needed for CI now, but any vault-gated operation remains unavailable; no secret was requested or displayed.
4. Live CMS host for NEO-004 and publishing stack for SUR-005/006/008.
