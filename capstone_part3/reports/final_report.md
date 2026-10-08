# Smart City Traffic Intelligence Final Capstone Report

This project implements historical traffic analysis, a logged Python workflow, and a simulated AI mobility solution for westbound I-94. The traffic random forest outperforms the linear baseline on chronological holdout evaluation. The recommendation component combines historical training-period demand with model estimates, while API and monitoring components demonstrate deployment practices. This report covers all analytical tasks completed to date. The actual Power BI dashboard and its interactive validation remain unfinished, so the portfolio is not yet a complete final submission.

## Data lineage and analytics

The supplied 48,204-row, nine-column dataset contains 17 exact duplicates, 10 zero-Kelvin readings and one rainfall value of 9,831.3 mm. The pipeline preserves raw data, removes exact duplicates, and uses monthly medians for invalid weather values. At repeated timestamps traffic readings agree; the hourly view averages numerical weather readings and selects the most severe recorded category. It produces 40,575 distinct hours. Sparse holiday labels are propagated only within observed labelled dates. Coverage spans October 2012 to September 2018 with substantial gaps.

SQLite outputs include raw-record and hourly annual totals for 2012-2017, absolute/percentage changes, coverage and holiday temperatures. Low 2014/2015 totals reflect incomplete coverage, while 2017 captures 99.5% of expected hours. New Year's Day 2015 lacks a labelled observation. The Part 1 report presents the raw-file SQLite results first: mean traffic 3,259.82, median 3,380, sample SD 1,986.86, sample variance 3,947,615.32 and range 7,280; temperature correlation is 0.130299 and the clear/cloudy congestion odds ratio is 0.735388. Congestion, Clear, joint, Clear-given-congestion and high-temperature-given-congestion probabilities are 14.73%, 27.78%, 3.66%, 24.83% and 26.30%. The supplementary cleaned hourly view gives mean 3,290.65 and correlation 0.139; its different aggregation and denominator are explicitly labelled. Primary SQL and complete holiday/year comparisons are in requested_raw_analysis.sql and raw_sql_answers.md. Four figures and Power BI import/measure files support communication, but a PBIX dashboard has not been created.

## Features labels and evaluation

Calendar inputs include hour, day of week, month, weekend, holiday flag and cyclic sine/cosine encodings for hour and weekday. Weather inputs include Kelvin temperature, rainfall, snowfall, cloud cover and one-hot weather category. Predictor lists exclude measured traffic volume, congestion category and proxy target.

The classifier's label is High/Severe quartile congestion AND severe/low-visibility weather. Severe weather is defined as Thunderstorm, Squall or Snow; low-visibility indicators use Fog, Mist, Haze or Smoke. These are textual category assumptions rather than measured visibility. Quartile thresholds are fit on training traffic; the label definition is saved. Weather also helps define the target, so high classification scores demonstrate rule approximation rather than actual accident likelihood. No real accident or travel-time dataset was sourced.

Unique timestamps are divided chronologically into 28,402 training hours through 2017-05-10 04:00, 6,086 validation hours through 2018-01-19 14:00, and 6,087 later test hours through 2018-09-30. Duplicate-hour records stay in one partition. Weather imputation references, scaling, encoding and target quartiles use training data only. The validation partition selects the lowest-MAE regressor and highest-F1 classifier; test metrics are reported without selecting on them. Neural internal early stopping uses only the training partition. Because current weather is supplied, these are retrospective or conditional estimates; future forecasting requires weather forecasts and clearer availability assumptions.

## Supervised comparison and neural demand model

| Model | Validation MAE or F1 | Test MAE or F1 | Test R² or AUC |
| --- | --- | --- | --- |
| ridge regression | 803.29 MAE | 804.84 MAE | 0.7345 R² |
| random forest regression | 248.27 MAE | 223.76 MAE | 0.9637 R² |
| logistic proxy classifier | 0.8865 F1 | 0.8331 F1 | 0.9939 AUC |
| random forest proxy classifier | 0.9625 F1 | 0.9326 F1 | 0.9978 AUC |
| neural demand network | 267.53 MAE | 245.14 MAE | 0.9613 R² |


The selected random forest uses 100 trees, maximum depth 18 and minimum leaf size 4. Ridge alpha is 1.0; the logistic baseline uses balanced class weights. The forest proxy classifier also uses balanced weights. The neural demand network has hidden layers of 64 and 32 ReLU units, a scaled traffic target, a maximum of 160 iterations, early stopping and seed 42. It is a feed-forward neural network trained by backpropagation, fulfilling the neural demand-prediction option. An LSTM was not selected because irregular coverage and repeated-hour handling would require additional sequence assumptions. Saved run evidence contains convergence warnings, if any, and runtime per model.

| Classifier | Accuracy | Precision | Recall | F1 | ROC AUC |
| --- | --- | --- | --- | --- | --- |
| logistic proxy classifier | 0.9566 | 0.7179 | 0.9925 | 0.8331 | 0.9939 |
| random forest proxy classifier | 0.9844 | 0.8819 | 0.9895 | 0.9326 | 0.9978 |


These classifier metrics refer only to the constructed proxy. Class prevalence, weather-rule dependence and sampling limitations limit their interpretation. Required regression and classification metrics are saved in machine-readable comparison files.

## Unsupervised patterns

