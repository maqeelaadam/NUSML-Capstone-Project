"""Train and evaluate regression, proxy classifiers and a neural demand model."""
import os
os.environ.setdefault("MLFLOW_ALLOW_FILE_STORE","true")
import json
import logging
import time
import warnings
from pathlib import Path
import joblib
import mlflow
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.compose import TransformedTargetRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score, accuracy_score,precision_score,recall_score,f1_score,roc_auc_score
from sklearn.exceptions import ConvergenceWarning
from capstone_part2.cleaning import clean_data,hourly_view,SEVERE_WEATHER,LOW_VISIBILITY
from capstone_part3.supervised.common import chronological_split,features,preprocess,proxy_labels

logger=logging.getLogger(__name__)
ROOT=Path(__file__).resolve().parents[1]
RESULTS=ROOT/"capstone_part3/results"
MODELS=ROOT/"capstone_part3/models"


def regression_metrics(model,X,y):
    pred=model.predict(X)
    return {"MAE":float(mean_absolute_error(y,pred)),"R2":float(r2_score(y,pred))}


def classification_metrics(model,X,y):
    pred=model.predict(X);score=model.predict_proba(X)[:,1]
    return {"accuracy":float(accuracy_score(y,pred)),"precision":float(precision_score(y,pred,zero_division=0)),"recall":float(recall_score(y,pred,zero_division=0)),"F1":float(f1_score(y,pred,zero_division=0)),"ROC_AUC":float(roc_auc_score(y,score)) if len(np.unique(y))==2 else None}


