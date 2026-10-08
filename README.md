# Smart City Traffic Intelligence

NUS School of Computing AMLDS capstone using the supplied Metro Interstate Traffic Volume dataset to analyse historical westbound I-94 demand, build a Python pipeline and simulate an AI mobility solution.

SQL, Python and ML work is implemented and evaluated. Part 1 Task 4 was not completed: I use macOS and do not have access to Power BI Desktop in my current setup. Power BI preparation files and dashboard-specific outputs are excluded. No real accident dataset was supplied; classification uses a documented weather/congestion proxy. Course submission remains pending.

## Project structure and reports

- `capstone_part1/`: SQLite queries, numerical results and the [insights report](capstone_part1/reports/insights_report.pdf). [Detailed SQL answers](capstone_part1/reports/raw_sql_answers.md) explain all requested calculations.
- `capstone_part2/`: required cleaning/features/figures pipeline, local data, three-command application, sample pipeline.log and [methodology report](capstone_part2/reports/methodology_report.pdf).
- `capstone_part3/`: supervised and neural models, clusters, rules, SHAP, MLflow evidence, recommendations, deployment and monitoring simulations, [final report](capstone_part3/reports/final_report.pdf) and [bias/fairness report](capstone_part3/reports/bias_fairness_report.pdf).
- `.gitignore`: excludes local environments, datasets, runtime files and credentials from GitHub.

## Setup

