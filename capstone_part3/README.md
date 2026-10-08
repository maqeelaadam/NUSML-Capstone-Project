# Part 3 Machine learning and AI

The supervised models, neural demand network, clusters, rules, SHAP explanations, MLflow runs, recommendation engine, API simulation and drift checks have been implemented and run. All accident-risk classification metrics concern a documented proxy; no real accident dataset was sourced.

```bash
python -m capstone_part3.train
python -m capstone_part3.unsupervised.analyze
python -m capstone_part3.explainability.explain
python -m capstone_part3.monitoring.check
python -m capstone_part3.recommendations.engine --day-type weekday --weather Clear
python -m capstone_part3.deployment.api
```

Run after copying the supplied CSV and running the Part 2 pipeline. The root README lists the Python 3.12 setup and package versions. Training creates binary models under models/ and the local MLflow store under .runtime/mlruns. The checked-in artifacts/verified_models.zip archive includes all five trained models and their original MLflow run records. Follow the archive restoration commands in the root README to restore these without training and verify their checksums. The selected traffic-model alias and MLflow artifact copies are recreated from identical archived model bytes, with metadata relocated to the new checkout. results/model_comparison.json, split_manifest.json, label_definition.json, model_versions.csv and experiments/tracking_export.json supply evidence. The selected model is models/traffic_model.joblib, restored from the archive or rebuilt by the training command.

Chronological partitions contain 28,402 train, 6,086 validation and 6,087 test hours. Imputation, preprocessing and target quartiles are train-fitted. Model selection uses validation MAE/F1. Both tasks use a shared calendar/weather/holiday predictor set with cyclic hour and weekday encodings. The target volume and its derived labels are excluded from predictors. Five runs compare ridge/forest regressors, logistic/forest classifiers and a (64,32) ReLU demand network. The forest achieves test MAE about 224 and R² about 0.964; classifier F1 about 0.933 is only proxy performance.

Full-data clustering/rules are labelled descriptive. SHAP explains the comparable forest, with an additivity check, rather than claiming direct explanations of the neural model. Recommendations combine train-period mean traffic with illustrative model estimates and supporting counts. Drift simulation uses a documented KS effect-size threshold with an identical-data PASS control and injected-temperature ALERT case.

FastAPI serves POST /predict locally; request/response examples are in deployment/. Tests exercised valid and invalid requests. Actual deployment, live data and production controls are outside this educational simulation. reports/ contains final methodology/findings and bias/fairness/governance/sustainability reports in PDF and editable Markdown. See the root README for reproducibility and the documented macOS access limitation that prevented completion of the Power BI section.
