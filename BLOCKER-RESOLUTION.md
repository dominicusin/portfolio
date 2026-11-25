# Blockers — resolution options (evidence-based)

Probe: `python3 automation/check_blockers.py`. It performs only read-only checks and prints no secrets.

## 1. Host `192.168.1.2` (INF-003/004/005, FTN-001…004)

**Verified:** ICMP reply and SSH key auth both work (`dietpi@192.168.1.2`, `/bin/bash -c` wrapper). Services `qico`, `inn2`, `jamnntpd`, `cups`, `cron` are running. Remote user's fish shell sources a broken line in `/etc/fish/conf.d/dietpi.fish` — cosmetic noise, not an auth failure.

**Resolution paths:**
1. Use `ssh -o BatchMode=yes dietpi@192.168.1.2 'bash -c "<read-only command>"'` for audits. Already possible.
2. Remove/comment the invalid `(( $G_HW_MODEL > 9 )) || alias ...` line in the remote fish config (requires sudo on host) to remove stderr noise.
3. Install `ansible-playbook` in a local venv and run `make check` with a vault password supplied locally (not in chat) for INF-003. An idempotency proof must be two consecutive `--check` runs with identical `changed=0`.
4. INF-005 restore drill: copy backups to an isolated target, verify checksums and one FTN/JAM record; only then approve JAM `DW`, `sqpack`/`hpucode` cron or `areastat` changes.

## 2. GitHub token scope / archived-fork alerts (SEC-002)

**Verified:** token scopes are `gist`, `read:org`, `repo`, `workflow` — no `admin:repo_hook`, no `admin:org`.

**Resolution paths:**
1. Interactive terminal: `gh auth refresh -h github.com -s delete_repo` (adds the missing scope for the current API). Then re-run dismissal with `dismissed_reason: not_used` only.
2. Enable delegated alert dismissal for the target repositories, or use a fine-grained PAT/GitHub App with `Dependabot alerts: write` and `Administration: write`, stored via `hermes-vault add` and read through the vault injector. Preferred for scheduled automation.
3. For archived repos, an even simpler path is to let GitHub archive-state policies handle alerts: document accepted risk in `SEC-002-triage.md` if the token cannot be upgraded. Do not mark alerts as false positives.

## 3. Private `Linux-Serv-Ansible` branch protection (SEC-001 residual)

**Verified:** `PUT /branches/main/protection` returns 403 "Upgrade to GitHub Pro or make this repository public".

**Resolution paths:**
1. Upgrade the account/org plan, then re-run the protection API call.
2. Make the repository public (owner decision; it contains infrastructure code).
3. Use an external CI gate as compensating control: the `CI` workflow is green on main; add a documented review checklist until protection is available.

## 4. Vault passphrase (not on the critical path)

**Verified:** `hermes-vault status` prompts for a passphrase; no passphrase was provided and none is requested in chat.

**Resolution paths:**
1. Unlock locally, then run `automation/set-gitleaks-secret.py` (reads from injected env or vaultknox, never prints the value).
2. Use the desktop bridge/keyring if configured for the profile.
3. No CI action is required: Surypus security scan now uses `GITHUB_TOKEN`, and the environment secret already exists in `dominicusin/portfolio`.

## 5. PostgreSQL / live CMS for SUR-005/006/008 and NEO-004

**Verified:** no local `docker`/`postgres` server binary; `psql` client is present; no CMS host was supplied.

**Resolution paths:**
1. Add a GitHub Actions job with `services: postgres:16`, run an RLS policy migration and a two-tenant cross-access test there. No local server needed.
2. Provide a staging CMS host for NEO-004; CI/deploy are already separated and template validation is enforced.
3. For SUR-006/008, run DB-backed integration specs in the same service container before marking them DONE.

## Priority

1. Token scope refresh (unblocks SEC-002).
2. Host read-only audit with `bash -c` + ansible venv (unblocks INF-003/005 evidence).
3. GitHub Actions postgres service (unblocks SUR-005/006/008 without host changes).
4. Vault/plan/public decisions are owner-level and do not block the current green CI state.
