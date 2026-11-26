# Surypus open issues — triage after verified closure pass

Snapshot saved before closure: `artifacts/surypus-issues-before-bulk-close.json` (105 issues).
Closed with evidence: #243, #210, #183, #224, #226, #198, #177, #66, and 7 bot reports (#257, #255, #253, #251, #248, #146, #145).
Remaining open: **89**. These are distinct product tasks, not duplicates; marking them DONE without implementation would violate the DoD rule.

| Category | Count | Why not closed |
|---|---:|---|
| DB / event store / read models | 26 | needs a real PostgreSQL test database and migration runner |
| API / UI / transport | 21 | needs frontend/transport implementation and contract tests |
| Other product work | 13 | needs product decisions or host access |
| Domain modules | 12 | needs domain code and invariant tests |
| Auth / RBAC | 11 | needs endpoint-by-endpoint handler changes plus review |
| Testing / infra | 6 | needs CI/live infrastructure changes |

Top remaining IDs by category:

- **Other product work**: #246, #242, #225, #213, #194, #174, #156, #153, #150, #149, #140, #70 …
- **API / UI / transport**: #245, #241, #238, #228, #227, #221, #212, #211, #203, #202, #201, #197 …
- **Domain modules**: #240, #218, #217, #208, #200, #199, #161, #160, #159, #158, #139, #68
- **DB / event store / read models**: #239, #237, #236, #235, #234, #231, #230, #214, #190, #188, #187, #178 …
- **Testing / infra**: #233, #229, #223, #196, #189, #72
- **Auth / RBAC**: #232, #209, #192, #181, #171, #165, #164, #157, #63, #62, #60

Next executable slice: add a GitHub Actions `services: postgres:16` job, then implement the DB-backed DAL/read-model issues in that environment; no host access is required for this path.
