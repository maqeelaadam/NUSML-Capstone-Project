"""Validate and copy the supplied CSV into the ignored raw directory."""
import argparse
import csv
import hashlib
import logging
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from capstone_part2.data_io import load_records

logger = logging.getLogger(__name__)
EXPECTED_SHA256 = "749c90d720360a4215bb15345526073c079ba4cc95e3fa558796d083f85fce9e"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        log_path = ROOT / "data/import.log"
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            handlers=[logging.StreamHandler(), logging.FileHandler(log_path, encoding="utf-8")],
            force=True,
        )
        rows = load_records(args.source)
        checksum = hashlib.sha256(args.source.read_bytes()).hexdigest()
        if checksum != EXPECTED_SHA256:
            raise ValueError("Source checksum differs from supplied course data; document the new version before importing")
        target = ROOT / "data/raw/Metro_Interstate_Traffic_Volume.csv"
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            existing = hashlib.sha256(target.read_bytes()).hexdigest()
            if existing != checksum:
                raise ValueError("A different raw dataset already exists; refusing to overwrite it")
            logger.info("Verified existing raw dataset: %s", target)
        else:
            shutil.copyfile(args.source, target)
            logger.info("Imported %d raw observations to %s", len(rows), target)
        logger.info("SHA-256: %s", checksum)
        return 0
    except (OSError, csv.Error, UnicodeError, ValueError) as exc:
        logger.error("Data import failed: %s", exc, exc_info=True)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