def train():
    RESULTS.mkdir(parents=True,exist_ok=True);MODELS.mkdir(parents=True,exist_ok=True)
    raw=pd.read_csv(ROOT/"data/raw/Metro_Interstate_Traffic_Volume.csv",keep_default_na=False)
    raw_splits=chronological_split(raw)
    # All imputation references are from the training partition.
    train_hourly=hourly_view(clean_data(raw_splits[0]))
    val_hourly=hourly_view(clean_data(raw_splits[1],reference=raw_splits[0]))
    test_hourly=hourly_view(clean_data(raw_splits[2],reference=raw_splits[0]))
    datasets=[train_hourly,val_hourly,test_hourly]
    split_manifest={name:{"rows":len(df),"first":str(df.date_time.min()),"last":str(df.date_time.max())} for name,df in zip(["train","validation","test"],datasets)}
    (RESULTS/"split_manifest.json").write_text(json.dumps(split_manifest,indent=2)+"\n")
    thresholds=train_hourly.traffic_volume.quantile([0.25,0.5,0.75]).to_numpy()
    logger.debug("Training quartiles: %s",thresholds)
    (RESULTS/"label_definition.json").write_text(json.dumps({"training_quartiles":thresholds.tolist(),"severe_weather":sorted(SEVERE_WEATHER),"low_visibility_categories":sorted(LOW_VISIBILITY),"formula":"High/Severe congestion AND severe/low-visibility weather","proxy_only":True},indent=2)+"\n")
    X=[features(df) for df in datasets]
    yreg=[df.traffic_volume.to_numpy() for df in datasets]
    yclass=[proxy_labels(df,thresholds) for df in datasets]
    mlflow.set_tracking_uri((ROOT/".runtime/mlruns").as_uri())
    mlflow.set_experiment("traffic_capstone")
    estimators={
        "ridge_regression":("regression",Ridge(alpha=1.0)),
        "random_forest_regression":("regression",RandomForestRegressor(n_estimators=100,max_depth=18,min_samples_leaf=4,n_jobs=2,random_state=42)),
        "logistic_proxy_classifier":("classification",LogisticRegression(max_iter=1000,class_weight="balanced",random_state=42)),
        "random_forest_proxy_classifier":("classification",RandomForestClassifier(n_estimators=100,max_depth=18,min_samples_leaf=4,class_weight="balanced",n_jobs=2,random_state=42)),
        "neural_demand_network":("regression",TransformedTargetRegressor(regressor=MLPRegressor(hidden_layer_sizes=(64,32),activation="relu",max_iter=160,early_stopping=True,n_iter_no_change=12,random_state=42),transformer=StandardScaler())),
    }
    records=[];saved={}
    for name,(task,estimator) in estimators.items():
        logger.info("Training %s",name)
        start=time.perf_counter()
        model=Pipeline([("preprocess",preprocess()),("model",estimator)])
        target=yreg if task=="regression" else yclass
        with mlflow.start_run(run_name=name) as run:
            mlflow.log_params({"model_name":name,"task":task,"seed":42,"split":"chronological 70/15/15", "proxy_label":task=="classification","model_version":"v1"})
            # Only training data is passed to fit.
            with warnings.catch_warnings(record=True) as observed:
                warnings.simplefilter("always",ConvergenceWarning)
                model.fit(X[0],target[0])
            for warning in observed:
                logger.warning("Training warning for %s: %s",name,warning.message)
            evaluate=regression_metrics if task=="regression" else classification_metrics
            val=evaluate(model,X[1],target[1]);test=evaluate(model,X[2],target[2])
            duration=time.perf_counter()-start
            mlflow.log_metrics({**{"validation_"+k:v for k,v in val.items() if v is not None},**{"test_"+k:v for k,v in test.items() if v is not None},"fit_and_evaluate_seconds":duration})
            model_path=MODELS/(name+".joblib");joblib.dump(model,model_path)
            mlflow.log_artifact(str(model_path),artifact_path="models")
            mlflow.log_artifact(str(RESULTS/"split_manifest.json"))
            record={"name":name,"task":task,"version":"v1","validation":val,"test":test,"seconds":duration,"mlflow_run_id":run.info.run_id,"model_artifact":str(model_path.relative_to(ROOT)),"convergence_warnings":[str(w.message) for w in observed]}
            mlflow.log_dict(record,"evaluation.json")
            records.append(record);saved[name]=model
            logger.info("Saved %s; validation=%s test=%s",name,val,test)
    # Selection uses validation metrics only; test scores are reported once and do not select a model.
    regression= min([r for r in records if r["task"]=="regression"],key=lambda r:r["validation"]["MAE"])
    classifier=max([r for r in records if r["task"]=="classification"],key=lambda r:r["validation"]["F1"])
    best=saved[regression["name"]]
    joblib.dump(best,MODELS/"traffic_model.joblib")
    (RESULTS/"model_comparison.json").write_text(json.dumps({"models":records,"selected_regression":regression["name"],"selected_classifier":classifier["name"],"selection_basis":"validation MAE / validation F1"},indent=2)+"\n")
    predictions=test_hourly.copy()
    predictions["prediction"]=best.predict(X[2]);predictions["absolute_error"]=abs(predictions.prediction-predictions.traffic_volume)
    predictions["proxy_label"]=yclass[2];predictions["proxy_prediction"]=saved[classifier["name"]].predict(X[2])
    predictions.to_csv(ROOT/"data/processed/test_predictions.csv",index=False)
    group_rows=[]
    for column in ["weather_main"]:
        for value,group in predictions.groupby(column):
            group_rows.append({"dimension":column,"group":str(value),"n":len(group),"MAE":float(group.absolute_error.mean()),"proxy_F1":float(f1_score(group.proxy_label,group.proxy_prediction,zero_division=0))})
    for value,group in predictions.groupby(predictions.date_time.dt.hour):
        group_rows.append({"dimension":"hour","group":str(value),"n":len(group),"MAE":float(group.absolute_error.mean()),"proxy_F1":float(f1_score(group.proxy_label,group.proxy_prediction,zero_division=0))})
    for value,group in predictions.groupby(predictions.date_time.dt.dayofweek.ge(5)):
        group_rows.append({"dimension":"weekend","group":str(value),"n":len(group),"MAE":float(group.absolute_error.mean()),"proxy_F1":float(f1_score(group.proxy_label,group.proxy_prediction,zero_division=0))})
    pd.DataFrame(group_rows).to_csv(RESULTS/"group_error_audit.csv",index=False)
    # Recommendation profiles use training hours only, avoiding future-period advice leakage.
    recommendation=features(train_hourly).assign(traffic_volume=train_hourly.traffic_volume)
    recommendation.groupby(["is_weekend","weather_main","hour"]).agg(count=("traffic_volume","size"),mean=("traffic_volume","mean"),temp=("temp","mean"),rain_1h=("rain_1h","mean"),snow_1h=("snow_1h","mean"),clouds_all=("clouds_all","mean")).reset_index().to_csv(RESULTS/"training_travel_profiles.csv",index=False)
    client=mlflow.tracking.MlflowClient()
    exports=[]
    for record in records:
        run=client.get_run(record["mlflow_run_id"])
        exports.append({"run_id":run.info.run_id,"status":run.info.status,"start_time":run.info.start_time,"end_time":run.info.end_time,"params":run.data.params,"metrics":run.data.metrics,"artifact_uri":run.info.artifact_uri})
    (ROOT/"capstone_part3/experiments/tracking_export.json").write_text(json.dumps(exports,indent=2)+"\n")
    logger.info("Training and MLflow export complete")


def main():
    try:
        logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",handlers=[logging.StreamHandler(),logging.FileHandler(ROOT/"capstone_part3/training.log",encoding="utf-8")],force=True)
        train();return 0
    except (OSError,ValueError,KeyError,RuntimeError,ImportError) as exc:
        logger.error("Training failed: %s",exc,exc_info=True);return 1


if __name__=="__main__":
    raise SystemExit(main())
