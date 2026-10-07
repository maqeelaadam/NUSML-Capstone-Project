# Part 2 Reproducible Python pipeline

Status: working input-validation scaffold; cleaning, full features, figures and application are pending.

Run from the project root:

```bash
python scripts/import_data.py --source /path/to/Metro_Interstate_Traffic_Volume.csv
python -m capstone_part2.pipeline
python -m capstone_part2.pipeline --log-level DEBUG
```

The starter validates all nine columns before profiling and writes `data/processed/raw_profile.json`. It preserves raw data and logs to console plus `capstone_part2/pipeline.log` with timestamp, severity, logger name and message. Named module loggers are used; only entry points configure handlers. INFO is default; DEBUG is opt-in. Cleaning changes must eventually use WARNING with counts/reasons; failures use ERROR and a nonzero status. The checked-in pipeline.log is genuine output from starter validation and must be replaced by a completed cleaning/feature/figure run before submission.

## Interfaces to implement

- `cleaning.py`: categorical mappings, time parsing, missing/impossible readings, exact duplicate removal, justified monthly median loops and per-step logs.
- `feature_engineering.py`: expand the calendar helper with weather encodings/indicators, >=2 scaled continuous variables, quartile congestion categories, before/after shapes and DEBUG intermediate values.
- `visualizations.py`: save >=3 Matplotlib figures and write interpretations, logging each saved path.
- `mini_app/`: implement at least `at --datetime`, `high-traffic --threshold`, and `compare-day-types`. These are planned command names, not implemented commands. Log command+arguments; validate input and return readable errors without raw tracebacks.
- `reports/methodology_report_outline.md`: finish the required 1–2 page report after results exist.

For Part 3, create separately fitted ML preprocessing so full-dataset descriptive scaling and quartiles cannot leak into holdout evaluation.
