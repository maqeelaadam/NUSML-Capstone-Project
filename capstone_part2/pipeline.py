"""Working validation scaffold. Cleaning and modelling remain pending."""
import argparse
import csv
import hashlib
import json
import logging
from pathlib import Path

from .data_io import load_records

logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1]


def configure_logging(log_path: Path, level: str) -> None:
    """Configure handlers only when this entry point is run."""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_path, encoding="utf-8")],
        force=True,
    )


def profile_records(rows: list[dict[str, str]], source: Path) -> dict:
    timestamps = [row["date_time"] for row in rows]
    profile = {
        "stage": "raw_validation_only",
        "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "row_count": len(rows),
        "column_count": len(rows[0]),
        "columns": list(rows[0]),
        "unique_timestamp_strings": len(set(timestamps)),
        "first_timestamp_string": min(timestamps),
        "last_timestamp_string": max(timestamps),
        "exact_duplicate_rows": len(rows) - len({tuple(row.items()) for row in rows}),
        "empty_cells_by_column": {
            column: sum(value[column].strip() == "" for value in rows)
            for column in rows[0]
        },
    }
    logger.debug("Raw profile: %s", profile)
    return profile


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=ROOT / "data/raw/Metro_Interstate_Traffic_Volume.csv")
    parser.add_argument("--output", type=Path, default=ROOT / "data/processed/raw_profile.json")
    parser.add_argument("--log-file", type=Path, default=ROOT / "capstone_part2/pipeline.log")
    parser.add_argument("--log-level", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO")
    args = parser.parse_args(argv)
    try:
        configure_logging(args.log_file, args.log_level)
        logger.info("Starting raw validation scaffold")
        rows = load_records(args.input)
        profile = profile_records(rows, args.input)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(profile, indent=2) + "\n", encoding="utf-8")
        logger.info("Saved raw profile to %s", args.output)
        logger.info("Validation complete; cleaning, full features, figures and CLI remain pending")
        return 0
    except (OSError, csv.Error, UnicodeError, ValueError) as exc:
        logger.error("Validation pipeline failed: %s", exc, exc_info=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
