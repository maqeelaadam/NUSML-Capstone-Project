-- STARTER QUERIES ONLY: first import supplied CSV as traffic_raw.
-- Decide and document observation vs hourly grain before final interpretations.
SELECT COUNT(*) AS rows_loaded, COUNT(DISTINCT date_time) AS unique_hours,
       MIN(date_time) AS first_timestamp, MAX(date_time) AS last_timestamp
FROM traffic_raw;

-- Task 1.2: required years. Raw totals may repeat hourly readings.
WITH annual AS (
 SELECT strftime('%Y', date_time) AS year,
        COUNT(*) AS observations, COUNT(DISTINCT date_time) AS unique_hours,
        SUM(CAST(traffic_volume AS INTEGER)) AS total_volume,
        AVG(CAST(traffic_volume AS REAL)) AS mean_volume
 FROM traffic_raw
 WHERE strftime('%Y', date_time) BETWEEN '2012' AND '2017'
 GROUP BY year
), changes AS (
 SELECT *, LAG(total_volume) OVER (ORDER BY year) AS previous_total FROM annual
)
SELECT *, total_volume - previous_total AS absolute_change,
       100.0 * (total_volume - previous_total) / NULLIF(previous_total, 0) AS percent_change
FROM changes ORDER BY year;

-- Task 1.3: labelled holiday observations, not assumed full holiday days.
SELECT strftime('%Y', date_time) AS year, holiday, COUNT(*) AS observations,
       AVG(CASE WHEN CAST(temp AS REAL) > 0 THEN CAST(temp AS REAL) END) AS mean_kelvin,
       AVG(CASE WHEN CAST(temp AS REAL) > 0 THEN CAST(temp AS REAL)-273.15 END) AS mean_celsius
FROM traffic_raw
WHERE strftime('%Y', date_time) BETWEEN '2015' AND '2017'
  AND holiday IN ('New Years Day', 'Labor Day')
GROUP BY year, holiday ORDER BY year, holiday;

-- Audit coverage by year/month before explaining annual differences.
SELECT strftime('%Y-%m', date_time) AS month,
       COUNT(*) AS observations, COUNT(DISTINCT date_time) AS unique_hours
FROM traffic_raw GROUP BY month ORDER BY month;
