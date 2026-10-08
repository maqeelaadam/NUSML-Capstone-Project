# Analytical decisions and assumptions

These document the implemented choices and remaining review points, rather than extra requirements from the course brief.

## Data integrity and coverage

Preserve the raw file unchanged and identify it by SHA-256. Raw data contains 48,204 observations, nine columns, 40,575 unique timestamp strings, and 17 exact duplicate rows. Repeated timestamps are not necessarily duplicate observations: weather descriptions can produce multiple records for an hour. Remove exact duplicates separately from choosing one record per hour.

Create two explicitly documented views if needed: a cleaned observation table and an hourly table. For hourly analysis, investigate conflicting traffic values and weather records before selecting an aggregation rule. Do not sum repeated readings as if they were separate hours. Report row counts and unique hours together.

The supplied file spans 2012-10-02 through 2018-09-30. Audit missing hours and partial years before interpreting 2012–2017 annual totals. Holiday labels may not mark every hour of a holiday; compare labelled observations first, then document any date-level propagation. Preserve `holiday='None'` as a valid no-holiday category rather than letting CSV parsing treat it as missing.

Zero Kelvin and rainfall above 9000 mm require investigation. Use monthly median imputation where appropriate, explicitly loop by month, and log each affected count and reason. A 9000 mm flag reproduces the brief's example; it is not a claim that all smaller values are physically plausible. Set more useful validation limits only with justification. Zero traffic can be valid; do not replace it solely because it is zero. Retain genuine extremes unless evidence supports treating them as errors.

UCI describes timestamps as local CST. Preserve supplied local timestamps and do not silently convert to Bangkok time, UTC, or daylight-saving time.

## Definitions

Use `traffic_category_fixed` for Part 1 (Low <4500, Medium 4500–5500, High >5500), and `congestion_category_quartile` for Part 2/3 (<=Q1, <=Q2, <=Q3, >Q3). Part 1 congestion probability always uses volume >5500; high temperature always uses >292 K. Define clear as weather_main `Clear` and cloudy as `Clouds`, explicitly excluding other categories from the clear/cloudy odds-ratio table. State denominators and handle zero contingency cells.

Specify sample vs population variance/SD in the report. Explain that weather–traffic correlation is observational and can reflect time-of-day/seasonal effects.

The supplied proxy code references undefined `SEVERE_WEATHER` and `is_low_visibility`. Propose documented configurable severe-weather categories and fog/mist visibility indicators after auditing category values. No measured visibility field exists, so describe this as an indicator based on textual weather categories.

## Evaluation and leakage

Prefer chronological train/validation/test splits (proposed 70/15/15 by unique timestamps). Keep equal timestamps together, record cutoff dates, and assess temporal gaps. Fit imputation, scaling, encoders, quartiles and model selection on training data only. A whole-data descriptive feature table is not automatically safe for ML training.

Regression predicts traffic volume because no travel-time target exists. Use time, holiday and weather features available at the stated prediction moment. Observed current weather supports a retrospective estimate; a genuine future forecast needs weather forecasts or clearly stated assumptions.

Classification target: High/Severe quartile congestion AND severe/low-visibility weather. Exclude traffic_volume, congestion labels and other target-derived values from predictors. Weather inputs partly define this proxy; report that dependence and do not equate proxy performance with real accident prediction. Compute ROC AUC from scores/probabilities; if a partition has one class, report undefined AUC rather than inventing a value.

Start with a small feed-forward neural demand model; consider LSTM only after handling irregular hours, repeated timestamps and sequence boundaries. MLflow is the proposed advanced technique and remains required for experiment tracking under Task 6. Use bounded experiments and record runtime/resource trade-offs.

## Delivery boundaries

Travel recommendations concern timing on a single corridor. API deployment and monitoring are simulations. Actual Power BI authoring is a separate deliverable: this scaffold supplies a specification, not a completed dashboard. The checked-in submission archive contains all five saved models and the original records for the five reported MLflow runs. Extraction verifies hashes and relocates MLflow metadata to the reader's checkout. Runtime files remain ignored; model and run evidence are available without retraining.

## Implemented weather and recommendation choices

Severe weather uses Thunderstorm, Squall and Snow. Low-visibility categories use Fog, Mist, Haze and Smoke; these are textual proxies, not measured visibility. Highest-severity category selection per hour is defined in cleaning.py. Numeric validation also flags temperature >350 K as a broad guard. Imputation uses month-of-year medians from the appropriate reference data. The recommendation engine combines historical mean and an illustrative model estimate equally; it uses training-calendar weekday/weekend scenarios with mean weather inputs and at least 20 observed hours per candidate.
