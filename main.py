#!/usr/bin/env python3
"""news-image-20261120 entrypoint.

Copies the pre-rendered front page (entry.png, drawn by draw.py from the
verified news of Friday 20 November 2026) to /output/entry.png, or to
$MAKEFUN_OUTPUT_DIR when set for a local run.

Standard library only, no network, no randomness: every run writes the
same bytes.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")


if __name__ == "__main__":
    main()
