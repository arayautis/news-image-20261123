#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261123.

The entry is the front page this repository holds (entry.png): a
1024x1024 newspaper front page summing up Monday 23 November 2026,
drawn by compose.py with vector art only (no photographs, no network).
This program does no drawing and reaches no network: it copies that
one file to the grader's output directory, so both runs write
identical bytes. Python 3.13, standard library only.

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil
from pathlib import Path

PNG_MAGIC = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])


def main() -> None:
    source = Path(__file__).resolve().parent / "entry.png"
    with source.open("rb") as handle:
        magic = handle.read(8)
    if magic != PNG_MAGIC:
        raise ValueError("entry.png is not a PNG file")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(source, dest)
    # Verify the copy landed whole: same size and same bytes as the source.
    if dest.stat().st_size != source.stat().st_size:
        raise ValueError("copied entry.png has the wrong size")
    if dest.read_bytes() != source.read_bytes():
        raise ValueError("copied entry.png differs from the source")


if __name__ == "__main__":
    main()
