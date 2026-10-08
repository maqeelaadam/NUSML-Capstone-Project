"""Query observed traffic with validated user input."""
import argparse
import logging
from datetime import datetime
from pathlib import Path
import pandas as pd

logger=logging.getLogger(__name__)
ROOT=Path(__file__).resolve().parents[2]


class QueryParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def main(argv=None):
    try:
        logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            handlers=[logging.StreamHandler(),logging.FileHandler(ROOT/"capstone_part2/mini_app.log",encoding="utf-8")],force=True)
    except OSError as exc:
        logger.error("Cannot configure application logging: %s",exc)
        return 1
    parser=QueryParser(description=__doc__)
    parser.add_argument("--data",type=Path,default=ROOT/"capstone_part2/data/processed/traffic_features.csv")
    sub=parser.add_subparsers(dest="command",required=True)
    at=sub.add_parser("at");at.add_argument("--datetime",required=True)
    high=sub.add_parser("high-traffic");high.add_argument("--threshold",type=float,default=5500);high.add_argument("--limit",type=int,default=10)
    sub.add_parser("compare-day-types")
    try:
        args=parser.parse_args(argv)
    except ValueError as exc:
        logger.error("Invalid command arguments: %s",exc)
        return 2
    try:
        logger.info("Command %s arguments %s",args.command,vars(args))
        df=pd.read_csv(args.data,keep_default_na=False,parse_dates=["date_time"])
        if args.command=="at":
            value=datetime.strptime(args.datetime,"%Y-%m-%d %H:%M:%S")
            result=df.loc[df.date_time.eq(value),["date_time","traffic_volume","weather_main","temp_celsius"]]
            print(result.to_string(index=False) if len(result) else "No observed traffic for that timestamp.")
        elif args.command=="high-traffic":
            if not (0<=args.threshold<100000) or not 1<=args.limit<=1000:
                raise ValueError("Threshold must be finite in [0,100000) and limit in [1,1000]")
            result=df.loc[df.traffic_volume.gt(args.threshold),["date_time","traffic_volume","weather_main"]].nlargest(args.limit,"traffic_volume")
            print(result.to_string(index=False) if len(result) else "No observed hours exceed the threshold.")
        else:
            result=df.groupby("is_weekend").traffic_volume.agg(["count","mean","median"]).rename(index={0:"Weekday",1:"Weekend"})
            print(result.to_string())
        return 0
    except (OSError,ValueError,KeyError,TypeError) as exc:
        logger.error("Cannot answer query: %s",exc)
        return 1


if __name__=="__main__":
    raise SystemExit(main())
