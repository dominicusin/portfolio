#!/usr/bin/env python3
"""SUR-004 advisory audit: find API routes with no permission check nearby.

This is a static heuristic, not a proof of safety. It produces evidence for a
manual review and fails only when a route has neither a permission call nor an
explicit public-path annotation within the lookahead window.
"""
import json
import re
import sys
from pathlib import Path

ROUTE = re.compile(r'"(/api/[^"]+)"')
GUARD = re.compile(r'(requirePermission|checkPermission|authorize|publicPaths|publicPath)', re.I)


def audit_file(path: Path, lookahead: int = 20):
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    findings = []
    for i, line in enumerate(lines):
        for route in ROUTE.findall(line):
            window = "\n".join(lines[i + 1:i + 1 + lookahead])
            guarded = bool(GUARD.search(line) or GUARD.search(window))
            findings.append({"route": route, "file": str(path), "line": i + 1,
                             "guarded": guarded})
    return findings


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    files = list(root.rglob("*.hs"))
    findings = []
    for f in files:
        findings.extend(audit_file(f))
    unguarded = [f for f in findings if not f["guarded"]]
    out = {"routes": findings, "unguarded": unguarded,
           "total": len(findings), "unguarded_count": len(unguarded)}
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
