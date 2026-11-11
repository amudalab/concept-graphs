"""CLI: split ``filewords(om)3`` (``name>key1,key2,...`` lines) into per-document key files."""

from __future__ import annotations

from pathlib import Path

FILEWORDS_PATH = Path("data/filewords(om)3")
KEYS_DIR = Path("data/keys")


def main(filewords_path: Path = FILEWORDS_PATH, keys_dir: Path = KEYS_DIR) -> None:
    keys_dir.mkdir(parents=True, exist_ok=True)
    with filewords_path.open(encoding="utf-8") as filewords:
        for line in filewords:
            name, keyphrases = line.rstrip("\n").split(">", 1)
            lines = [key + "\n" for key in keyphrases.lower().split(",")]
            (keys_dir / name).write_text("".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
