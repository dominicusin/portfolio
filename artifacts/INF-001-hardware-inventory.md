# INF-001 — Hardware / host inventory (draft)

Evidence levels: **verified** = host fact used in working configs; **from audit** = repository metadata; **unverified** = needs a live check.

| Host | Role | OS / arch | Storage / boot | Evidence |
|---|---|---|---|---|
| `192.168.1.2` (`wdmch.lan`) | FidoNet point, printing, backups | Debian 13 ARM64 (DietPi) | WD My Cloud Home, RTD1295; rescue image from `alpine-wdmch-builder` | verified (ansible user `dietpi`) |
| Quasar | AI/GPU workstation | Linux, x86_64 | i9-9820X, GTX 1050 Ti (sm_61), 188 GB RAM | verified (`strata` build notes) |
| AllUnity host | CMS/publishing | unknown | Wagtail stack in `allunity-wagtail` | unverified |
| Personal site | GitHub Pages | n/a | `dominicusin.github.io` | from audit |

Do not add new hosts without an owner and a restore procedure (INF-005).
