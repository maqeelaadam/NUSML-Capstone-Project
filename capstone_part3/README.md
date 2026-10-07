# Part 3 Machine learning and AI

Status: implementation plan only. No model has been trained or served.

Use the documented accident-risk **proxy**, because no accident data is supplied. Regression predicts traffic volume; no measured travel-time target is available. The shared predictor set includes time, weather, holiday flag and cyclical hour/day-of-week encodings. Exclude traffic volume and its derived labels from predictors.

Implement in this order:

1. `supervised/`: chronological timestamp-grouped split, train-fitted transformations, two regression algorithms and two classifiers; required evaluation metrics.
2. `unsupervised/`: interpreted K-means conditions and association rules predicting congestion, ranked by lift with support/confidence.
3. `deep_learning/` and `explainability/`: neural demand prediction plus SHAP/LIME. Explain a comparable-model choice if used.
4. `experiments/`: MLflow advanced-technique rationale and tracked parameters, metrics, model versions and experiments.
5. `recommendations/`: lower-traffic travel windows with day/weather context and readable recommendations.
6. `deployment/`: FastAPI model prediction simulation, input validation and example request/response.
7. `monitoring/`: reference/current feature or prediction-error distributions, justified thresholds and PASS/ALERT evidence.
8. `reports/`: final methodology/findings across all tasks, bias/fairness, governance/sustainability and versioned performance.

`configs/experiment_plan.json` records proposed choices. Install `requirements-ml.txt` when implementation begins, select a deep-learning library, and lock the tested environment. Export grader-readable MLflow evidence and document model retrieval before final submission. Runtime tracking stores and binary models are ignored at framework stage.
