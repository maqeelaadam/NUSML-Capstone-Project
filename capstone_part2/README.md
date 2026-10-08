# Part 2 Reproducible traffic pipeline

The end-to-end workflow has run on the supplied CSV. It validates schema before processing, standardises categories, parses dates, removes exact duplicates, imputes invalid weather readings by monthly medians, builds a unique-hour table, engineers features, saves four Matplotlib figures and writes a levelled pipeline.log.

```bash
python -m capstone_part2.pipeline
python -m capstone_part2.pipeline --log-level DEBUG
python -m capstone_part2.mini_app at --datetime "2017-01-01 12:00:00"
python -m capstone_part2.mini_app high-traffic --threshold 5500 --limit 10
python -m capstone_part2.mini_app compare-day-types
```

Run from the repository root after copying the supplied CSV as described in the root README. Generated tables are capstone_part2/data/processed/cleaned_observations.csv, hourly_traffic.csv and traffic_features.csv. The feature table has 40,575 rows and 35 columns. Calendar/holiday/cyclic features, severe-weather/visibility indicators, one-hot weather, and scaled temperature/cloud cover are included. Descriptive full-data scaling and quartiles must not be used as fitted ML preprocessing; Part 3 estimates those parameters on training data independently.

Entry points configure console and file handlers. Every module declares a named logger; format includes timestamp/level/module/message. INFO records shapes and saved paths; WARNING records cleaning counts/reasons; DEBUG values appear only in DEBUG mode; ERROR captures failure and returns nonzero status. CLI answers may print, internal progress does not. The checked-in pipeline.log is a real completed run and is intentionally retained by .gitignore.

figures/ includes four figures and INTERPRETATIONS.md. reports/methodology_report.pdf is the written report, with editable Markdown. The required methodology report explains the schema checks and anomaly policy. Monthly imputation, holiday propagation and weather-severity aggregation remain analytical choices for your review.
