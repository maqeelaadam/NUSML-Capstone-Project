# Data Analytics Insights Report

The main analysis uses one record per observed hour so repeated weather reports do not inflate traffic totals. Across 40,575 observed hours, hourly traffic averages 3,291 vehicles, with substantial variation by time of day. Temporal coverage must be considered before treating annual totals as demand trends. The Power BI dashboard itself remains to be authored; its preparation assets and required analysis outputs are provided.

## Data preparation and scope

The supplied CSV contains 48,204 rows and nine columns, with no empty cells. There are 17 exact duplicates and 7,612 additional weather records after deduplication. Cleaning removes exact duplicates, replaces 10 impossible temperature readings and one rainfall reading using monthly medians, and preserves valid zero traffic. The hourly view averages numeric weather readings and selects the most severe textual weather category. Traffic counts agree at repeated timestamps. The file covers October 2012 to September 2018, with gaps; it represents one westbound I-94 station, not a city-wide network.

## Annual and holiday observations

Observed hourly totals fall from 24.14 million vehicles in 2013 to 14.72 million in 2014 and 11.71 million in 2015, then rise to 25.03 million in 2016 and 29.42 million in 2017. These changes track recording coverage: 83.3%, 51.4%, 41.0%, 89.2% and 99.5% of full-year hours respectively. They cannot be read as equivalent changes in annual demand. A second observation is that mean traffic increases from 3,194 vehicles/hour in 2016 to 3,377 in 2017, about 5.7%, much less than the 17.5% increase in observed totals. Raw-record totals and year-on-year changes are supplied separately to meet the raw analysis requirement and expose repeated-hour sensitivity.

Labour Day labelled readings average 295.02 K in 2015, 293.17 K in 2016 and 295.54 K in 2017. New Year's Day averages 265.94 K in 2016 and 270.62 K in 2017; 2015 has no labelled record. Each estimate comes from only one or two labelled rows, so it does not establish a full-day temperature or a temperature-driven traffic effect.

## Statistics and weather probabilities

Mean traffic is 3,290.65, median 3,427, sample standard deviation 1,984.77, sample variance 3,939,323.50, and range 7,280 vehicles/hour (0 to 7,280). The large dispersion reflects strong hourly variation. Temperature-volume Pearson correlation is 0.139, a weak positive association; time, season and commuting patterns can confound it.

Using congestion >5,500 vehicles and high temperature >292 K: P(congestion)=0.1505, P(clear)=0.3294, P(congestion AND clear)=0.0434, P(clear | congestion)=0.2885, and P(high temperature | congestion)=0.2782. The joint probability differs from the product of marginals (0.0496), so simple empirical independence is not supported. Congestion odds in clear versus cloudy conditions have ratio 0.736; this excludes 12,088 hours in other weather categories and does not establish weather causation.

## Implications for mobility planning

Average traffic peaks at 16:00 (5,709 vehicles/hour); weekdays average 3,557 versus weekends 2,624. Haze has the highest hourly weather-category mean (3,703) and Squall the lowest (2,062), a difference of roughly 1,641. Squall has very few observations, limiting that comparison. Higher traffic is visible across a broad temperature range rather than a narrow reliable band. Prioritise hour/day information in timing advice, show coverage and category sample sizes on the dashboard, and avoid interpreting weather associations as safety claims.

Source: Hogue, J. (2019), Metro Interstate Traffic Volume, UCI Machine Learning Repository, DOI 10.24432/C5X60B, CC BY 4.0. Numerical evidence is in capstone_part1/results; definitions and SQL are in the repository.
