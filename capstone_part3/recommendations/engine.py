"""Recommend observed low-traffic windows with day/weather context."""
import argparse
import json
import logging
from pathlib import Path
import pandas as pd
import joblib
from capstone_part3.supervised.common import features

logger=logging.getLogger(__name__)
ROOT=Path(__file__).resolve().parents[2]


def recommend(day_type="weekday",weather="Clear",earliest=6,latest=22):
    if day_type not in {"weekday","weekend"} or not 0<=earliest<latest<=24:
        raise ValueError("Choose weekday/weekend and 0 <= earliest < latest <=24")
    profile=pd.read_csv(ROOT/"capstone_part3/results/training_travel_profiles.csv")
    match=profile.loc[profile.is_weekend.eq(int(day_type=="weekend")) & profile.weather_main.eq(weather) & profile.hour.ge(earliest) & profile.hour.lt(latest) & profile['count'].ge(20)]
    if match.empty:raise ValueError("No sufficiently supported matching travel windows; broaden the conditions")
    context=match.copy()
    # Illustrative calendar dates are within the training period and have the requested day type.
    context["date_time"]=pd.to_datetime("2017-05-08" if day_type=="weekday" else "2017-05-06") + pd.to_timedelta(context.hour,unit="h")
    context["holiday"]="None"
    model=joblib.load(ROOT/"capstone_part3/models/traffic_model.joblib")
    match=match.copy()
    match["model_estimate"]=model.predict(features(context))
    match["ranking_score"]=(match["mean"]+match.model_estimate)/2
    choice=match.sort_values(["ranking_score","hour"]).iloc[0]
    hour=int(choice.hour)
    return {"recommended_hour":hour,"mean_vehicles_per_hour":float(choice['mean']),"model_estimate":float(choice.model_estimate),"ranking_rule":"Equal weight historical mean and illustrative model estimate","supporting_hours":int(choice['count']),"message":f"For a {day_type} journey in {weather.lower()} conditions, consider {hour:02d}:00-{hour+1:02d}:00 within your selected hours. Training-period traffic averaged {choice['mean']:,.0f} vehicles/hour across {int(choice['count'])} observations. The model estimates {choice.model_estimate:,.0f} vehicles/hour under an illustrative training-calendar scenario with mean weather inputs. This is historical timing advice for one corridor, not a safety or live-traffic guarantee."}


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--day-type",choices=["weekday","weekend"],default="weekday")
    parser.add_argument("--weather",default="Clear")
    parser.add_argument("--earliest",type=int,default=6);parser.add_argument("--latest",type=int,default=22)
    args=parser.parse_args(argv)
    try:
        logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",handlers=[logging.StreamHandler(),logging.FileHandler(ROOT/"capstone_part3/recommendations.log",encoding="utf-8")],force=True)
        logger.info("Recommendation arguments %s",vars(args))
        print(json.dumps(recommend(args.day_type,args.weather,args.earliest,args.latest),indent=2));return 0
    except (OSError,ValueError,KeyError) as exc:
        logger.error("Cannot recommend a window: %s",exc);return 1


if __name__=="__main__":raise SystemExit(main())
