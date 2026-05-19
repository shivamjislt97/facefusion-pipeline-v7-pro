#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> int:
    p = subprocess.run(cmd, cwd=str(cwd), text=True)
    return p.returncode


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--mode", choices=["dry-run", "up", "status"], default="dry-run")
    args = parser.parse_args()

    project_root = Path(args.project_root)
    run_sh = project_root / "run.sh"
    if not run_sh.exists():
        print("run.sh missing")
        return 1

    if args.mode == "dry-run":
        return run(["bash", str(run_sh), "status"], project_root)
    if args.mode == "up":
        return run(["bash", str(run_sh), "up"], project_root)
    return run(["bash", str(run_sh), "status"], project_root)


if __name__ == "__main__":
    raise SystemExit(main())