Use Python 3.12. Run all commands from the repository root. The following direct package versions were used for the verified results. Dependency versions can also affect reproduction.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install numpy==2.5.3 pandas==3.0.6 matplotlib==3.11.2 scikit-learn==1.9.1 scipy==1.18.1 joblib==1.6.0 mlflow-skinny==3.17.0 fastapi==0.142.3 uvicorn==0.54.0 shap==0.52.0 mlxtend==0.25.0 PyYAML==6.0.3
mkdir -p capstone_part2/data/raw
cp "/path/to/Metro_Interstate_Traffic_Volume.csv" capstone_part2/data/raw/
```

Replace the example CSV path with its actual location. The original and generated datasets stay local. The pipeline validates columns before cleaning. The supplied file contains 48,204 rows and nine columns; SHA-256 is `749c90d720360a4215bb15345526073c079ba4cc95e3fa558796d083f85fce9e`.

## Run the analysis and models

```bash
python -m capstone_part1.run_requested_sql
python -m capstone_part2.pipeline
python -m capstone_part1.analyze
python -m capstone_part3.train
python -m capstone_part3.unsupervised.analyze
python -m capstone_part3.explainability.explain
python -m capstone_part3.monitoring.check
python -m capstone_part3.recommendations.engine
```

Part 1's primary SQL answers use the original 48,204 records. The supplementary hourly analysis runs after the Python pipeline. Part 2 saves cleaned observations, hourly traffic and descriptive features under `capstone_part2/data/processed/`; the final feature table has 40,575 rows and 35 columns. Training regenerates models and MLflow records. Reports contain reviewed results and must be reviewed and updated if a new run changes the findings; they do not update automatically.

## Use the application

```bash
python -m capstone_part2.mini_app at --datetime "2017-01-01 12:00:00"
python -m capstone_part2.mini_app high-traffic --threshold 5500 --limit 10
python -m capstone_part2.mini_app compare-day-types
python -m capstone_part3.recommendations.engine --day-type weekday --weather Clear --earliest 6 --latest 22
python -m capstone_part3.deployment.api
```

The local API starts at http://127.0.0.1:8000; interactive documentation is at `/docs`. POST `/predict` accepts the supplied example in `capstone_part3/deployment/example_request.json`. Models must first be trained or restored. No public service has been deployed. Recommendations use historical observations and illustrative model estimates for one corridor.

## Restore the submitted models without retraining

The archive `capstone_part3/artifacts/verified_models.zip` contains all five trained models and their original MLflow records. The code below validates the archive and member checksums, restores files and selected-model copies, and relocates MLflow paths. Run it from the repository root after setup. The archive's original manifest mentions the former environment filename as historical metadata; current setup instructions are above.

```bash
python - <<'PYRESTORE'
from pathlib import Path, PurePosixPath
import hashlib, json, shutil, zipfile
root = Path.cwd()
archive = root / 'capstone_part3/artifacts/verified_models.zip'
summary = json.loads(archive.with_name('archive_summary.json').read_text())
assert hashlib.sha256(archive.read_bytes()).hexdigest() == summary['archive_sha256']
with zipfile.ZipFile(archive) as z:
    manifest = json.loads(z.read('manifest.json'))
    for entry in manifest['files']:
        name, data = entry['path'], z.read(entry['path'])
        assert not PurePosixPath(name).is_absolute() and '..' not in PurePosixPath(name).parts
        assert len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256']
    for entry in manifest['files']:
        name, data = entry['path'], z.read(entry['path'])
        target = root / name
        assert target.resolve().is_relative_to(root.resolve())
        target.parent.mkdir(parents=True, exist_ok=True)
        if name.startswith('.runtime/mlruns/') and name.endswith('/meta.yaml'):
            lines = data.decode().splitlines()
            lines = [('artifact_location: ' + target.parent.as_uri()) if line.startswith('artifact_location:') else
                     ('artifact_uri: ' + (target.parent / 'artifacts').as_uri()) if line.startswith('artifact_uri:') else line for line in lines]
            data = ('\n'.join(lines) + '\n').encode()
        target.write_bytes(data)
    for entry in manifest['copies']:
        target = root / entry['destination']
        assert target.resolve().is_relative_to(root.resolve())
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / entry['source'], target)
print('Restored five models and their original MLflow records.')
PYRESTORE
```

The API can then run without retraining. Dataset queries still require the supplied CSV and Part 2 pipeline. `capstone_part3/experiments/tracking_export.json` contains readable experiment records; `model_versions.csv` records the candidates and selection. The pinned MLflow package supports programmatic tracking; an interactive MLflow UI requires the full MLflow distribution.

## Logging

Every Python module uses `logging.getLogger(__name__)`. Entry points configure console and file handlers with timestamp, level, module and message. INFO records milestones, shapes and saved paths; WARNING records recoverable changes with counts and reasons; ERROR describes failures; DEBUG records internal values when requested. Run `python -m capstone_part2.pipeline --log-level DEBUG` for detailed pipeline logging. Internal progress uses logging; the application prints answers for users.

The required `capstone_part2/pipeline.log` is a completed sample run. Other modules generate logs within their respective capstone folders. MLflow writes experiment records under `.runtime/mlruns`.

## Findings and analytical assumptions

The data spans October 2012 to September 2018 with gaps. Raw-record annual totals repeat some hourly traffic counts and depend on coverage. The pipeline removes 17 exact duplicates and imputes invalid weather using monthly medians. At repeated timestamps, traffic readings agree; numeric weather is averaged and the highest-severity recorded category is selected. Missing hours remain missing. Holiday labels propagate only within dates with an observed label. Details are in the required reports.

Part 1 defines congestion as volume >5,500, high temperature as >292 K, clear weather as Clear and cloudy weather as Clouds. Parts 2/3 use traffic quartile categories. ML partitions are chronological; imputation, preprocessing and label thresholds use training data only. Model selection uses validation performance. Predictors exclude measured traffic and its derived target labels.

The selected random forest's test MAE is about 224 vehicles/hour and R² is 0.964; neural MAE is about 245. The proxy classifier models High/Severe quartile congestion together with severe or low-visibility weather. Severe weather means Thunderstorm, Squall or Snow; low visibility means Fog, Mist, Haze or Smoke. These are textual indicators. Proxy performance is not validated accident prediction, and observed weather supports conditional historical estimates rather than live forecasts.

## Dataset attribution

Hogue, J. (2019), Metro Interstate Traffic Volume, UCI Machine Learning Repository, https://doi.org/10.24432/C5X60B. The dataset is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This attribution accompanies use of the supplied data. Course Word documents are not redistributed.

## Submission

The repository contains incremental, descriptive commits as requested by the assignment. Review the reports, confirm grader access, and submit the repository URL through Canvas with the completed submission form. The Power BI access limitation is recorded above. Nothing has been submitted to Canvas.