K-means uses four clusters on scaled traffic volume, cyclic hour and weather severity. Cluster 0 contains 10,618 hours, averages 1,173 vehicles/hour, and has a 0.8% low-visibility fraction.
Cluster 1 contains 12,450 hours, averages 4,823 vehicles/hour, and has a 14.4% low-visibility fraction.
Cluster 2 contains 11,592 hours, averages 4,525 vehicles/hour, and has a 5.7% low-visibility fraction.
Cluster 3 contains 5,915 hours, averages 1,448 vehicles/hour, and has a 42.8% low-visibility fraction. The two high-demand clusters distinguish daytime patterns; the lower-demand clusters differ in weather/visibility prevalence. Mean arithmetic hour can hide midnight wrapping, so cyclic features drive clustering. A 2,000-hour reproducible sample supplies the silhouette score. Four clusters are a descriptive starting choice, not an asserted optimum.

Association mining discretises time bands, weekday/weekend, weather and quartile congestion. Support is at least 3%, confidence at least 50%, and itemsets contain at most three terms. Rules with only congestion outcomes are ranked by lift. Weekend overnight hours imply Low congestion in 89.6% of matching observations, with lift 3.59 and support 6.4%; this is a strong descriptive pattern, not a causal relationship. Nineteen eligible rules are saved with interpretations. Full-data discovery is labelled descriptive and is separate from supervised holdout evaluation.

## Explainability and advanced technique

SHAP explains the comparable random-forest traffic model on 150 reproducibly sampled test hours using the same problem and feature set as the neural network. Hourly/cyclic time features have the largest mean absolute contributions. An additivity check reconstructs forest predictions with a maximum error below 1e-9. These explanations concern the forest; they do not directly explain neural weights or establish causality. Weather and time features can be correlated, affecting attribution.

MLflow is the selected advanced technique. Five real training runs record parameters, validation/test metrics, runtime, model version, saved model artifacts and split metadata. tracking_export.json preserves grader-readable run IDs and metrics. The checked-in verified_models.zip submission archive contains all five trained models and the original MLflow run records for those evaluations. The restoration command recreates the selected traffic-model alias and MLflow artifact copies, relocates metadata to the reader's checkout, and verifies file checksums. Retraining remains available. MLflow improves experiment comparison and traceability, but it does not by itself validate labels, data quality, fairness or operational readiness. model_versions.csv distinguishes baseline, forest and neural release candidates, while each algorithm artifact starts at version v1.

## Recommendations deployment and monitoring

The timing engine filters training-period hourly profiles by day type, weather and user-selected hours, requiring at least 20 supporting observations. It ranks windows by equal weighting of historical mean and a model estimate under an explicitly illustrative training-calendar scenario with mean weather inputs. For the default weekday/Clear window 06:00-22:00, it recommends 21:00-22:00, with historical mean 2,733 and model estimate 2,413 vehicles/hour. It returns the supporting count and a plain-language explanation. The dates, weather averages and equal weighting are demonstration choices, and the output is not a live-traffic or safety guarantee.

The local FastAPI mock-up accepts a timestamp, weather readings/category and holiday label and returns a traffic prediction. Input checks reject impossible temperature, invalid categories, timezone-aware timestamps and non-hourly times. Missing model artifacts yield a service-unavailable response. A test client verified valid prediction and rejected malformed inputs; an example response is tracked. Serving is bound locally and has not been deployed to a public service.

Monitoring compares reference and current feature distributions using the two-sample KS statistic. An effect size above 0.20 triggers ALERT; p-values are displayed but do not independently drive decisions. The identical-reference control passes, the later-period comparison passes, and a deliberately injected +20 K shift triggers ALERT. This threshold is a classroom heuristic requiring operational calibration; detected seasonal shifts need investigation and do not automatically imply worse prediction accuracy.

## Responsible AI reproducibility and remaining work

Test regression MAE differs across conditions: roughly 189 in clear weather, 401 in snow and 626 in fog. Weekend MAE is about 295 versus 195 on weekdays. Rare groups have too few observations for dependable comparisons; protected-attribute fairness cannot be evaluated from this dataset. The separate bias/fairness report discusses coverage, proxies, oversight, sustainability and error variation.

The end-to-end pipeline, all three CLI commands, model training, rules, SHAP, recommendations and monitoring have run. Nine acceptance checks passed. Requirements are pinned in the tested Python 3.12 environment. README commands regenerate datasets or restore the checked-in trained models and original MLflow records without retraining. Sample logs, figures, metrics, report files and incremental task commits provide review evidence. Remaining work is to author and validate the actual Power BI dashboard, review analytical choices against instructor expectations, and perform the final submission/access check. Nothing has been submitted to Canvas.

## References

Hogue, J. (2019). Metro Interstate Traffic Volume. UCI Machine Learning Repository. DOI 10.24432/C5X60B. CC BY 4.0. Python Logging HOWTO: https://docs.python.org/3/howto/logging.html. Neural network model documentation: https://scikit-learn.org/stable/modules/neural_networks_supervised.html. MLflow tracking: https://mlflow.org/docs/latest/ml/tracking/. SHAP TreeExplainer: https://shap.readthedocs.io/en/latest/generated/shap.TreeExplainer.html. Association rules: https://rasbt.github.io/mlxtend/user_guide/frequent_patterns/association_rules/.
