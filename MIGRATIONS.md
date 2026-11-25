# Migration and PR plan (prepared 2026-11-25, nothing deleted)

All migrations are additive or documentation-only. Source repositories remain intact; no archive, transfer, deletion, content removal or license assignment is performed here.

| # | Target repo | Change | Type | Status |
|---|---|---|---|---|
| M-01 | `neoallunity/README` | Replace links to 8 archived `integral-philosophy-*` modules with canonical `neoallunity/integral-philosophy` | docs migration | PR #1 merged |
| M-02 | `dominicusin/uaw` | Add `INTEGRATIONS.md` with real/mock/unsupported matrix from `artifacts/UAW-001-integrations.md` | docs, no code change | PR #2 merged |
| M-03 | `neoallunity/allunity-{diskussii,knigi,zhurnaly}` | Add README stating provenance, rights=UNKNOWN and read-only status; no license | docs, non-destructive | PR #1 merged in all three mirrors |
| M-04 | `dominicusin/portfolio` | Publish fresh audit, maturity matrix and three evidence reports | artifacts | done in this cycle |
| M-05 | `surypus/surypus` | Keep the already merged security/CI fixes; no further repository move | no-op | done |
| M-06 | future | Move bulk media out of git history only after rights decision and bundle backup | deferred | blocked by ALL-001 owner decision |

Rollback for every PR: revert the merge commit; no data was removed, so restoration is trivial.
