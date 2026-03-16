# Lineage Operations

Lineage captures source-to-target movement plus execution context (`pipeline_id`, `model_id`, `trace_id`, purpose) to make downstream data usage traceable.

## What lineage stores

- Job events (`sys.lineage_jobs`)
- Edge events (`sys.lineage_edges`)
- Optional projected durable stores (index/table sink configuration)

## Enable lineage sink

```sql
SET GLOBAL TRANSIENT
  lineage.enabled = true,
  lineage.sink.mode = 'async',
  "lineage.sink.index.enabled" = true,
  "lineage.sink.index.jobs_table" = 'doc.lineage_jobs_store_e2e',
  "lineage.sink.index.edges_table" = 'doc.lineage_edges_store_e2e',
  "lineage.sink.index.shards" = 1,
  "lineage.sink.index.replicas" = '0',
  "lineage.sink.index.partition_by" = 'day';
```

## Optional projected tables

```sql
CREATE TABLE IF NOT EXISTS doc.lineage_jobs_store_e2e (
  event_id STRING,
  job_id STRING,
  user_id STRING,
  timestamp LONG,
  query_hash STRING,
  status STRING,
  pipeline_id STRING,
  model_id STRING,
  dataset_version STRING,
  purpose STRING,
  trace_id STRING,
  event_bucket STRING,
  PRIMARY KEY (event_id, event_bucket)
)
PARTITIONED BY (event_bucket)
CLUSTERED INTO 1 SHARDS
WITH (number_of_replicas = 0);

CREATE TABLE IF NOT EXISTS doc.lineage_edges_store_e2e (
  event_id STRING,
  job_id STRING,
  source_table STRING,
  source_columns ARRAY(STRING),
  target_table STRING,
  target_columns ARRAY(STRING),
  transform_metadata OBJECT(DYNAMIC),
  timestamp LONG,
  pipeline_id STRING,
  model_id STRING,
  dataset_version STRING,
  purpose STRING,
  trace_id STRING,
  event_bucket STRING,
  PRIMARY KEY (event_id, event_bucket)
)
PARTITIONED BY (event_bucket)
CLUSTERED INTO 1 SHARDS
WITH (number_of_replicas = 0);
```

## Generate lineage

As `testuser`:

```sql
SET SESSION lineage.enabled = true;
SET SESSION pipeline_id = 'pipeline-ctx';
SET SESSION model_id = 'model-ctx';
SET SESSION dataset_version = 'v-ctx';
SET SESSION purpose = 'fraud_scoring';
SET SESSION trace_id = 'trace-ctx';

INSERT INTO doc.l_src (id) VALUES (1), (2);
INSERT INTO doc.l_dst (id) SELECT id FROM doc.l_src;
```

## Inspect lineage

```sql
SELECT source_table, target_table, transform_metadata['operation']
FROM sys.lineage_edges
WHERE source_table = 'doc.l_src' AND target_table = 'doc.l_dst'
ORDER BY timestamp DESC
LIMIT 5;

SELECT job_id, pipeline_id, model_id, dataset_version, purpose, trace_id
FROM sys.lineage_jobs
ORDER BY timestamp DESC
LIMIT 5;
```

Projected table checks:

```sql
REFRESH TABLE doc.lineage_edges_store_e2e;
REFRESH TABLE doc.lineage_jobs_store_e2e;

SELECT job_id, source_table, target_table, transform_metadata['operation']
FROM doc.lineage_edges_store_e2e
ORDER BY timestamp DESC
LIMIT 10;

SELECT job_id, pipeline_id, model_id, dataset_version, purpose, trace_id
FROM doc.lineage_jobs_store_e2e
ORDER BY timestamp DESC
LIMIT 10;
```

## Sink health checks

```sql
SELECT mode,
       queue_depth,
       queue_size,
       sink_lag_ms,
       retry_count,
       dropped_events,
       spool_replay_count
FROM sys.lineage_sink_metrics
LIMIT 1;
```

## Troubleshooting

- No lineage rows:
  - confirm `lineage.enabled` at session/cluster scopes.
  - confirm statements perform actual source-target data movement.
- High sink lag:
  - tune async queue/batch settings and reduce burst pressure.
- Missing context fields:
  - verify `pipeline_id`, `model_id`, `dataset_version`, `purpose`, `trace_id` are set before execution.
