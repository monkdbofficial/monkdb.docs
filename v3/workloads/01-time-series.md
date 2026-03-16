# Time-Series Workloads

Time-series workloads in MonkDB typically combine high-ingest writes with aggregate-heavy reads.

## Create table

```sql
CREATE TABLE IF NOT EXISTS doc.sensor_data (
  ts TIMESTAMPTZ PRIMARY KEY,
  location TEXT NOT NULL,
  temperature REAL NOT NULL,
  humidity REAL NOT NULL,
  wind_speed REAL NOT NULL
)
CLUSTERED BY (ts) INTO 4 SHARDS
WITH (number_of_replicas = '0-1');
```

## Insert sample rows

```sql
INSERT INTO doc.sensor_data (ts, location, temperature, humidity, wind_speed) VALUES
  ('2026-03-14T10:00:00Z', 'New York', 20.2, 61.0, 12.4),
  ('2026-03-14T10:01:00Z', 'London',   14.6, 71.5,  8.3),
  ('2026-03-14T10:02:00Z', 'Berlin',   16.8, 65.2, 10.7),
  ('2026-03-14T10:03:00Z', 'Tokyo',    19.1, 59.3,  6.4);

REFRESH TABLE doc.sensor_data;
```

## Query patterns

Recent window:

```sql
SELECT ts, location, temperature, humidity, wind_speed
FROM doc.sensor_data
WHERE ts >= CURRENT_TIMESTAMP - INTERVAL '24 hours'
ORDER BY ts DESC
LIMIT 50;
```

Per-location aggregation:

```sql
SELECT location,
       AVG(temperature) AS avg_temp,
       MIN(temperature) AS min_temp,
       MAX(temperature) AS max_temp,
       COUNT(*) AS samples
FROM doc.sensor_data
GROUP BY location
ORDER BY avg_temp DESC;
```

Hourly rollup:

```sql
SELECT date_trunc('hour', ts) AS hour_bucket,
       location,
       AVG(temperature) AS avg_temp,
       AVG(humidity) AS avg_humidity
FROM doc.sensor_data
GROUP BY 1, 2
ORDER BY 1, 2;
```

## Operational checks

```sql
SELECT table_name, number_of_shards, number_of_replicas
FROM information_schema.tables
WHERE table_schema = 'doc' AND table_name = 'sensor_data';

SHOW CREATE TABLE doc.sensor_data;
```

