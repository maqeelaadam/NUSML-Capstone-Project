"""Timestamp-aware splits and training-fitted predictor transformations."""
import logging
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from capstone_part2.feature_engineering import add_calendar, quartile_categories
from capstone_part2.cleaning import SEVERE_WEATHER, LOW_VISIBILITY

logger=logging.getLogger(__name__)
NUMERIC=["temp","rain_1h","snow_1h","clouds_all","hour","day_of_week","month","is_weekend","is_holiday","hour_sin","hour_cos","day_of_week_sin","day_of_week_cos"]
CATEGORICAL=["weather_main"]
FEATURES=NUMERIC+CATEGORICAL


def chronological_split(raw):
    timestamps=pd.to_datetime(raw.date_time,format="%Y-%m-%d %H:%M:%S",errors="raise")
    unique=np.sort(timestamps.unique())
    if len(unique)<20:
        raise ValueError("Too few unique timestamps for chronological split")
    cutoff1=unique[int(len(unique)*0.7)];cutoff2=unique[int(len(unique)*0.85)]
    splits=[raw.loc[timestamps<cutoff1].copy(),raw.loc[(timestamps>=cutoff1)&(timestamps<cutoff2)].copy(),raw.loc[timestamps>=cutoff2].copy()]
    logger.info("Chronological cutoffs: %s and %s",cutoff1,cutoff2)
    return splits


def preprocess():
    return ColumnTransformer([
        ("numeric",Pipeline([("impute",SimpleImputer(strategy="median")),("scale",StandardScaler())]),NUMERIC),
        ("weather",OneHotEncoder(handle_unknown="ignore",sparse_output=False),CATEGORICAL),
    ])


def features(df):
    return add_calendar(df)[FEATURES]


def proxy_labels(df, thresholds):
    category=quartile_categories(df.traffic_volume,thresholds)
    congestion=np.isin(category,["High","Severe"])
    risky=df.weather_main.isin(SEVERE_WEATHER|LOW_VISIBILITY).to_numpy()
    return (congestion&risky).astype(int)
