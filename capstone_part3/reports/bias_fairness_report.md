# Bias Fairness Governance and Sustainability Report

This educational system supports historical traffic analysis and deployment simulation. It does not validate real accident prediction or justify autonomous safety decisions. Its strongest limitation is the combination of single-corridor sampling and a weather/congestion proxy target.

## Sampling and label limitations

The observations cover one westbound I-94 station near Minneapolis-St Paul from October 2012 to September 2018. Missing hours, partial years and seasonal/time differences limit generalisation to other roads, directions, climates or present-day conditions. Repeated weather records and sparse holiday labels require explicit aggregation choices. Weather severity selection and monthly median imputation simplify real conditions and can hide variability.

The classifier target combines traffic quartiles with selected severe-weather and low-visibility textual categories. There are no measured accidents, accident severity outcomes or actual visibility readings. Weather predictors partly define the proxy label, which helps explain very high performance. The reported F1 and AUC quantify reconstruction of this rule, not accident calibration. Snow, Haze and Mist do not all have equal severity in reality; these mapping choices need sensitivity analysis and external validation before any operational use.

## Uneven errors and uncertainty

On the chronological test set, regression MAE is approximately 189 vehicles/hour in Clear conditions, 401 in Snow and 626 in Fog. Weekend MAE is about 295 versus 195 on weekdays. Errors also vary by hour: at 03:00 MAE is about 32, compared with 351 at 16:00. Low-volume groups can have low absolute error while relative error remains large; evaluate both if decisions require it.

The holdout contains only two Smoke observations and no Squall observations, so apparent good performance in rare conditions cannot establish reliability. The group audit records counts; zero proxy F1 in a group with no positive labels should not be treated as evidence of poor positive-class performance. The dataset has no demographic or protected-attribute information. The project therefore audits operational conditions and coverage, and cannot establish demographic fairness.

## Governance and appropriate oversight

Human reviewers should approve target definitions, weather mappings, aggregation policies, imputation, intended use and release criteria. Preserve raw-file provenance, split dates, model versions, MLflow metrics and reproducible code. Restrict recommendations to timing on this corridor and show supporting sample counts. A real deployment would require current data, measured outcomes, privacy/access controls where relevant, validation outside the training geography/time, calibrated uncertainty and an incident-response owner.

Monitoring uses a transparent KS effect-size threshold and simulated PASS/ALERT outputs. Seasonal shifts can trigger distribution changes without harming predictions. An alert should prompt diagnosis of data quality, coverage, sensor change and observed error; it should not automatically retrain or silently replace a model. The present API is a local simulation and has no production authentication, service-level controls or live feeds.

## Sustainability and resource trade-offs

Bounded CPU experiments use two worker threads, 100-tree ensembles, a small two-hidden-layer neural model and fixed seeds. A feed-forward model avoids the extra sequence preparation and search cost of an LSTM at this stage. Runtime is recorded per experiment, but electrical energy and carbon emissions are not measured, so no numerical carbon claim is made. Prefer the smallest model that meets validated requirements, cache reproducible outputs, avoid repeated full training without a reason, and record any future larger hyperparameter search and deployment resource cost.

Source: project holdout metrics and group_error_audit.csv; Hogue (2019), UCI Metro Interstate Traffic Volume, DOI 10.24432/C5X60B. This is a methodological fairness assessment, not a certification of safety or equal outcomes.
