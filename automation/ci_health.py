#!/usr/bin/env python3
"""Report latest CI conclusions for the seven core repositories."""
import json, os, subprocess, collections, argparse, datetime
CORE = ["surypus/surypus", "dominicusin/uaw", "neoallunity/integral-philosophy",
        "neoallunity/allunity-wagtail", "dominicusin/dominicusin.github.io",
        "dominicusin/Linux-Serv-Ansible", "dominicusin/package-maximizer"]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def gh(args):
    p = subprocess.run(["gh"] + args, capture_output=True, text=True, timeout=120)
    return p.stdout if p.returncode == 0 else "[]"
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--write", action="store_true"); a = ap.parse_args()
    rows = []
    for repo in CORE:
        raw = gh(["run", "list", "--repo", repo, "--limit", "20",
                  "--json", "name,conclusion,status,createdAt"])
        try: runs = json.loads(raw)
        except Exception: runs = []
        c = collections.Counter((r.get("conclusion") or r.get("status")) for r in runs)
        rows.append({"repo": repo, "runs": len(runs), "summary": dict(c),
                     "latest": (runs[0]["createdAt"][:10] if runs else "no runs")})
    md = ["# CI health", "", "| Repository | Runs | Conclusions | Latest |", "|---|---:|---|---|"]
    for r in rows:
        md.append(f"| `{r['repo']}` | {r['runs']} | {r['summary']} | {r['latest']} |")
    text = "\n".join(md) + "\n"
    if a.write:
        with open(os.path.join(ROOT, "STATUS.md"), "w") as fh: fh.write(text)
    print(text)
if __name__ == "__main__":
    main()
