# Smart City Traffic Intelligence

NUS School of Computing AMLDS capstone using the Metro Interstate Traffic Volume dataset to analyse historical westbound I-94 demand, build a reproducible Python pipeline, and simulate an AI mobility solution.

**Status: SQL analysis and Python/ML workflows implemented and verified. The Power BI section was not completed because of my macOS access limitation; final course submission is pending.** The supplied capstone instructions and GitHub guide were reviewed before implementation. No accident dataset was supplied: classification uses a documented weather/congestion **proxy**, never a validated prediction of actual accidents.

## Start here

- [Current status and remaining work](docs/STATUS.md)
- [Course requirements and evidence](docs/REQUIREMENTS.md)
- [Submission review and saved-model instructions](docs/SUBMISSION_REVIEW.md)
- [Analytical definitions and decisions](docs/DECISIONS.md)
- [Part 1 insights report](capstone_part1/reports/insights_report.pdf)
- [Part 2 methodology report](capstone_part2/reports/methodology_report.pdf)
- [Capstone report across all tasks](capstone_part3/reports/final_report.pdf)
- [Bias, fairness and sustainability report](capstone_part3/reports/bias_fairness_report.pdf)

## What works

Part 1 supplies verified SQLite loading, annual/holiday outputs, statistics, correlation, required congestion probabilities and odds ratio. 

Part 2 loads and validates the raw CSV, logs each cleaning stage, engineers calendar/weather/scaled features, saves four figures with interpretations, and runs three traffic-query commands. It produces 48,187 cleaned observations and 40,575 hourly records from 48,204 raw observations.

Part 3 compares two regressors and two proxy classifiers, trains a two-hidden-layer neural demand model, produces four traffic clusters and association rules, applies SHAP to a comparable tree model, records five real MLflow experiments, recommends travel windows using historical data and model estimates, serves a local FastAPI prediction simulation, and demonstrates PASS/ALERT drift monitoring.

On the chronological test set, the selected forest's traffic MAE is about 224 vehicles/hour with R² 0.964; the neural model's MAE is about 245. Models were selected using validation performance. These are historical conditional estimates with observed weather, not real-time forecasts. Nine acceptance checks passed.

## Power BI access limitation

I use macOS and do not have access to Power BI Desktop in my current setup. I was therefore unable to complete Part 1 Task 4, the Power BI section. Power BI preparation files and dashboard-specific outputs are excluded from this submission.

## Project structure

```text
capstone_part1/   SQLite queries, analysis script, results and report
capstone_part2/   Logged cleaning/features/figures pipeline and mini application
capstone_part3/   Models, SHAP, rules, recommendations, API, monitoring, reports
scripts/         Data import and complete reproduction commands
tests/           Schema, leakage, CLI, API and monitoring acceptance checks
data/            Provenance; raw and generated datasets ignored by Git
docs/            Requirements, decisions, status and GitHub workflow
.github/         Task and pull request templates
```

Folder names follow the brief's explicit `capstone_part2` and `capstone_part3` deliverable names. They correspond to the GitHub guide's illustrative part1_data_analytics / part2_python / part3_machine_learning layout.

## Reproduce

Use **Python 3.12** and run from the repository root. The tested environment is pinned in requirements-lock.txt. Raw data and extracted binary models are not committed individually. The verified_models.zip archive contains the five saved models and original MLflow records; restoration is available without retraining. The commands below regenerate the full workflow.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-lock.txt
python scripts/import_data.py --source "/path/to/Metro_Interstate_Traffic_Volume.csv"
python scripts/reproduce.py
```

To run stages separately:

```bash
python -m capstone_part2.pipeline
python -m capstone_part1.run_requested_sql
python -m capstone_part1.analyze
python -m capstone_part3.train
python -m capstone_part3.unsupervised.analyze
python -m capstone_part3.explainability.explain
python -m capstone_part3.monitoring.check
python -m capstone_part3.recommendations.engine
python -m unittest discover -s tests -v
```

Reports are checked-in results from the verified runs. Re-running workflows changes result files; review and regenerate reports if numerical outputs change. The current reports are authored reviewable documents, not automatically refreshed by reproduce.py.

## Review saved models without retraining

```bash
python scripts/submission_artifacts.py restore
python scripts/submission_artifacts.py verify
```

Restoration checks every archived file hash, restores the five models plus the selected-model alias, and reconstructs the five original MLflow runs at the new checkout location. The API can then run immediately. Dataset queries still require importing the CSV and running the Python pipeline. See [submission review instructions](docs/SUBMISSION_REVIEW.md).

## Traffic application and API

```bash
python -m capstone_part2.mini_app at --datetime "2017-01-01 12:00:00"
python -m capstone_part2.mini_app high-traffic --threshold 5500 --limit 10
python -m capstone_part2.mini_app compare-day-types
python -m capstone_part3.recommendations.engine --day-type weekday --weather Clear --earliest 6 --latest 22
python -m capstone_part3.deployment.api
```

The API starts locally at http://127.0.0.1:8000. Its interactive documentation is at `/docs`; POST `/predict` using capstone_part3/deployment/example_request.json. A verified response is supplied alongside it. No public service has been deployed.

## Logging and model records

Every module uses `logging.getLogger(__name__)`. Entry points configure console and file handlers, with timestamp, log level, module/logger name and message. INFO covers milestones, shapes and save paths; WARNING covers recoverable changes with counts/reasons; ERROR covers failures; DEBUG captures internal values only with `--log-level DEBUG`. Internal progress uses logging; print is reserved for CLI answers. The checked-in `capstone_part2/pipeline.log` is a genuine completed pipeline run. Other logs are generated under their respective part folders.

Training stores MLflow runs under `.runtime/mlruns` and exports grader-readable records to capstone_part3/experiments/tracking_export.json. Saved models go under capstone_part3/models and are rebuilt by the training command. The exported JSON can be inspected without a tracking server. An interactive MLflow UI requires the full MLflow distribution; the pinned environment uses mlflow-skinny for programmatic tracking. model_versions.csv records candidate releases and selection; extracted model files, runtime stores and generated datasets are ignored; the portable submission archive is checked in under capstone_part3/artifacts/.

## Important assumptions

Primary Part 1 SQL answers use all 48,204 raw CSV records. The 1-2 page insights report and final report use these results consistently; supplementary hourly outputs are labelled separately. Parts 2 and 3 use one record per observed hour. Traffic values match at repeated timestamps; numeric weather readings are averaged and the highest-severity weather category is selected. Missing hours remain missing. Holiday labels are propagated only within dates with an observed holiday label. These choices and alternative raw-record results are documented.

Part 1 congestion is always volume >5500. Parts 2/3 use data-driven quartile categories. ML partitions are chronological, with identical timestamps kept together; imputation references, scalers, encoders and label quartiles are fitted on training data only. Inputs exclude traffic targets and their derived labels. Recommendations concern timing on one corridor; the proxy, API, and monitoring require further validation before operational use.

## GitHub and submission

Continue with descriptive commits for coherent tasks. [GitHub workflow](docs/GITHUB_WORKFLOW.md) explains the ZIP and Git bundle backups. Review the reports and documented macOS access limitation before submitting the repository URL through Canvas. No grader invitation or Canvas submission has been sent.

## Dataset licence

Dataset licensing and provenance details are recorded in [data/README.md](data/README.md). Course Word documents are not redistributed.
