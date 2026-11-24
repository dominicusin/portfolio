#!/usr/bin/env python3
"""Find (and optionally close) duplicate open issues by normalized title."""
import json, os, re, subprocess, sys, argparse

def gh(args):
    p = subprocess.run(["gh"] + args, capture_output=True, text=True, timeout=120)
    return p.stdout if p.returncode == 0 else ""
def norm(t):
    t = t.lower().strip(); t = re.sub(r"^#?\d+[:.) ]*", "", t)
    return " ".join(re.sub(r"[^a-zа-яё0-9 ]+", " ", t).split())
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--close", action="store_true", help="close duplicates, keep lowest issue number")
    a = ap.parse_args()
    raw = gh(["issue", "list", "--repo", a.repo, "--state", "open", "--limit", "200",
              "--json", "number,title"])
    items = json.loads(raw) if raw.strip() else []
    groups = {}
    for it in items: groups.setdefault(norm(it["title"]), []).append(it["number"])
    dups = [sorted(set(v)) for v in groups.values() if len(set(v)) > 1]
    print(f"{a.repo}: {len(items)} open issues, {len(dups)} duplicate groups")
    for nums in dups:
        keep = min(nums)
        others = [n for n in nums if n != keep]
        print(f"  keep #{keep}, duplicates: {others}")
        if a.close:
            for n in others:
                gh(["api", f"repos/{a.repo}/issues/{n}/comments", "-f",
                    f"body=D duplicate of #{keep} (normalized-title match). Closed by portfolio dedup automation."])
                gh(["api", f"repos/{a.repo}/issues/{n}", "--method", "PATCH",
                    "-f", "state=closed", "-f", "state_reason=not_planned",
                    "-f", "labels[]=duplicate"])
if __name__ == "__main__": main()
