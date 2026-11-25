#!/usr/bin/env python3
"""Read-only probe of the remaining plan blockers; prints actions, never secrets."""
import json
import shutil
import subprocess


def run(cmd, timeout=25, stdin=None):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, stdin=stdin)
        return p.returncode, (p.stdout or p.stderr).strip()
    except Exception as exc:
        return -1, str(exc)


def ssh_probe():
    cmd = ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=6",
           "dietpi@192.168.1.2", 'bash -c "echo HOST_OK; hostname"']
    rc, out = run(cmd)
    return {"reachable": "HOST_OK" in out, "output": out[:200], "rc": rc}


def gh_scopes():
    rc, out = run(["gh", "auth", "status"])
    line = next((l for l in out.splitlines() if "Token scopes" in l), "")
    import re
    tail = line.split("scopes:", 1)[-1]
    scopes = ",".join(re.findall(r"'([^']+)'", tail))
    return {"scopes": scopes,
            "has_admin_repo_hook": "admin:repo_hook" in scopes,
            "has_admin_org": "admin:org" in scopes}


def tooling():
    return {name: bool(shutil.which(name)) for name in ("docker", "psql", "postgres", "ansible-playbook")}


def vault():
    rc, out = run(["hermes-vault", "--no-banner", "status"], timeout=20,
                  stdin=subprocess.DEVNULL)
    return {"locked": "passphrase" in out.lower() or rc != 0, "hint": out[:180]}


def main():
    result = {"ssh_wdmch": ssh_probe(), "github_token": gh_scopes(),
              "local_tooling": tooling(), "vault": vault()}
    result["actions"] = []
    if result["ssh_wdmch"]["reachable"]:
        result["actions"].append("SSH key auth works: use `bash -c` wrapper for remote commands; fix /etc/fish/conf.d/dietpi.fish line 22 to remove startup noise.")
    else:
        result["actions"].append("SSH key auth failed: add the agent public key to dietpi@192.168.1.2 ~/.ssh/authorized_keys.")
    if not result["github_token"]["has_admin_repo_hook"]:
        result["actions"].append("Run `gh auth refresh -h github.com -s admin:repo_hook -s admin:org` in an interactive terminal (no secret pasting).")
    if not result["local_tooling"]["docker"] and not result["local_tooling"]["postgres"]:
        result["actions"].append("Use GitHub Actions `services: postgres:16` for DB tests instead of a local server.")
    if result["vault"]["locked"]:
        result["actions"].append("Vault is locked: unlock locally; CI no longer needs the key, so this is not on the critical path.")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
