#!/usr/bin/env python3
"""Set GITLEAKS_LICENSE in surypus/surypus from the Hermes vault.

The secret value is never printed and never written to a file. Rotate the key
first if it was ever pasted into chat, then store it in the vault:

    hermes-vault add --id gitleaks_license --type api_key \
      --label "Gitleaks GitHub Action license" \
      --data '{"value":"<KEY>"}'

Then run: python automation/set-gitleaks-secret.py
"""
import os
import subprocess

SECRET_ID = "GITLEAKS_LICENSE"
REPO = "surypus/surypus"

def main():
    try:
        from vaultknox import AutonomousSecretsStore
    except ImportError as exc:
        raise SystemExit("vaultknox is unavailable in this environment: %s" % exc)
    value = os.environ.get(SECRET_ID)
    if not value:
        try:
            store = AutonomousSecretsStore()
            value = store.get(SECRET_ID)
        except Exception as exc:
            raise SystemExit("vault unavailable: %s" % exc)
    if not value:
        raise SystemExit("secret %s not found in vault" % SECRET_ID)
    result = subprocess.run(
        ["gh", "secret", "set", SECRET_ID, "--repo", REPO],
        input=value.encode("utf-8"),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise SystemExit("gh secret set failed: %s" % result.stderr.decode(errors="replace"))
    print("GITLEAKS_LICENSE installed in %s (value not shown)" % REPO)

if __name__ == "__main__":
    main()
