"""Auditable cleaning; optional reference ensures train-only imputation."""
import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)
NUMERIC = ["temp", "rain_1h", "snow_1h", "clouds_all", "traffic_volume"]
WEATHER_SEVERITY = {"Clear": 0, "Clouds": 1, "Haze": 2, "Drizzle": 2,
                    "Rain": 3, "Mist": 3, "Smoke": 4, "Snow": 4,
                    "Fog": 5, "Thunderstorm": 5, "Squall": 6}
SEVERE_WEATHER = {"Thunderstorm", "Squall", "Snow"}
LOW_VISIBILITY = {"Fog", "Mist", "Haze", "Smoke"}


def prepare(df):
    """Validate/flag anomalies without estimating any distribution parameters."""
    df = df.copy()
    for column in ["holiday", "weather_main", "weather_description"]:
        original = df[column].astype(str)
        stripped = original.str.strip()
        if column == "weather_main":
            stripped = stripped.str.title()
        changed = int(original.ne(stripped).sum())
        if changed:
            logger.warning("Standardised %d rows: %s whitespace/case", changed, column)
        else:
            logger.info("Categorical check %s: no changes", column)
        df[column] = stripped
    parsed = pd.to_datetime(df.date_time, format="%Y-%m-%d %H:%M:%S", errors="coerce")
    invalid = int(parsed.isna().sum())
    if invalid:
        logger.warning("Dropped %d rows: invalid date_time", invalid)
    df = df.loc[parsed.notna()].copy()
    df["date_time"] = parsed.loc[parsed.notna()]
    logger.info("Date/time validation complete: %d retained rows", len(df))
    before = len(df)
    df = df.drop_duplicates()
    count = before - len(df)
    if count:
        logger.warning("Dropped %d rows: exact duplicates", count)
    else:
        logger.info("Exact duplicate check: no rows removed")
    for column in NUMERIC:
        numeric = pd.to_numeric(df[column], errors="coerce")
        bad = ~np.isfinite(numeric)
        if column == "temp":
            bad |= numeric.le(0) | numeric.gt(350)
        elif column == "rain_1h":
            bad |= numeric.lt(0) | numeric.gt(9000)
        elif column == "clouds_all":
            bad |= numeric.lt(0) | numeric.gt(100)
        else:
            bad |= numeric.lt(0)
        if column == "traffic_volume":
            bad |= numeric.mod(1).ne(0)
        count = int(bad.sum())
        df[column] = numeric.mask(bad)
        if count:
            logger.warning("Flagged %d rows: missing/nonfinite/impossible %s", count, column)
        else:
            logger.info("Numeric check %s: no invalid values", column)
    return df


def clean_data(df, reference=None):
    df = prepare(df)
    reference = df if reference is None else prepare(reference)
    # The measured target is never imputed.
    invalid_target = df.traffic_volume.isna()
    if invalid_target.any():
        logger.warning("Dropped %d rows: missing/invalid measured traffic target", invalid_target.sum())
        df = df.loc[~invalid_target].copy()
    for column in NUMERIC[:-1]:
        invalid = df[column].isna()
        for month in sorted(df.loc[invalid, "date_time"].dt.month.unique()):
            selection = invalid & df.date_time.dt.month.eq(month)
            median = reference.loc[reference.date_time.dt.month.eq(month), column].median()
            if pd.isna(median):
                median = reference[column].median()
            if pd.isna(median):
                raise ValueError(f"No valid reference readings to impute {column}")
            logger.debug("Monthly %s median month=%s value=%s", column, month, median)
            df.loc[selection, column] = median
            logger.warning("Imputed %d rows: %s using reference median for month %d", selection.sum(), column, month)
        logger.info("Imputation check complete: %s", column)
    if df.empty:
        raise ValueError("No valid records remain after cleaning")
    return df.sort_values("date_time", kind="stable").reset_index(drop=True)


def hourly_view(df):
    conflicts = df.groupby("date_time").traffic_volume.nunique().gt(1)
    if conflicts.any():
        raise ValueError("Conflicting measured traffic values at repeated timestamps")
    # Conservative category selection is explicit: select highest severity per hour.
    ranked = df.assign(_severity=df.weather_main.map(WEATHER_SEVERITY).fillna(2))
    ranked = ranked.sort_values(["date_time", "_severity", "weather_main", "weather_description"], ascending=[True, False, True, True])
    categories = ranked.drop_duplicates("date_time")[["date_time", "weather_main", "weather_description", "holiday"]]
    means = df.groupby("date_time", as_index=False)[NUMERIC].mean()
    hourly = means.merge(categories, on="date_time", validate="one_to_one")
    reduction = len(df) - len(hourly)
    if reduction:
        logger.warning("Aggregated %d extra records into %d unique hours: mean weather readings, identical traffic count, highest-severity category", reduction, len(hourly))
    # Holiday labels occur at isolated hours: explicitly propagate within labelled dates.
    dates = hourly.date_time.dt.date
    holiday_dates = hourly.loc[hourly.holiday.ne("None")].assign(_date=dates).groupby("_date").holiday.first()
    replacement = dates.map(holiday_dates).fillna("None")
    changed = hourly.holiday.ne(replacement)
    if changed.any():
        logger.warning("Modified %d rows: propagate observed holiday label across its calendar date", changed.sum())
    hourly["holiday"] = replacement
    return hourly.sort_values("date_time").reset_index(drop=True)
