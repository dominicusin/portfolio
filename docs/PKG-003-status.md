# PKG-003 — Status decision for R&D Haskell repos

| Repository | Status | Evidence / next action |
|---|---|---|
| `dominicusin/polyresolver` | Phase 0 spec, honest status | README points at a foreign fork and LICENSE is 8 bytes — rewrite README with local status and spec-only scope |
| `dominicusin/MessageGateway` | experimental skeleton | 3 Haskell files, no runnable service; keep as `status: experiment` until a transport spec exists |

Decision rule: one repository, one status, one CI state. A repository that cannot run a real build must say so in its README rather than show a green but empty workflow.

No repository was archived in this change: archiving is irreversible from the UI and needs an explicit content-rights/owner check.
