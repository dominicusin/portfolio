#!/usr/bin/env python3
"""Refresh the portfolio audit and publish a dated weekly report (no issue spam)."""
import datetime
import os
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def run(args, check=False):
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=900)
    if check and proc.returncode != 0:
        raise SystemExit("failed: %s\n%s" % (" ".join(args), proc.stderr[-500:]))
    return proc.stdout.strip()


def git(*args):
    return run(["git", *args])


def main():
    today = datetime.date.today().isoformat()
    run(["python3", "automation/audit.py"], check=True)
    run(["python3", "automation/ci_health.py", "--write"], check=True)

    import json
    audit_path = os.path.join(ROOT, "artifacts", "repository-audit.json")
    repos = json.load(open(audit_path, encoding="utf-8")) if os.path.exists(audit_path) else []
    alerts = sum((r.get("open_dependabot_alerts") or 0) for r in repos)
    protected = sum(1 for r in repos if r.get("protected"))
    active = sum(1 for r in repos if (r.get("commits_90d_cap100") or 0) > 0)

    ci_path = os.path.join(ROOT, "STATUS.md")
    ci_note = "Run `python3 automation/ci_health.py` for the live table."
    if os.path.exists(ci_path):
        lines = [l for l in open(ci_path, encoding="utf-8").read().splitlines()
                 if l.strip().startswith("|") or l.strip().startswith("-")]
        if lines:
            ci_note = "Snapshot from `STATUS.md`:\n\n" + "\n".join(lines[:20])

    report = "\n".join([
        "# Portfolio weekly report — " + today, "",
        "- Repositories audited: %d" % len(repos),
        "- Active in last 90 days: %d" % active,
        "- Branch-protected: %d" % protected,
        "- Open Dependabot alerts (cap 100/repo): %d" % alerts,
        "", "## CI health", "", ci_note, "",
        "## Recommended actions", "",
        "1. Keep P0 on Surypus auth/tenant fixes and green required CI.",
        "2. Triage security alerts in active repositories first.",
        "3. Do not create new repositories without a system and status.",
        "", "Unverified items: see `RISKS.md` (status BLOCKED).", "",
    ])
    os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
    path = os.path.join(ROOT, "reports", today + ".md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(report)
    git("add", "artifacts", "reports", "STATUS.md")
    status = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT)
    if status.returncode != 0:
        git("-c", "user.name=dominicusin",
            "-c", "user.email=dominicusin@users.noreply.github.com",
            "commit", "-q", "-m", "chore: weekly portfolio report " + today)
        git("push", "-q", "origin", "HEAD")
    print(path)


if __name__ == "__main__":
    main()
