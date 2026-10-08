# Data Analytics Insights Report

## Scope and data quality

The primary Part 1 answers use all 48,204 rows and nine columns in the supplied CSV. Every required calculation is executed in SQLite by requested_raw_analysis.sql. A row is a weather/traffic observation, not necessarily a distinct hour: the file has 40,575 distinct timestamps and 17 exact duplicate rows. Raw sums can therefore repeat hourly vehicle counts. Parts 2 and 3 use a separately documented cleaned hourly view; its results are supplementary to the raw-file answers here.

There are no empty CSV cells, but ten temperature readings are 0 K and one rainfall reading is 9,831.3 mm. Primary raw results preserve these readings. The later cleaning pipeline removes exact duplicates and imputes impossible weather readings using monthly medians. Data covers October 2012 to September 2018 at one westbound I-94 station, with gaps; it does not represent an entire city.

## Annual traffic trends, 2012-2017

| Year | Raw volume sum | Year-on-year change | Change % |
| --- | --- | --- | --- |
| 2012 | 8,208,767 | N/A | N/A |
| 2013 | 28,177,412 | +19,968,645 | +243.26% |
| 2014 | 15,731,289 | -12,446,123 | -44.17% |
| 2015 | 14,181,206 | -1,550,083 | -9.85% |
| 2016 | 29,494,821 | +15,313,615 | +107.99% |
| 2017 | 35,428,156 | +5,933,335 | +20.12% |

Totals decline in 2014 and 2015, then recover in 2016 and 2017. The largest requested total is in 2017. However, observed unique-hour coverage is only 23.94%, 83.26%, 51.38%, 41.02%, 89.23% and 99.46% for 2012-2017. Partial coverage and repeated traffic readings prevent treating these sums as comparable full-year demand.

A second observation is that the 2016 total rises 107.99%, while mean traffic per CSV row falls from 3,242.90 to 3,169.44. Increased record availability explains why a higher sum need not imply higher typical hourly demand. Changes are current minus previous total; percentage changes divide by the previous total.

## Holiday temperatures, 2015-2017

New Year's Day labelled readings average 265.94 K in 2016 and 270.62 K in 2017, a rise of 4.68 K. There is no 2015 labelled observation or record on 1 January 2015. The 2017 holiday label is on 2 January. Labor Day readings are 295.02, 293.17 and 295.54 K, falling 1.85 K in 2016 and rising 2.37 K in 2017. Each labelled estimate represents midnight, with only one or two rows.

The available-hour holiday-date supplement gives a fuller comparison: Labor Day daily mean temperature falls 0.32 K in 2016 and 3.72 K in 2017, while mean traffic changes -11.47% and +11.32%. This mixed direction does not establish a temperature effect. The New Year comparison also has unequal coverage: 18 hours in 2016 versus 24 in 2017. Detailed dates, temperatures and denominators are in raw_sql_answers.md.

## Statistics and weather probabilities

Raw-row mean traffic is 3,259.82 vehicles/hour, median 3,380, sample standard deviation 1,986.86, and sample variance 3,947,615.32 (vehicles/hour)^2. Counts range from 0 to 7,280, giving a range of 7,280. Standard deviation is about 61% of the mean, indicating substantial variation between quiet and busy periods. Sample SD/variance use n-1; population alternatives are supplied in the detailed SQL answers.

Temperature-traffic Pearson correlation is 0.130299: positive but weak. Excluding only the ten 0 K readings gives 0.132291, preserving that interpretation. Season, commuting schedules, holidays and time of day can influence both variables, so correlation does not establish causation.

Congestion means traffic_volume >5,500; Clear means weather_main = Clear; high temperature means temp >292 K. All probabilities below concern CSV records, with 48,204 observations overall and 7,100 congested observations.

| Probability | Count / denominator | Result |
| --- | --- | --- |
| P(Congestion) | 7,100 / 48,204 | 14.73% |
| P(Clear) | 13,391 / 48,204 | 27.78% |
| P(Congestion AND Clear) | 1,763 / 48,204 | 3.66% |
| P(Clear given Congestion) | 1,763 / 7,100 | 24.83% |
| P(High temperature given Congestion) | 1,867 / 7,100 | 26.30% |

The joint probability is 0.036574, versus 0.040917 for the product of marginal probabilities. Observed proportions do not satisfy independence; this comparison is not a formal population test. Clear/cloudy congestion odds ratio is (1,763/11,628)/(2,592/12,572) = 0.735388. Congestion odds are about 26.46% lower in Clear than Clouds records, excluding 19,649 observations in other weather categories. Odds are distinct from probabilities; congestion probabilities within Clear and Clouds are 13.17% and 17.09%.

## Supplementary hourly findings and implications

After cleaning and combining repeated timestamps, the separate hourly view has mean traffic 3,290.65 and correlation 0.139. These differ from raw-row values because observations receive different weights and invalid weather is imputed. The hourly view is used for the Python figures and ML evaluation, not substituted for the raw SQL answers.

Hourly mean demand peaks at 16:00 (5,709 vehicles/hour); weekdays average 3,557 versus 2,624 on weekends. Prioritise time/day patterns for travel advice, show recording coverage and weather sample sizes, and avoid causal weather or accident claims. I use macOS and do not have access to Power BI Desktop in my current setup. I was therefore unable to complete Part 1 Task 4, the Power BI section. Power BI preparation files and dashboard-specific outputs are excluded from this submission.

Evidence: requested_raw_analysis.sql and results/requested_raw_analysis/ contain primary SQLite outputs; raw_sql_answers.md contains full calculations. Supplementary hourly outputs are in results/statistics_probability.json.
