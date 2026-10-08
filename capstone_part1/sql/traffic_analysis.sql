-- All requested calculations use the CSV as supplied: no deduplication/imputation.
-- Table: traffic_raw, imported by capstone_part1/run_requested_sql.py.
-- Clear = weather_main='Clear'; cloudy = weather_main='Clouds'.
-- Congestion: traffic_volume > 5500. High temperature: temp > 292 K.
-- SQRT is a SQLite math function; the runner supplies it if unavailable.

-- query: data_audit
SELECT COUNT(*) AS raw_rows,
       COUNT(DISTINCT date_time) AS distinct_hours,
       MIN(date_time) AS first_timestamp,
       MAX(date_time) AS last_timestamp,
       SUM(CASE WHEN temp <= 0 THEN 1 ELSE 0 END) AS nonpositive_temperature_rows
FROM traffic_raw;

-- query: annual_traffic
WITH annual AS (
    SELECT CAST(strftime('%Y', date_time) AS INTEGER) AS year,
           COUNT(*) AS raw_rows,
           COUNT(DISTINCT date_time) AS observed_hours,
           SUM(traffic_volume) AS total_traffic_volume,
           AVG(traffic_volume) AS mean_traffic_per_record
    FROM traffic_raw
    WHERE strftime('%Y', date_time) BETWEEN '2012' AND '2017'
    GROUP BY year
), compared AS (
    SELECT *, LAG(total_traffic_volume) OVER (ORDER BY year) AS previous_total
    FROM annual
)
SELECT *, total_traffic_volume - previous_total AS absolute_change,
       100.0 * (total_traffic_volume - previous_total)
           / NULLIF(previous_total, 0) AS percentage_change,
       CASE WHEN previous_total IS NULL THEN 'Baseline'
            WHEN total_traffic_volume > previous_total THEN 'Increase'
            WHEN total_traffic_volume < previous_total THEN 'Decrease'
            ELSE 'No change' END AS direction,
       100.0 * observed_hours /
           CASE WHEN year % 4 = 0 THEN 8784 ELSE 8760 END AS full_year_hour_coverage_pct
FROM compared ORDER BY year;

-- query: holiday_label_temperatures
-- Includes every requested year/holiday pair; NULL signifies no labelled record.
WITH years(year) AS (VALUES (2015), (2016), (2017)),
     holidays(holiday) AS (VALUES ('New Years Day'), ('Labor Day')),
     averages AS (
         SELECT y.year, h.holiday, COUNT(t.date_time) AS labelled_rows,
                COUNT(DISTINCT t.date_time) AS labelled_hours,
                MIN(date(t.date_time)) AS labelled_date,
                AVG(t.temp) AS mean_kelvin,
                AVG(t.temp) - 273.15 AS mean_celsius,
                AVG(t.traffic_volume) AS mean_labelled_traffic
         FROM years y CROSS JOIN holidays h
         LEFT JOIN traffic_raw t
           ON CAST(strftime('%Y', t.date_time) AS INTEGER) = y.year
          AND t.holiday = h.holiday
         GROUP BY y.year, h.holiday
     )
SELECT *, mean_kelvin - LAG(mean_kelvin)
    OVER (PARTITION BY holiday ORDER BY year) AS temperature_change_kelvin
FROM averages ORDER BY holiday, year;

-- query: full_labelled_holiday_dates
-- Supplement: all available hours on dates actually labelled in this file.
-- Numeric readings are averaged per timestamp to avoid repeated-hour weighting.
-- No holiday is inferred for a year that lacks labelled data.
WITH holiday_dates AS (
    SELECT DISTINCT holiday, date(date_time) AS day
    FROM traffic_raw
    WHERE holiday IN ('New Years Day', 'Labor Day')
      AND strftime('%Y', date_time) BETWEEN '2015' AND '2017'
), hourly AS (
    SELECT d.holiday, d.day, t.date_time,
           AVG(t.temp) AS hourly_kelvin,
           MAX(t.traffic_volume) AS hourly_traffic
    FROM holiday_dates d JOIN traffic_raw t ON date(t.date_time) = d.day
    GROUP BY d.holiday, d.day, t.date_time
), averages AS (
    SELECT holiday, day, COUNT(*) AS available_hours,
           AVG(hourly_kelvin) AS mean_kelvin,
           AVG(hourly_kelvin) - 273.15 AS mean_celsius,
           AVG(hourly_traffic) AS mean_vehicles_per_hour
    FROM hourly GROUP BY holiday, day
)
SELECT *, mean_kelvin - LAG(mean_kelvin)
    OVER (PARTITION BY holiday ORDER BY day) AS temperature_change_kelvin,
    100.0 * (mean_vehicles_per_hour - LAG(mean_vehicles_per_hour)
    OVER (PARTITION BY holiday ORDER BY day)) /
    NULLIF(LAG(mean_vehicles_per_hour)
    OVER (PARTITION BY holiday ORDER BY day), 0) AS traffic_percentage_change
FROM averages ORDER BY holiday, day;

