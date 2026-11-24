#!/usr/bin/env python3
"""Generate a weekly portfolio report (no issue spam)."""
import datetime, json, os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def run(args):
    p = subprocess.run(args, capture_output=True, text=True, timeout=180)
    return p.stdout if p.returncode == 0 else ""
def main():
    today = datetime.date.today().isoformat()
    audit_path = os.path.join(ROOT, "artifacts", "repository-audit.json")
    repos = json.load(open(audit_path)) if os.path.exists(audit_path) else []
    alerts = sum(r.get("open_dependabot_alerts") or 0 for r in repos)
    protected = sum(1 for r in repos if r.get("protected"))
    out = [
        f"# Portfolio weekly report — {today}", "",
        f"- Repositories audited: {len(repos)}",
        f"- Branch-protected: {protected}",
        f"- Open Dependabot alerts (cap 100/repo): {alerts}",
        "- Unverified items: see RISKS.md (status BLOCKED)", "",
        "## CI health", "", "Run `python automation/ci_health.py` for the core table.", "",
        "## Recommended actions", "",
        "1. Keep P0 on Surypus auth/tenant fixes and green required CI.",
        "2. Triage security alerts in active repositories first.",
        "3. Do not create new repos without a system and status.",
    ]
    path = os.path.join(ROOT, "reports", f"{today}.md")
    with open(path, "w") as fh: fh.write("\n".join(out) + "\n")
    print(path)
if __name__ == "__main__": main()
