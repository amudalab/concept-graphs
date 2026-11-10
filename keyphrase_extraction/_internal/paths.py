"""Resolved data directories for the keyphrase_extraction module."""

from __future__ import annotations

from pathlib import Path

MODULE_ROOT: Path = Path(__file__).resolve().parents[1]
DATA_DIR: Path = MODULE_ROOT / "data"
TRANSCRIPTS_DIR: Path = DATA_DIR / "transcripts"
OUTPUT_DIR: Path = DATA_DIR / "output"
KEYS_DIR: Path = DATA_DIR / "keys"
VIDEO_SLIDES_DIR: Path = DATA_DIR / "video_text_slides"
TRAINING_DATA_DIR: Path = DATA_DIR / "training_data"
CONFIG_DIR: Path = MODULE_ROOT / "config"


def lecture_stem(filename: str) -> str:
    """Return the lecture id (filename without extension)."""
    return Path(filename).stem.split("_")[0]