-- query: traffic_statistics
WITH centre AS (
    SELECT COUNT(*) AS n, AVG(traffic_volume) AS mean_traffic
    FROM traffic_raw
), ordered AS (
    SELECT traffic_volume,
           ROW_NUMBER() OVER (ORDER BY traffic_volume) AS row_position
    FROM traffic_raw
), median_value AS (
    SELECT AVG(1.0 * traffic_volume) AS median_traffic
    FROM ordered CROSS JOIN centre
    WHERE row_position IN ((n + 1) / 2, (n + 2) / 2)
), spread AS (
    SELECT SUM((traffic_volume - mean_traffic) *
               (traffic_volume - mean_traffic)) AS squared_deviation_sum,
           MIN(traffic_volume) AS minimum_traffic,
           MAX(traffic_volume) AS maximum_traffic
    FROM traffic_raw CROSS JOIN centre
)
SELECT n, mean_traffic, median_traffic,
       squared_deviation_sum / (n - 1) AS sample_variance,
       SQRT(squared_deviation_sum / (n - 1)) AS sample_standard_deviation,
       squared_deviation_sum / n AS population_variance,
       SQRT(squared_deviation_sum / n) AS population_standard_deviation,
       minimum_traffic, maximum_traffic,
       maximum_traffic - minimum_traffic AS traffic_range
FROM centre CROSS JOIN median_value CROSS JOIN spread;

-- query: temperature_correlation
-- Pearson correlation, calculated with centred values for numerical stability.
WITH means AS (
    SELECT AVG(temp) AS mean_temp,
           AVG(traffic_volume) AS mean_traffic FROM traffic_raw
)
SELECT COUNT(*) AS n,
       SUM((temp - mean_temp) * (traffic_volume - mean_traffic)) /
       NULLIF(SQRT(SUM((temp - mean_temp) * (temp - mean_temp)) *
                   SUM((traffic_volume - mean_traffic) *
                       (traffic_volume - mean_traffic))), 0) AS pearson_r
FROM traffic_raw CROSS JOIN means;

-- query: correlation_positive_temperature_sensitivity
-- Separately labelled sensitivity check; does not replace the raw-file result.
WITH valid AS (SELECT * FROM traffic_raw WHERE temp > 0),
     means AS (SELECT AVG(temp) AS mean_temp,
                      AVG(traffic_volume) AS mean_traffic FROM valid)
SELECT COUNT(*) AS n,
       SUM((temp - mean_temp) * (traffic_volume - mean_traffic)) /
       NULLIF(SQRT(SUM((temp - mean_temp) * (temp - mean_temp)) *
                   SUM((traffic_volume - mean_traffic) *
                       (traffic_volume - mean_traffic))), 0) AS pearson_r
FROM valid CROSS JOIN means;

-- query: congestion_probabilities
WITH counts AS (
    SELECT COUNT(*) AS n,
           SUM(CASE WHEN traffic_volume > 5500 THEN 1 ELSE 0 END) AS congested,
           SUM(CASE WHEN weather_main = 'Clear' THEN 1 ELSE 0 END) AS clear,
           SUM(CASE WHEN traffic_volume > 5500 AND weather_main = 'Clear'
                    THEN 1 ELSE 0 END) AS congested_and_clear,
           SUM(CASE WHEN traffic_volume > 5500 AND temp > 292
                    THEN 1 ELSE 0 END) AS congested_and_hot
    FROM traffic_raw
)
SELECT *, 1.0 * congested / n AS p_congestion,
       1.0 * clear / n AS p_clear,
       1.0 * congested_and_clear / n AS p_congestion_and_clear,
       1.0 * congested_and_clear / NULLIF(congested, 0) AS p_clear_given_congestion,
       1.0 * congested_and_hot / NULLIF(congested, 0) AS p_hot_given_congestion,
       (1.0 * congested / n) * (1.0 * clear / n) AS product_of_marginals,
       1.0 * congested_and_clear / n -
           (1.0 * congested / n) * (1.0 * clear / n) AS independence_gap
FROM counts;

-- query: clear_cloudy_odds_ratio
-- The comparison is restricted to Clear and Clouds, excluding other weather.
WITH contingency AS (
    SELECT SUM(CASE WHEN weather_main = 'Clear' AND traffic_volume > 5500
                    THEN 1 ELSE 0 END) AS a_clear_congested,
           SUM(CASE WHEN weather_main = 'Clear' AND traffic_volume <= 5500
                    THEN 1 ELSE 0 END) AS b_clear_not_congested,
           SUM(CASE WHEN weather_main = 'Clouds' AND traffic_volume > 5500
                    THEN 1 ELSE 0 END) AS c_cloudy_congested,
           SUM(CASE WHEN weather_main = 'Clouds' AND traffic_volume <= 5500
                    THEN 1 ELSE 0 END) AS d_cloudy_not_congested,
           SUM(CASE WHEN weather_main NOT IN ('Clear', 'Clouds')
                    THEN 1 ELSE 0 END) AS excluded_other_weather
    FROM traffic_raw
)
SELECT *, 1.0 * a_clear_congested / NULLIF(b_clear_not_congested, 0) AS clear_odds,
       1.0 * c_cloudy_congested / NULLIF(d_cloudy_not_congested, 0) AS cloudy_odds,
       1.0 * a_clear_congested * d_cloudy_not_congested /
           NULLIF(b_clear_not_congested * c_cloudy_congested, 0) AS odds_ratio,
       1.0 * a_clear_congested /
           NULLIF(a_clear_congested + b_clear_not_congested, 0) AS clear_congestion_probability,
       1.0 * c_cloudy_congested /
           NULLIF(c_cloudy_congested + d_cloudy_not_congested, 0) AS cloudy_congestion_probability
FROM contingency;

-- query: monthly_coverage
SELECT strftime('%Y-%m', date_time) AS month,
       COUNT(*) AS observations, COUNT(DISTINCT date_time) AS unique_hours
FROM traffic_raw GROUP BY month ORDER BY month;
