#!/usr/bin/env python3
"""Download PDFs for keyphrases via Google Custom Search."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any, Mapping

from googleapiclient.discovery import build  # type: ignore
import urllib.request


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise SystemExit(
            f"Environment variable {name} is required. "
            "Export GOOGLE_API_KEY and GOOGLE_CSE_ID before running."
        )
    return value


def _download(url: str, destination: Path) -> bool:
    try:
        urllib.request.urlretrieve(url, destination)
        return True
    except Exception as exc:  # noqa: BLE001 - network errors vary
        print(f"download failed for {url}: {exc}")
        return False


def search_and_download(
    phrases: list[str],
    *,
    start_index: int,
    limit: int,
    output_root: Path,
    relation_log: Path,
) -> int:
    api_key = _require_env("GOOGLE_API_KEY")
    cse_id = _require_env("GOOGLE_CSE_ID")
    service = build("customsearch", "v1", developerKey=api_key)

    processed = 0
    with relation_log.open("a", encoding="utf-8") as rel:
        for offset, phrase in enumerate(phrases[start_index:]):
            if processed >= limit:
                break
            folder = output_root / phrase
            if folder.exists():
                print(f"skip existing: {phrase}")
                continue
            folder.mkdir(parents=True, exist_ok=True)
            rel.write(f"{phrase}\t")
            rank = 0
            for low, high in ((1, 10), (11, 20)):
                response: Mapping[str, Any] = (
                    service.cse()
                    .list(
                        q=phrase,
                        cx=cse_id,
                        fileType="pdf",
                        lr="lang_en",
                        num=10,
                        lowRange=str(low) if low > 1 else None,
                        highRange=str(high) if low > 1 else None,
                    )
                    .execute()
                )
                for item in response.get("items", []):
                    url = item["link"]
                    filename = url.rsplit("/", 1)[-1] or f"result-{rank}.pdf"
                    target = folder / filename
                    if _download(url, target):
                        rank += 1
                        rel.write(f"{target} {rank} ")
                        print(url)
            rel.write("\n")
            processed += 1
            _write_counter(relation_log.parent / "keycount.txt", start_index + offset + 1)
    return processed


def _write_counter(path: Path, value: int) -> None:
    path.write_text(str(value), encoding="utf-8")


def _read_counter(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8").strip()
    return int(text) if text else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--phrases",
        type=Path,
        default=Path("data/compkey.txt"),
        help="TSV/lines of keyphrases (first column used)",
    )
    parser.add_argument("--limit", type=int, default=30)
    parser.add_argument("--output", type=Path, default=Path("Gsearch"))
    args = parser.parse_args(argv)

    phrases: list[str] = []
    for line in args.phrases.read_text(encoding="utf-8").splitlines():
        phrase = line.split("\t", 1)[0].strip().lower()
        if phrase:
            phrases.append(phrase)

    counter_path = Path("data/keycount.txt")
    start = _read_counter(counter_path)
    relation_log = Path("data/docrel.txt")
    count = search_and_download(
        phrases,
        start_index=start,
        limit=args.limit,
        output_root=args.output,
        relation_log=relation_log,
    )
    print(f"downloaded sets: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
