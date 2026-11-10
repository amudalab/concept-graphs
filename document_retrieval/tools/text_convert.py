"""CLI: copy every file in ``all/`` to ``output/`` with spaces removed from its name."""

from __future__ import annotations

from pathlib import Path

SOURCE_DIR = Path("all")
OUTPUT_DIR = Path("output")


def main(source_dir: Path = SOURCE_DIR, output_dir: Path = OUTPUT_DIR) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for source in sorted(source_dir.iterdir()):
        target = output_dir / (source.name.replace(" ", "") + ".txt")
        target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")


if __name__ == "__main__":
    main()
