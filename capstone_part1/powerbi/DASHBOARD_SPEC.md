# Power BI dashboard specification

Status: specification only; no PBIX dashboard has been created.

In Power Query, import the CSV, confirm row/column counts, missingness and types, parse DateTime, extract Hour, derive Temperature_Celsius, and create `traffic_category_fixed`: Low <4500, Medium 4500–5500 inclusive, High >5500. Preserve no-holiday text and document the treatment of invalid weather readings and repeated timestamps.

Build these report visuals:

- Daily average traffic line chart for 2015, 2016 and 2017.
- Average traffic column chart by hour for 2017.
- Average traffic by weather; identify highest and lowest categories and their difference, with sample sizes.
- Temperature–traffic scatter plot; discuss visible relationship, high-volume temperature range and outliers.
- KPI cards: total hours analysed (distinct timestamps at the documented grain), average traffic volume, average temperature.
- Slicers: hour range, weather condition, fixed traffic category.

Record screenshot evidence and save the actual dashboard as `traffic_intelligence.pbix`. Include the Power Query transformations and measure definitions so the grader can reproduce the calculations. Verify slicers affect the intended charts and KPI cards. If distinct-hour and row-based measures differ, explain the chosen grain in the report.
