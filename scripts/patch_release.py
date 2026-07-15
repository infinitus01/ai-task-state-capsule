#!/usr/bin/env python3
"""Run the release pipeline."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from pack_common import RELEASE, project_root


def run_step(label: str, args: list[str]) -> None:
    print(f"\n==> {label}")
    print(" ".join(args))
    result = subprocess.run(args, cwd=project_root())
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def prune_old_builds(dist: Path) -> None:
    groups = {
        "source": "ai-task-state-capsule-source-",
        "capsule": "ai-task-state-capsule-v",
        "audit": "ai-task-state-capsule-work-audit-",
    }
    for prefix in groups.values():
        matches = sorted(dist.glob(f"{prefix}*"), key=lambda p: p.stat().st_mtime, reverse=True)
        keep = None
        for path in matches:
            if path.suffix == ".zip":
                keep = path.stem
                break
        for path in matches:
            if path.suffix == ".zip" and path.stem != keep:
                path.unlink()
                print(f"Removed stale build: {path.name}")
            elif path.suffix in {".json", ".sha256"} and keep and not path.name.startswith(keep):
                path.unlink()
                print(f"Removed stale seal: {path.name}")


def main() -> int:
    root = project_root()
    py = sys.executable
    dist = root / "dist"
    print(f"Release: {RELEASE}")
    run_step("Source ZIP", [py, "scripts/generate_source_zip.py"])
    run_step(
        "Capsule handoff readiness",
        [
            py,
            "scripts/verify_capsule.py",
            "--capsule-dir",
            "examples/example-coding-task",
            "--ready-for-handoff",
        ],
    )
    run_step(
        "Capsule ZIP",
        [py, "scripts/generate_capsule_zip.py", "--source", "examples/example-coding-task"],
    )
    capsule_zips = sorted(
        dist.glob("ai-task-state-capsule-v*.zip"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not capsule_zips:
        print("No capsule ZIP found", file=sys.stderr)
        return 1
    run_step(
        "Audit ZIP + external seal",
        [py, "scripts/generate_audit_zip.py", "--capsule-zip", str(capsule_zips[0])],
    )
    prune_old_builds(dist)
    print("\n==> Final verification")
    return subprocess.run([py, "scripts/verify_zips.py"], cwd=root).returncode


if __name__ == "__main__":
    raise SystemExit(main())
