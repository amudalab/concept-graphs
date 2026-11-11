#!/usr/bin/env python3
"""Convert PDFs under a directory tree to text with pdfminer."""

from __future__ import annotations

import argparse
from pathlib import Path

from pdfminer.high_level import extract_text  # type: ignore


def pdf_to_text(pdf_path: Path, txt_path: Path) -> None:
    text = extract_text(str(pdf_path)) or ""
    txt_path.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "directory",
        nargs="?",
        type=Path,
        default=Path("data"),
        help="Root directory to scan for PDFs",
    )
    parser.add_argument(
        "--progress",
        type=Path,
        default=Path("data/pdf2txtcount.txt"),
    )
    args = parser.parse_args(argv)

    done_count = 0
    if args.progress.exists():
        raw = args.progress.read_text(encoding="utf-8").strip()
        done_count = int(raw) if raw else 0

    converted = 0
    for pdf_path in sorted(args.directory.rglob("*.pdf")):
        txt_path = pdf_path.with_suffix(".txt")
        if txt_path.exists():
            continue
        print(pdf_path)
        pdf_to_text(pdf_path, txt_path)
        converted += 1

    args.progress.write_text(str(done_count + converted), encoding="utf-8")
    print(f"converted {converted} PDFs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
