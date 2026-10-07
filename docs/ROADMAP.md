# Implementation roadmap

The stages below are a proposed sequence, without assumed submission dates. Complete each stage with a meaningful commit and update REQUIREMENTS.md with links to evidence.

1. **Establish the framework** — folder structure, requirements, raw-file provenance, starter logging and input validation. This is the current stage.
2. **Audit the raw data** — confirm types, missingness, duplicates, repeated timestamps, impossible readings, holiday encoding and temporal coverage. Write the cleaning policy before changing data.
3. **Complete Part 1 analysis** — SQLite import and required queries; statistics and probability; explain denominator choices and coverage effects; build Power Query steps and the actual Power BI dashboard; finish the 1–2 page insights report.
4. **Complete Part 2 cleaning** — implement independently logged cleaning steps with monthly median loops where justified, save a cleaned observation table, and verify it end-to-end.
5. **Complete Part 2 features** — calendar helper, weather encodings, >=2 scaled fields and congestion categories; distinguish descriptive full-data features from training-fitted ML transformations.
6. **Complete Part 2 communication** — >=3 saved figures and interpretations, >=3 CLI queries and invalid-input handling, final sample pipeline log, 1–2 page report and run instructions.
7. **Complete Part 3 baselines** — chronological split manifest, train-fitted quartiles/scalers, documented severe-weather/visibility definitions, proxy labels, two algorithms for each supervised task, required metrics.
8. **Complete unsupervised and neural modelling** — traffic clusters, association rules, a neural demand model, and SHAP/LIME explanations. Verify sampling and runtime choices.
9. **Complete recommendations and MLOps** — MLflow tracking and exported evidence, model version registry, time-window recommendation engine, FastAPI prediction example, simulated drift and PASS/ALERT evidence.
10. **Complete portfolio and responsible AI** — evaluate errors by time/weather, governance and sustainability, final report, dashboard evidence, fresh-environment reproduction, required tracked outputs, grader access and Canvas submission.

Suggested commit messages: `Add SQLite traffic analysis`, `Add probability analysis`, `Add Power BI dashboard`, `Add logged data cleaning`, `Add train-fitted feature engineering`, `Add traffic figures`, `Add three-command traffic application`, `Add supervised baselines`, `Add clustering and association rules`, `Add neural demand prediction and explanations`, `Add MLflow and deployment simulation`, `Add final reports and reproduction evidence`.

Do not generate final findings, scores, screenshots, or reports before their underlying analysis has run.
