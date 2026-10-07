"""Run validated loading, cleaning, hourly aggregation, features and figures."""
import argparse
import csv
import json
import logging
from pathlib import Path
import pandas as pd
from .data_io import load_records
from .cleaning import clean_data, hourly_view
from .feature_engineering import engineer_features
from .visualizations import save_figures

logger = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1]


def configure_logging(log_path, level):
    log_path.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=getattr(logging,level),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(),logging.FileHandler(log_path,encoding="utf-8",mode="w")], force=True)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input",type=Path,default=ROOT/"data/raw/Metro_Interstate_Traffic_Volume.csv")
    parser.add_argument("--output-dir",type=Path,default=ROOT/"data/processed")
    parser.add_argument("--figures-dir",type=Path,default=ROOT/"capstone_part2/figures")
    parser.add_argument("--log-file",type=Path,default=ROOT/"capstone_part2/pipeline.log")
    parser.add_argument("--log-level",choices=["DEBUG","INFO","WARNING","ERROR"],default="INFO")
    args=parser.parse_args(argv)
    try:
        configure_logging(args.log_file,args.log_level)
        raw=pd.DataFrame(load_records(args.input))
        cleaned=clean_data(raw)
        hourly=hourly_view(cleaned)
        features=engineer_features(hourly)
        args.output_dir.mkdir(parents=True,exist_ok=True)
        for name,frame in [("cleaned_observations.csv",cleaned),("hourly_traffic.csv",hourly),("traffic_features.csv",features)]:
            path=args.output_dir/name;frame.to_csv(path,index=False)
            logger.info("Saved %d rows and %d columns to %s",*frame.shape,path)
        audit={"raw_rows":len(raw),"cleaned_observations":len(cleaned),"unique_hours":len(hourly),"full_data_features_for_descriptive_analysis_only":True}
        (args.output_dir/"pipeline_audit.json").write_text(json.dumps(audit,indent=2)+"\n")
        save_figures(features,args.figures_dir)
        logger.info("Pipeline completed successfully")
        return 0
    except (OSError,csv.Error,UnicodeError,ValueError,KeyError,TypeError) as exc:
        logger.error("Pipeline failed: %s",exc,exc_info=True)
        return 1


if __name__=="__main__":
    raise SystemExit(main())
