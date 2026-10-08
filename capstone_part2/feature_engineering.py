"""Descriptive features; ML re-fits transformations on training data."""
import logging
import numpy as np
import pandas as pd
from .cleaning import SEVERE_WEATHER, LOW_VISIBILITY

logger = logging.getLogger(__name__)


def add_calendar(df):
    df = df.copy()
    date = pd.to_datetime(df.date_time)
    df["hour"] = date.dt.hour
    df["day_of_week"] = date.dt.dayofweek
    df["is_weekend"] = (df.day_of_week >= 5).astype(int)
    df["month"] = date.dt.month
    df["is_holiday"] = df.holiday.ne("None").astype(int)
    for field, period in [("hour", 24), ("day_of_week", 7)]:
        df[field + "_sin"] = np.sin(2 * np.pi * df[field] / period)
        df[field + "_cos"] = np.cos(2 * np.pi * df[field] / period)
    df["temp_celsius"] = df.temp - 273.15
    df["is_low_visibility"] = df.weather_main.isin(LOW_VISIBILITY).astype(int)
    df["is_severe_weather"] = df.weather_main.isin(SEVERE_WEATHER).astype(int)
    return df


def quartile_categories(values, thresholds):
    q1, q2, q3 = thresholds
    return np.select([values <= q1, values <= q2, values <= q3], ["Low", "Medium", "High"], default="Severe")


def engineer_features(df):
    logger.info("Before feature engineering: rows=%d columns=%d", *df.shape)
    df = add_calendar(df)
    thresholds = df.traffic_volume.quantile([0.25, 0.5, 0.75]).to_numpy()
    logger.debug("Descriptive traffic quartiles: %s", thresholds.tolist())
    df["congestion_category_quartile"] = quartile_categories(df.traffic_volume, thresholds)
    for column in ["temp", "clouds_all"]:
        mean, std = df[column].mean(), df[column].std(ddof=0)
        logger.debug("Descriptive %s mean=%s std=%s", column, mean, std)
        df[column + "_scaled"] = (df[column] - mean) / (std if std > 0 else 1)
    encoded = pd.get_dummies(df.weather_main, prefix="weather", dtype=int)
    df = pd.concat([df, encoded], axis=1)
    logger.info("After feature engineering: rows=%d columns=%d", *df.shape)
    return df
