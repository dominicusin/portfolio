# CURRENT-STATE — corrections to v2 planning documents (2026-11-25)

The two v2 documents circulating in chat are already stale. Canonical live facts:

| Claim in v2 docs | Live state | Evidence |
|---|---|---|
| 78 repositories (51+6+21) | **79** (52 user + 6 surypus + 21 neoallunity; 58 public + 21 private) | `artifacts/repository-audit-generated.json` |
| PR `surypus/surypus#259` open | **MERGED** 2026-11-25T00:38:46Z | `gh pr view 259` |
| Main build broken / issues #8, #9 open | **CI success**, main run `45519684668`; #8, #9 closed | `artifacts/SUR-001-build-evidence.md` |
| Issue #1 (tenant stubs) open | **CLOSED** (removed in PR #258, CI verified) | portfolio issue #1 |
| Issue #3 (fidonet regressions) open | **CLOSED** (Linux-Serv-Ansible PR #1 merged, CI success) | portfolio issue #3 |
| 129 → 105 issues | still 105 open | `automation/dedup_issues.py` |
| Surypus tests 792/798 | **1188 examples, 0 failures, 4 pending** in real CI | main run log |
| UAW has 3 live integrations | Linear/Notion/Box/DocLib are mocks; GitHub requires absent external module | `artifacts/UAW-001-integrations.md` |
| Media mirrors: rights unknown | confirmed; READMEs added with rights=UNKNOWN, 3 PRs merged | `artifacts/ALL-001-provenance.md` |

Open portfolio issues now: #2 (gitleaks secret), #5 (media rights — owner decision), #6 (Vercel/CircleCI), #7 (alert triage blocked by missing `admin:repo_hook` scope).

Everything else in the first execution cycle (PORT-001, PORT-002, SUR-001, UAW-001, ALL-001, non-destructive migration PRs) is complete; see `reports/2026-11-25-cycle2.md` and `MIGRATIONS.md`.
