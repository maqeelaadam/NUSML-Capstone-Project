"""Simulate feature drift using an effect-size threshold, with PASS/ALERT."""
import json
import logging
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp

logger=logging.getLogger(__name__)
ROOT=Path(__file__).resolve().parents[2]


def check_drift(reference,current,threshold=.2):
    rows=[]
    for field in ["temp","rain_1h","clouds_all"]:
        result=ks_2samp(reference[field],current[field])
        rows.append({"feature":field,"KS_statistic":float(result.statistic),"p_value":float(result.pvalue),"threshold":threshold,"status":"ALERT" if result.statistic>threshold else "PASS"})
    status="ALERT" if any(r["status"]=="ALERT" for r in rows) else "PASS"
    if status=="ALERT":logger.warning("Monitoring ALERT: feature drift exceeds effect-size threshold")
    else:logger.info("Monitoring PASS: no feature drift exceeds effect-size threshold")
    return {"status":status,"checks":rows,"scope":"Feature distribution drift simulation; not proof of prediction degradation."}


def main():
    try:
        logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",handlers=[logging.StreamHandler(),logging.FileHandler(ROOT/"capstone_part3/monitoring.log",encoding="utf-8")],force=True)
        df=pd.read_csv(ROOT/"capstone_part2/data/processed/hourly_traffic.csv",keep_default_na=False,parse_dates=["date_time"])
        manifest=json.loads((ROOT/"capstone_part3/results/split_manifest.json").read_text())
        reference=df.loc[df.date_time.le(pd.Timestamp(manifest["train"]["last"]))]
        current=df.loc[df.date_time.ge(pd.Timestamp(manifest["test"]["first"]))]
        shifted=current.copy();shifted["temp"]=shifted.temp+20
        output={"threshold_rationale":"KS effect size >0.20 is a transparent classroom threshold requiring operational calibration; p-values are shown but not the sole trigger.","normal_control":check_drift(reference,reference.copy()),"observed_later_period":check_drift(reference,current),"injected_20K_shift":check_drift(reference,shifted)}
        (ROOT/"capstone_part3/results/monitoring_status.json").write_text(json.dumps(output,indent=2)+"\n")
        logger.info("Saved monitoring simulation");return 0
    except (OSError,ValueError,KeyError) as exc:
        logger.error("Monitoring failed: %s",exc,exc_info=True);return 1


if __name__=="__main__":raise SystemExit(main())
