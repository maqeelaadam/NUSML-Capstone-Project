# Part 1 Data analytics

SQLite loading, required annual/holiday queries, descriptive statistics, correlation, congestion probabilities, independence comparison and clear/cloudy odds ratio have been run. Results are saved under results/. Primary answers use all 48,204 supplied CSV rows and are calculated entirely in SQLite. The unique-hour analysis is a separately labelled supplement for the Python/ML workflow.

```bash
python -m capstone_part1.run_requested_sql
# Supplementary hourly analysis, after running the Python pipeline:
python -m capstone_part2.pipeline
python -m capstone_part1.analyze
```

The primary SQLite database is regenerated at data/processed/requested_raw_analysis.sqlite; sql/requested_raw_analysis.sql supplies every requested calculation and the results are in results/requested_raw_analysis/. The supplementary database is data/processed/traffic.sqlite; analyze.py exports the hourly statistics and dashboard preparation tables. sql/traffic_analysis.sql supplies additional audit queries. reports/insights_report.pdf is the two-page report, with editable Markdown alongside it.

**Remaining:** build and validate the actual Power BI dashboard. powerbi/traffic_import.pq imports/prepares the raw CSV using a TrafficCsvPath parameter; measures.dax supplies KPI measures. DASHBOARD_SPEC.md lists visuals/slicers. If the dashboard uses the prepared hourly table, explicitly document that grain and repeat the required Power Query checks. Raw-record averages differ from hourly averages. No completed PBIX is claimed.

## Requested calculations using the unchanged CSV

For the explicitly requested raw-file SQL answers, see [raw_sql_answers.md](reports/raw_sql_answers.md) and [requested_raw_analysis.sql](sql/requested_raw_analysis.sql). These use all 48,204 CSV rows, while the separately labelled hourly supplement uses one record per observed hour. The insights report now presents the raw-file results first. The holiday supplement distinguishes sparse midnight labels from complete available holiday-date records.

Run `python -m capstone_part1.run_requested_sql --csv "/path/to/Metro_Interstate_Traffic_Volume.csv"`. SQLite computes every requested result and saves tables/JSON under results/requested_raw_analysis/.
