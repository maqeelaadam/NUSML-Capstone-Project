# Python Methodology and Findings Report

The reproducible workflow turns 48,204 supplied records into 48,187 cleaned observations and 40,575 hourly records, then saves engineered features and four traffic figures. It also supports three traffic queries with validated input. The raw dataset is preserved unchanged and identified by SHA-256.

## Loading and auditable cleaning

The loader checks all nine required columns before profiling or transformation. It preserves the literal no-holiday label `None`, rejects malformed CSV records, and uses explicit exception handling. Cleaning standardises categorical whitespace/case, parses timestamps, removes 17 exact duplicates, converts numeric fields, and identifies nonfinite, missing or impossible values. Ten temperature readings at 0 K and one rainfall value above 9,000 mm are imputed with monthly medians. Monthly processing explicitly loops over affected groups; fallback to a global reference median is available if a month has no valid reference. Invalid measured traffic targets are dropped rather than invented; valid zero traffic is retained. The broad upper temperature threshold of 350 K is a validation guard, not a calibrated sensor specification.

Repeated timestamps have matching traffic targets. The hourly table averages numeric weather values and selects the most severe reported weather category using a documented ordering. This combines 7,612 extra records without summing repeated hourly counts. Holiday labels occur sparsely at individual hours; date-level propagation changes 1,150 rows and is recorded explicitly. Both the cleaned observation table and hourly table are saved so the transformation remains reviewable.

## Feature engineering and figures

Features include hour, weekday, weekend, month, holiday flag, sine/cosine encodings for hour and weekday, Celsius temperature, severe-weather and textual low-visibility indicators, and one-hot weather columns. Temperature and cloud cover have standardised versions. The descriptive table includes fixed traffic categories for Part 1 and separately named quartile congestion categories. Full-dataset statistics describe historical data; Part 3 re-fits imputers, scales, encoders and quartiles using training data only.

Four Matplotlib outputs show hourly demand, weekday/weekend differences, weather-category averages and temperature-volume scatter. Peak mean demand occurs at 16:00 (5,709 vehicles/hour), compared with 373 at 03:00. Weekday mean traffic is 3,557 versus 2,624 on weekends. Weather comparisons depend on timing, severity aggregation and rare-category sample sizes; temperature shows broad traffic variation at similar readings. Each figure has a saved interpretation.

## Logging application and validation

Every module declares a named logger. Entry points configure console and file handlers with timestamp, level, module and message. INFO captures loaded shapes, stage milestones and saved file paths; WARNING records changed counts and reasons; DEBUG records monthly medians, quartiles and scale values only when requested. ERROR captures pipeline exceptions and returns failure gracefully. The checked-in pipeline.log is actual end-to-end output. Internal progress does not use print statements.

The mini application implements `at --datetime`, `high-traffic --threshold --limit`, and `compare-day-types`. Each command logs its arguments; direct answers are printed for the end user. All three commands were exercised on generated features. A malformed date produces a clear ERROR and failure status. Nine acceptance checks cover schema rejection, no-holiday preservation, train-only imputation, conflicting hourly targets, timestamp split isolation, quartile boundaries, invalid CLI input, API requests and drift controls. These checks passed. The workflow and environment are documented for reproduction; figures, interpretations and sample logs are tracked in GitHub.

Limitations: monthly medians and severe-category selection are explicit analytical choices; hourly gaps remain. The workflow estimates historical traffic on one corridor and cannot establish accident risk or real-time travel safety.
