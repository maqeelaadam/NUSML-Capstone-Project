"""Produce SQLite, statistical and probability evidence from raw and hourly data."""
import json
import logging
import sqlite3
from pathlib import Path
import pandas as pd

logger=logging.getLogger(__name__)
ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/"capstone_part1/results"


def probability(df):
    congestion=df.traffic_volume.gt(5500)
    clear=df.weather_main.eq("Clear")
    cloudy=df.weather_main.eq("Clouds")
    hot=df.temp.gt(292)
    a=int((congestion&clear).sum());b=int((~congestion&clear).sum())
    c=int((congestion&cloudy).sum());d=int((~congestion&cloudy).sum())
    joint=float((congestion&clear).mean())
    product=float(congestion.mean()*clear.mean())
    return {"n":len(df),"congestion_count":int(congestion.sum()),
        "P_congestion":float(congestion.mean()),"P_clear":float(clear.mean()),
        "P_congestion_and_clear":joint,"P_clear_given_congestion":float(clear[congestion].mean()),
        "P_hot_given_congestion":float(hot[congestion].mean()),"independence_product":product,
        "independence_absolute_gap":abs(joint-product),
        "clear_cloudy_table":{"clear_congested":a,"clear_uncongested":b,"cloudy_congested":c,"cloudy_uncongested":d},
        "odds_ratio_clear_vs_cloudy":a*d/(b*c) if b*c else None,
        "odds_ratio_excluded_other_weather":int((~(clear|cloudy)).sum())}


def analyze():
    RESULTS.mkdir(parents=True,exist_ok=True)
    raw=pd.read_csv(ROOT/"data/raw/Metro_Interstate_Traffic_Volume.csv",keep_default_na=False)
    hourly=pd.read_csv(ROOT/"data/processed/hourly_traffic.csv",keep_default_na=False,parse_dates=["date_time"])
    db=ROOT/"data/processed/traffic.sqlite"
    with sqlite3.connect(db) as con:
        raw.to_sql("traffic_raw",con,if_exists="replace",index=False)
        hourly.to_sql("traffic_hourly",con,if_exists="replace",index=False)
        logger.info("SQLite import verified: raw=%d hourly=%d",con.execute("SELECT COUNT(*) FROM traffic_raw").fetchone()[0],con.execute("SELECT COUNT(*) FROM traffic_hourly").fetchone()[0])
        for table in ["traffic_raw","traffic_hourly"]:
            annual=pd.read_sql_query(f"SELECT strftime('%Y',date_time) AS year, COUNT(*) AS observations,COUNT(DISTINCT date_time) AS unique_hours,SUM(traffic_volume) AS total_volume,AVG(traffic_volume) AS mean_volume FROM {table} WHERE strftime('%Y',date_time) BETWEEN '2012' AND '2017' GROUP BY year ORDER BY year",con)
            annual["absolute_change"]=annual.total_volume.diff()
            annual["percent_change"]=annual.total_volume.pct_change()*100
            annual["full_year_expected_hours"]=[8784 if int(y)%4==0 else 8760 for y in annual.year]
            annual["full_year_coverage_pct"]=100*annual.unique_hours/annual.full_year_expected_hours
            annual.to_csv(RESULTS/f"annual_{table}.csv",index=False)
            logger.info("Saved annual SQL output for %s",table)
        holiday=pd.read_sql_query("SELECT strftime('%Y',date_time) AS year,holiday,COUNT(*) AS labelled_observations,AVG(CASE WHEN temp>0 THEN temp END) AS mean_kelvin FROM traffic_raw WHERE strftime('%Y',date_time) BETWEEN '2015' AND '2017' AND holiday IN ('New Years Day','Labor Day') GROUP BY year,holiday ORDER BY holiday,year",con)
        holiday["mean_celsius"]=holiday.mean_kelvin-273.15
        holiday.to_csv(RESULTS/"holiday_temperatures.csv",index=False)
    volume=hourly.traffic_volume
    stats={"n_unique_hours":len(hourly),"mean":float(volume.mean()),"median":float(volume.median()),
        "sample_standard_deviation":float(volume.std(ddof=1)),"sample_variance":float(volume.var(ddof=1)),
        "minimum":float(volume.min()),"maximum":float(volume.max()),"range":float(volume.max()-volume.min()),
        "pearson_temperature_traffic":float(hourly.temp.corr(volume)),
        "hourly_probability":probability(hourly),"raw_observation_probability_sensitivity":probability(raw)}
    (RESULTS/"statistics_probability.json").write_text(json.dumps(stats,indent=2)+"\n")
    (RESULTS/"data_quality.json").write_text(json.dumps({"raw_shape":list(raw.shape),"missing_cells":raw.isna().sum().to_dict(),"raw_unique_hours":raw.date_time.nunique(),"exact_duplicates":int(raw.duplicated().sum()),"zero_kelvin":int(raw.temp.le(0).sum()),"rain_above_9000":int(raw.rain_1h.gt(9000).sum())},indent=2)+"\n")
    logger.info("Saved supplementary statistical, probability and data-quality outputs")
    return stats


def main():
    try:
        logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",handlers=[logging.StreamHandler(),logging.FileHandler(ROOT/"capstone_part1/analysis.log",encoding="utf-8")],force=True)
        analyze();return 0
    except (OSError,ValueError,sqlite3.Error,KeyError) as exc:
        logger.error("Part 1 analysis failed: %s",exc,exc_info=True);return 1


if __name__=="__main__":
    raise SystemExit(main())
