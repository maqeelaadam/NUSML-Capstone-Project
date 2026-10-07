"""Read raw records and validate the schema before further processing."""
import csv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
EXPECTED_COLUMNS = (
    "holiday", "temp", "rain_1h", "snow_1h", "clouds_all",
    "weather_main", "weather_description", "date_time", "traffic_volume",
)


def load_records(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, strict=True)
        columns = reader.fieldnames or []
        missing = sorted(set(EXPECTED_COLUMNS) - set(columns))
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        if len(columns) != len(set(columns)):
            raise ValueError("Duplicate CSV column names")
        logger.info("Schema validated: %d columns", len(columns))
        rows = []
        for line_number, row in enumerate(reader, start=2):
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"Inconsistent CSV fields on line {line_number}")
            rows.append(row)
    if not rows:
        raise ValueError("Dataset contains no data rows")
    logger.info("Loaded %d rows and %d columns from %s", len(rows), len(columns), path)
    return rows
