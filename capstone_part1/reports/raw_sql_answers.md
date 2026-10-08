# SQL Answers for the Supplied Traffic CSV

All primary calculations use all 48,204 rows from the supplied CSV without cleaning or removing duplicates. SQLite performs every calculation. These primary results also appear in insights_report.pdf; the separately labelled hourly supplement uses a different aggregation and denominator. The data contains 40,575 distinct timestamps, so probabilities are per CSV record and raw sums are not deduplicated counts of passing vehicles.

## 1.2 Annual traffic trends

| Year | Sum of traffic_volume | Change from previous year | Change % | Direction |
| --- | --- | --- | --- | --- |
| 2012 | 8,208,767 | N/A | N/A | Baseline |
| 2013 | 28,177,412 | +19,968,645 | +243.26% | Increase |
| 2014 | 15,731,289 | -12,446,123 | -44.17% | Decrease |
| 2015 | 14,181,206 | -1,550,083 | -9.85% | Decrease |
| 2016 | 29,494,821 | +15,313,615 | +107.99% | Increase |
| 2017 | 35,428,156 | +5,933,335 | +20.12% | Increase |

Change = current-year total minus previous-year total. Percentage change = change divided by previous-year total, multiplied by 100.

1. Observed totals declined in 2014 and 2015, then rose in 2016 and 2017. Of the requested years, 2017 has the highest raw total at 35,428,156.
2. Large total changes do not necessarily represent changes in underlying demand. Recording begins on 2 October 2012, and unique-hour coverage is 23.94%, 83.26%, 51.38%, 41.02%, 89.23% and 99.46% of full-year hours for 2012–2017. Weather records repeat some hourly traffic counts.
3. In 2016 the total rose 107.99%, but mean traffic per CSV record fell from 3,242.90 to 3,169.44. This illustrates the importance of record availability when interpreting annual sums.

## 1.3 Temperature around holidays

The first table uses the dataset holiday labels. All matching labels occur at midnight; the two records in some years refer to the same hour. These are labelled readings, not full-day means.

| Holiday | Year | Labelled date | Mean K | Mean °C | Change K |
| --- | --- | --- | --- | --- | --- |
| New Years Day | 2015 | No record | N/A | N/A | N/A |
| New Years Day | 2016 | 2016-01-01 | 265.94 | -7.21 | N/A |
| New Years Day | 2017 | 2017-01-02 | 270.62 | -2.53 | +4.68 |
| Labor Day | 2015 | 2015-09-07 | 295.02 | 21.87 | N/A |
| Labor Day | 2016 | 2016-09-05 | 293.17 | 20.02 | -1.85 |
| Labor Day | 2017 | 2017-09-04 | 295.54 | 22.39 | +2.37 |

New Year's Day labelled temperature rises by 4.68 K from 2016 to 2017. There is no 2015 labelled observation or record on 1 January 2015, so a 2015 comparison cannot be calculated. The 2017 label is on 2 January, not 1 January.
Labor Day labelled temperature falls by 1.85 K in 2016 and rises by 2.37 K in 2017. These midnight readings should not be interpreted as daily temperature trends.

For traffic relevance, the supplementary SQL query compares all available hours on the labelled holiday dates. Repeated records are averaged per timestamp for temperature, and a single identical traffic value is retained.

| Holiday date | Available hours | Mean daily K | Mean daily °C | Mean vehicles/hour |
| --- | --- | --- | --- | --- |
| Labor Day, 2015-09-07 | 24 | 295.32 | 22.17 | 2,430.29 |
| Labor Day, 2016-09-05 | 24 | 295.01 | 21.86 | 2,151.54 |
| Labor Day, 2017-09-04 | 24 | 291.29 | 18.14 | 2,395.17 |
| New Years Day, 2016-01-01 | 18 | 267.09 | -6.06 | 1,832.00 |
| New Years Day, 2017-01-02 | 24 | 271.85 | -1.30 | 2,091.08 |

