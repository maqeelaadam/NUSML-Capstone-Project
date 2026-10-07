# Smart City Traffic Intelligence

NUS School of Computing AMLDS capstone framework for historical westbound I-94 traffic analysis, reproducible Python analytics, and a simulated AI mobility solution.

**Status: framework established; capstone analysis and models are not yet complete.** This repository maps the supplied capstone brief into three connected workstreams. The starter pipeline validates input and records its profile; it does not yet clean data, train models, or produce final findings.

Start with [the roadmap](docs/ROADMAP.md), [the requirements checklist](docs/REQUIREMENTS.md), and [the analytical decisions](docs/DECISIONS.md).

## Project structure

```text
NUSML-Capstone-Project/
├── capstone_part1/          # SQLite, statistics, probability, Power BI, insights
├── capstone_part2/          # Python pipeline, features, figures, mini application
├── capstone_part3/          # ML, explainability, recommendations, MLOps
├── data/                   # Immutable raw data and generated data (ignored)
├── docs/                   # Requirements, roadmap, decisions, data dictionary
├── scripts/import_data.py  # Import the supplied CSV without modifying it
├── requirements.txt        # Analytics dependencies
├── requirements-ml.txt     # Later ML dependencies
└── .github/                # Task and pull request templates
```

The course brief explicitly names `capstone_part2` and `capstone_part3`; this framework uses corresponding names for all three parts. These map to the GitHub guide's illustrative `part1_data_analytics`, `part2_python`, and `part3_machine_learning` folders.

## Getting started

Use Python 3.11 or later. Run commands from the repository root.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/import_data.py --source "/path/to/Metro_Interstate_Traffic_Volume.csv"
python -m capstone_part2.pipeline
```

The import and starter pipeline use Python's standard library and can run before installing analytics dependencies. The raw CSV is intentionally ignored by Git; obtain it from your supplied file or the [UCI source](https://archive.ics.uci.edu/dataset/492/metro+interstate+traffic+volume). Course Word documents are not redistributed here.

The starter pipeline saves `data/processed/raw_profile.json` and logs to `capstone_part2/pipeline.log`. To inspect internal values:

```bash
python -m capstone_part2.pipeline --log-level DEBUG
```

`capstone_part2/feature_engineering.py` provides initial calendar features. Cleaning, weather encodings, fitted scaling, quartile targets, figures, and the mini application remain pending. See the Part 2 README for intended future commands.

## Logging

Every Python module declares `logging.getLogger(__name__)`. Handlers are configured only by entry points and write to the console and a file. Format: timestamp, level, logger/module name, message. INFO is the normal level; DEBUG appears only when selected. WARNING records recoverable changes with affected counts and reasons; ERROR records failures. The pipeline captures exception details and returns a nonzero exit status. Internal progress uses logging; `print()` is reserved for future CLI answers. The checked-in sample log demonstrates the **starter validation run**, not a completed cleaning pipeline.

## Modelling plan and limitations

Use chronological train/validation/test partitions and keep identical timestamps in one partition. Fit preprocessing and target quartiles on training data only. Use a common time, weather and holiday feature set for classification and regression; exclude traffic volume and labels derived from it as predictors. No accident dataset or travel-time target is supplied. Classification will demonstrate the specified **proxy accident-risk label**, never actual accident prediction. Recommendations concern travel timing on one corridor.

Part 3 will compare linear/logistic baselines with tree ensembles, add clustering and association rules, implement neural-network demand prediction with SHAP or LIME, and use MLflow, a FastAPI mock-up, and simulated drift alerts. These components are planned, not implemented.

## GitHub workflow

Commit each completed task with a descriptive message and push it. Use `codex/` branches for substantial changes and the pull request template for review. The initial framework commits are setup history; they do not substitute for incremental commits made while implementing the capstone. [Import and collaboration instructions](docs/GITHUB_WORKFLOW.md) include the local backup workflow.

## Data attribution

Hogue, J. (2019). *Metro Interstate Traffic Volume*. UCI Machine Learning Repository. https://doi.org/10.24432/C5X60B. Dataset licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). See [data/README.md](data/README.md) for provenance and the supplied file's checksum.
