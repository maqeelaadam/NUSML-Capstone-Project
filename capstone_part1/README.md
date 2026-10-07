# Part 1 Data analytics

SQLite loading, required annual/holiday queries, descriptive statistics, correlation, congestion probabilities, independence comparison and clear/cloudy odds ratio have been run. Results are saved under results/. Both raw-record and unique-hour annual outputs are supplied; the primary interpretation uses unique hours with coverage caveats.

```bash
python -m capstone_part2.pipeline
python -m capstone_part1.analyze
```

The SQLite database is regenerated at data/processed/traffic.sqlite. sql/traffic_analysis.sql contains the key queries; analyze.py executes and exports results. reports/insights_report.pdf is the two-page report, with editable Markdown alongside it.

**Remaining:** build and validate the actual Power BI dashboard. powerbi/traffic_import.pq imports/prepares the raw CSV using a TrafficCsvPath parameter; measures.dax supplies KPI measures. DASHBOARD_SPEC.md lists visuals/slicers. If the dashboard uses the prepared hourly table, explicitly document that grain and repeat the required Power Query checks. Raw-record averages differ from hourly averages. No completed PBIX is claimed.