New Year’s available-hour mean temperature rises by 4.76 K in 2017 and mean traffic rises 14.14%, but 2016 has only 18 observed hours compared with 24 in 2017. Different calendar dates/day types and incomplete hourly coverage prevent attributing that change to temperature.
Labor Day daily mean temperature falls 0.32 K in 2016 while mean traffic falls 11.47%. In 2017 daily temperature falls a further 3.72 K, but mean traffic rises 11.32%. There is no consistent temperature–traffic direction across these holiday comparisons. Holiday travel schedules, hour of day and other weather conditions may matter.

## 2.1 Traffic volume statistics

| Statistic | Value |
| --- | --- |
| Mean | 3,259.82 vehicles/hour |
| Median | 3,380 vehicles/hour |
| Sample standard deviation | 1,986.86 vehicles/hour |
| Sample variance | 3,947,615.32 (vehicles/hour)² |
| Minimum | 0 |
| Maximum | 7,280 |
| Range | 7,280 vehicles/hour |

Sample variance uses n−1. If population statistics are required, population SD is 1,986.84 and variance is 3,947,533.43.
The mean and median are fairly close, with the median slightly higher. SD is about 61% of the mean, indicating substantial traffic variability. Counts span zero to 7,280 vehicles/hour, reflecting very quiet and busy observed periods; extremes alone do not explain their cause.

## 2.2 Temperature–traffic correlation

Pearson r = 0.130299. The direction is positive and the strength is weak. Warmer readings tend to coincide with slightly higher traffic, but temperature alone has little linear explanatory value. Correlation does not establish causation: season, commuting schedules, holidays and time of day can affect both variables.
The raw data includes ten readings of 0 K. A separate sensitivity query excludes only those readings and gives r = 0.132291, retaining the same weak-positive interpretation.

## 3 Probability and congestion

Congestion means traffic_volume >5,500. Clear means weather_main = Clear; cloudy means weather_main = Clouds. High temperature means temp >292 K.

| Probability | Count / denominator | Result |
| --- | --- | --- |
| P(Congestion) | 7,100/48,204 | 0.147291 = 14.73% |
| P(Clear) | 13,391/48,204 | 0.277799 = 27.78% |
| P(Congestion AND Clear) | 1,763/48,204 | 0.036574 = 3.66% |
| P(Clear given Congestion) | 1,763/7,100 | 0.248310 = 24.83% |
| P(High temperature given Congestion) | 1,867/7,100 | 0.262958 = 26.30% |

Independence check: observed joint P(Congestion AND Clear) = 0.036574, whereas P(Congestion) × P(Clear) = 0.040917. They differ, so the observed record-level proportions do not satisfy independence. This is an empirical comparison, not a causal conclusion or a formal population-level test.

| Weather | Congested | Not congested |
| --- | --- | --- |
| Clear | 1,763 | 11,628 |
| Clouds | 2,592 | 12,572 |

Odds ratio = (1,763/11,628)/(2,592/12,572) = 0.735388. Congestion odds are approximately 26.46% lower for Clear than Clouds in these records. This is a reduction in odds, not the same percentage reduction in probability. Other weather categories (19,649 records) are excluded from this specific comparison.
For context, congestion probability is 13.17% within Clear records versus 17.09% within Clouds records.

Weather and congestion show an observed association, but the weak temperature correlation and mixed holiday patterns indicate that weather alone does not explain traffic. Differences in time, season, coverage and repeated weather records limit causal interpretations.

## Reproduction

Run from the project root: `python -m capstone_part1.run_requested_sql --csv "/path/to/Metro_Interstate_Traffic_Volume.csv"`. The script imports the raw file into SQLite; all statistical/probability calculations are executed by the supplied SQL queries. Results are under capstone_part1/results/requested_raw_analysis/. A separate Python standard-library check independently verified statistics, correlation, annual sums and event counts.

Input verification: the user-supplied CSV, SHA-256 749c90d720360a4215bb15345526073c079ba4cc95e3fa558796d083f85fce9e. No external dataset was substituted.
