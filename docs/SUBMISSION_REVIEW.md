# Submission review guide

The completed non-Power-BI sections are prepared for review. Power BI is still required by the course brief; a specification is not a finished dashboard. No Canvas submission has been made.

## Start with the reports

- Part 1: capstone_part1/reports/insights_report.pdf (1-2 pages), with complete SQL answers in raw_sql_answers.md.
- Part 2: capstone_part2/reports/methodology_report.pdf (1-2 pages).
- Part 3: capstone_part3/reports/final_report.pdf and bias_fairness_report.pdf.
- Full task mapping: docs/REQUIREMENTS.md.

Part 1 primary answers use 48,204 unchanged CSV records. The cleaned 40,575-hour view is supplementary in Part 1 and used in Parts 2/3. Neither set of results should be mixed with the other's denominator. Missing New Year's Day 2015 evidence is explicitly recorded rather than invented.

## Inspect the original model and tracking evidence

The committed capstone_part3/artifacts/verified_models.zip archive contains all five saved model pipelines and original MLflow params, metrics, tags, split metadata and evaluation records for the five reported runs. Its manifest identifies model/run relationships, every file's SHA-256, and the selected-regressor alias. Duplicate model copies are reconstructed from the same bytes during restoration.

From a repository checkout with the pinned environment installed:

```bash
python scripts/submission_artifacts.py restore
python scripts/submission_artifacts.py verify
python -m capstone_part3.deployment.api
```

Restoration reconstructs .runtime/mlruns and capstone_part3/models, updating file URIs to the current checkout. Training is not needed to inspect saved models, tracking records or the API. Original training timestamps and numerical metrics remain unchanged. The archive omits earlier exploratory runs and includes exactly the five runs reported in tracking_export.json. The pinned mlflow-skinny installation supports programmatic tracking inspection; an optional visual MLflow UI requires the full MLflow package.

Dataset-dependent CLI queries and complete reproduction also require importing the supplied CSV. The root README provides these commands. `scripts/reproduce.py` runs the primary SQLite answers as well as the supplementary hourly analysis and all implemented Python/ML stages. Reports are checked-in verified results, not automatically refreshed after retraining. To regenerate all four report PDFs from their Markdown, use `python scripts/render_reports.py`.

## Before course submission

1. Read and be able to explain aggregation, monthly median imputation, chronological evaluation and the weather/congestion proxy. The classifier does not predict observed accidents.
2. Complete and validate the actual Power BI dashboard, save the PBIX and visual evidence, and update the outstanding status in the reports and requirement map.
3. Verify grader access and submit the repository link through Canvas according to the instructor's instructions.
