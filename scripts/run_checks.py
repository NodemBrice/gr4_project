#!/usr/bin/env python3
"""
Run project static checks and tests, write a JSON report.

Usage:
    python scripts/run_checks.py --output report.json
"""

from __future__ import annotations
import subprocess
import json
import sys
import argparse
import shlex
from typing import List, Dict, Any
import os

CHECKS: List[Dict[str, Any]] = [
    {"name": "mypy", "cmd": "mypy --strict backend"},
    {"name": "pylint", "cmd": "pylint backend --output-format=text"},
    {"name": "py_compile", "cmd": "python -m py_compile backend/*.py"},
    {"name": "pytest", "cmd": "pytest -q"},
]

def run_cmd(cmd: str, timeout: int = 300) -> Dict[str, Any]:
    print(f"Running: {cmd}")
    try:
        # Split cmd for security
        cmd_list = shlex.split(cmd)
        proc = subprocess.run(cmd_list, capture_output=True, text=True, timeout=timeout)
        return {"returncode": proc.returncode, "output": (proc.stdout or "") + (proc.stderr or "")}
    except subprocess.TimeoutExpired as e:
        return {"returncode": 124, "output": f"Timeout ({timeout}s) while running: {cmd}\n"}
    except Exception as e:
        return {"returncode": 1, "output": f"Error running {cmd}: {str(e)}\n"}

def get_last_author() -> str:
    try:
        cmd = shlex.split("git log -1 --pretty=format:%an <%ae>")
        out = subprocess.check_output(cmd, text=True).strip()
        return out
    except Exception:
        return "unknown"

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="report.json", help="Path to JSON report")
    parser.add_argument("--checks", nargs="*", help="Override checks (list of names)", default=None)
    args = parser.parse_args()

    checks_to_run = CHECKS
    if args.checks:
        checks_to_run = [c for c in CHECKS if c["name"] in args.checks]

    report: Dict[str, Any] = {"failed": False, "checks": [], "author": get_last_author()}

    for chk in checks_to_run:
        res = run_cmd(chk["cmd"])
        entry = {"name": chk["name"], "returncode": res["returncode"], "output": res["output"][:200000]}  # truncate
        report["checks"].append(entry)
        if res["returncode"] != 0:
            report["failed"] = True

    # Save report
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"Wrote report to {args.output}. failed={report['failed']}")
    return 1 if report["failed"] else 0

if __name__ == "__main__":
    sys.exit(main())