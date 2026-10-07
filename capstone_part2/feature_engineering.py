"""Initial calendar features; full Task 2 feature engineering is pending."""
import logging
import math
from datetime import datetime

logger = logging.getLogger(__name__)


def calendar_features(timestamp: str) -> dict[str, int | float]:
    date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    hour, weekday = date.hour, date.weekday()
    return {
        "hour": hour,
        "day_of_week": weekday,
        "is_weekend": int(weekday >= 5),
        "hour_sin": math.sin(2 * math.pi * hour / 24),
        "hour_cos": math.cos(2 * math.pi * hour / 24),
        "weekday_sin": math.sin(2 * math.pi * weekday / 7),
        "weekday_cos": math.cos(2 * math.pi * weekday / 7),
    }
