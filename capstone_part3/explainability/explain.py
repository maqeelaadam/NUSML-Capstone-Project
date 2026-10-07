"""Explain the comparable tree traffic model using SHAP on holdout examples."""
import json
import logging
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import shap
from capstone_part3.supervised.common import features

logger=logging.getLogger(__name__)
ROOT=Path(__file__).resolve().parents[2]


def main():
    try:
        logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",handlers=[logging.StreamHandler(),logging.FileHandler(ROOT/"capstone_part3/explainability.log",encoding="utf-8")],force=True)
        model=joblib.load(ROOT/"capstone_part3/models/random_forest_regression.joblib")
        df=pd.read_csv(ROOT/"data/processed/test_predictions.csv",keep_default_na=False,parse_dates=["date_time"])
        sample=df.sample(min(150,len(df)),random_state=42)
        X=model.named_steps["preprocess"].transform(features(sample))
        names=model.named_steps["preprocess"].get_feature_names_out()
        explainer=shap.TreeExplainer(model.named_steps["model"])
        values=explainer.shap_values(X)
        ranking=pd.DataFrame({"feature":names,"mean_absolute_SHAP":np.abs(values).mean(axis=0)}).sort_values("mean_absolute_SHAP",ascending=False)
        ranking.to_csv(ROOT/"capstone_part3/results/shap_importance.csv",index=False)
        fig,ax=plt.subplots(figsize=(8,5))
        ranking.head(12).iloc[::-1].plot.barh(x="feature",y="mean_absolute_SHAP",ax=ax,color="#24618a",legend=False)
        ax.set(title="Tree model explanation on 150 held-out hours",xlabel="Mean absolute SHAP contribution (vehicles/hour)",ylabel="Feature")
        fig.tight_layout();fig.savefig(ROOT/"capstone_part3/results/shap_importance.png",dpi=130);plt.close(fig)
        reconstruction=np.asarray(values).sum(axis=1)+float(np.asarray(explainer.expected_value).item())
        error=float(np.max(abs(reconstruction-model.named_steps["model"].predict(X))))
        (ROOT/"capstone_part3/results/explanation_check.json").write_text(json.dumps({"sample_size":len(sample),"max_additivity_error":error,"explained_model":"random_forest_regression","neural_model_comparison":"Same prediction problem and shared features; tree explanations do not directly explain neural weights or outputs."},indent=2)+"\n")
        logger.info("Saved SHAP ranking and figure; max additivity error=%s",error);return 0
    except (OSError,ValueError,KeyError,RuntimeError,ImportError) as exc:
        logger.error("Explanation failed: %s",exc,exc_info=True);return 1


if __name__=="__main__":raise SystemExit(main())
