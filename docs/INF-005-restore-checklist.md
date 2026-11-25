# INF-005 — Backup/restore drill checklist

Secrets stay outside repositories (vault or GitHub Secrets); backups contain no credentials.

1. Snapshot: list hosts, services, data paths and the last successful backup timestamp.
2. Restore into an isolated target (never over production): configuration, message bases, database dumps.
3. Verify: checksum comparison, service start, one read query per database, one FTN message reconstructed from backup.
4. Record: date, operator, target, checksums, failures, and the exact command sequence.
5. Only after a green drill may JAM/sqpack/hpucode/areastat changes proceed (see FTN docs).

Status: procedure defined; execution requires access to 192.168.1.2 and is not yet evidenced.
