# FTN-005 — UAW adapter design

The adapter wraps the FTN gateway for UAW-004 capability discovery and UAW-005 policy checks.

| Operation | Kind | Policy level | Approval |
|---|---|---|---|
| `ftn.status` | read | L0 | no |
| `ftn.queue.list` | read | L0 | no |
| `ftn.message.retry` | send | L3 | yes |
| `ftn.message.delete` | delete | L4 | yes |

`is_available()` must return false when the gateway host is unreachable; the capability probe then reports a named reason instead of attempting a send. Dry-run evaluates all steps without touching the queue.
