# FTN-001/002 — Gateway stability and routing model (design, not applied)

Host-specific facts that MUST NOT be changed casually (wdmch, 192.168.1.2):

- JAM base timestamps use `DW = unixtime - 10368000`. `jamfix` rolls raw timestamps back from hpt; do not alter this offset.
- `areastat` is patched with `mtime += 10368000`.
- `sqpack -p 365 -$m 5000` runs Sundays 05:30; `hpucode` UUE → TIC → htick → FileArea runs 05:45.
- `hptsqfix` is for Squish only; do not apply it to JAM areas.

## Addressing and queues

One canonical address record: `zone:net/node.point@domain`, stored in Git as YAML with an owner and a status (`active`, `paused`, `retired`). Inbound and outbound queues are separate directories with file locks; a message is moved to `processed/` only after the downstream accept is recorded.

## Retry and dead-letter

- attempt counter and `next_attempt` stored in the queue entry;
- exponential backoff 5m → 25m → 125m, max 5 attempts;
- after max attempts, move to `dead-letter/` with reason and original envelope;
- delivery confirmation writes a receipt keyed by message-id (dedupe key).

## Prohibited changes without a restore test

Any change to JAM timestamps, sqpack/hpucode cron, or areastat patching requires the INF-005 restore drill first.
