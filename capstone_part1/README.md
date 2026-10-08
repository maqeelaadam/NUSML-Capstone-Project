# Part 1 Data analytics

SQLite loading, required annual/holiday queries, descriptive statistics, correlation, congestion probabilities, independence comparison and clear/cloudy odds ratio have been run. Results are saved under results/. Primary answers use all 48,204 supplied CSV rows and are calculated entirely in SQLite. The unique-hour analysis is a separately labelled supplement for the Python/ML workflow.

```bash
python -m capstone_part1.run_requested_sql
# Supplementary hourly analysis, after running the Python pipeline:
python -m capstone_part2.pipeline
python -m capstone_part1.analyze
```

The primary SQLite database is regenerated at capstone_part2/data/processed/requested_raw_analysis.sqlite; sql/traffic_analysis.sql supplies every requested calculation and the results are in results/requested_raw_analysis/. The supplementary database is capstone_part2/data/processed/traffic.sqlite; analyze.py exports supplementary hourly statistics. The same SQL file also includes the supplementary monthly coverage audit. reports/insights_report.pdf is the two-page report, with editable Markdown alongside it.

## Power BI access limitation

I use macOS and do not have access to Power BI Desktop in my current setup. I was therefore unable to complete Part 1 Task 4, the Power BI section. Power BI preparation files and dashboard-specific outputs are excluded from this submission.

## Requested calculations using the unchanged CSV

For the explicitly requested raw-file SQL answers, see [raw_sql_answers.md](reports/raw_sql_answers.md) and [traffic_analysis.sql](sql/traffic_analysis.sql). These use all 48,204 CSV rows, while the separately labelled hourly supplement uses one record per observed hour. The insights report now presents the raw-file results first. The holiday supplement distinguishes sparse midnight labels from complete available holiday-date records.

Run `python -m capstone_part1.run_requested_sql --csv "/path/to/Metro_Interstate_Traffic_Volume.csv"`. SQLite computes every requested result and saves tables/JSON under results/requested_raw_analysis/.
