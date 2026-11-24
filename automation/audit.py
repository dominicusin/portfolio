#!/usr/bin/env python3
"""Rebuild the full GitHub inventory using the gh CLI (no token in code)."""
import json, subprocess, datetime, os, re, concurrent.futures

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCOPES = [("user", ["api", "user/repos?per_page=100&affiliation=owner", "--paginate"]),
          ("surypus", ["api", "orgs/surypus/repos?per_page=100", "--paginate"]),
          ("neoallunity", ["api", "orgs/neoallunity/repos?per_page=100", "--paginate"])]

def gh(args):
    p = subprocess.run(["gh"] + args, capture_output=True, text=True, timeout=120)
    return p.stdout if p.returncode == 0 else ""

def main():
    repos = []
    for org, args in SCOPES:
        items = gh(args + ["--jq", ".[]"]).strip()
        for line in items.splitlines():
            try:
                r = json.loads(line)
            except Exception:
                continue
            repos.append((org, r))
    since = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=90)).strftime("%Y-%m-%dT%H:%M:%SZ")
    def one(*a): return gh(["api"] + list(a)).strip()
    def enrich(pair):
        org, r = pair
        fn = r["full_name"]
        branches = one(f"repos/{fn}/branches", "--paginate", "--jq", ".[].name")
        protected = subprocess.run(["gh", "api", f"repos/{fn}/branches/{r['default_branch']}/protection"],
                                   capture_output=True, text=True).returncode == 0
        commits = one(f"repos/{fn}/commits?since={since}&per_page=100", "--jq", "length")
        alerts = one(f"repos/{fn}/dependabot/alerts?state=open&per_page=100", "--jq", "length")
        return {"repo": fn, "org": org, "full_name": fn, "visibility": r.get("visibility"),
                "language": r.get("language"), "size_kb": r.get("size"), "updated_at": r.get("updated_at"),
                "archived": r.get("archived"), "fork": r.get("fork"), "description": r.get("description"),
                "license": (r.get("license") or {}).get("spdx_id"), "open_issues_count": r.get("open_issues_count"),
                "branch_count": len([x for x in branches.splitlines() if x]), "protected": protected,
                "commits_90d_cap100": int(commits) if commits.isdigit() else None,
                "open_dependabot_alerts": int(alerts) if alerts.isdigit() else None}
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        data = list(ex.map(enrich, repos))
    out = os.path.join(ROOT, "artifacts", "repository-audit-generated.json")
    with open(out, "w") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
    print(f"audited {len(data)} repos -> {out}")

if __name__ == "__main__":
    main()
