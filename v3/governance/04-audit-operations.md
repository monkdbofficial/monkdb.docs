# Audit Operations

Audit captures governance decisions and writes them to runtime metrics and optional persistent stores for compliance, debugging, and forensics.

## What to configure

Audit operations usually require:

- audit enablement
- sink mode (`sync` for strict durability profile, `async` for lower latency profile)
- optional index persistence (`audit.sink.index.*`)
- queue/batch tuning for async mode

## Enable audit sink

```sql
SET GLOBAL TRANSIENT
  audit.enabled = true,
  "audit.sink.mode" = 'sync',
  "audit.sink.index.enabled" = true,
  "audit.sink.index.name" = 'policy_audit_events_e2e',
  "audit.sink.index.shards" = 1,
  "audit.sink.index.replicas" = '0';
```

## Minimal persisted table (if not auto-created)

```sql
CREATE TABLE IF NOT EXISTS doc.policy_audit_events_e2e (
  policy_id STRING,
  scope STRING,
  outcome STRING,
  subject STRING,
  resource STRING,
  reason STRING,
  timestamp TIMESTAMP WITH TIME ZONE
) WITH (number_of_replicas = 0);
```

## Metrics and event checks

```sql
SELECT mode, index_enabled, queue_depth
FROM sys.policy_audit_sink_metrics
LIMIT 1;

REFRESH TABLE doc.policy_audit_events_e2e;

SELECT policy_id, scope, outcome, subject, resource, reason
FROM doc.policy_audit_events_e2e
ORDER BY timestamp DESC
LIMIT 20;
```

## SLO-style checks

```sql
SELECT mode,
       queue_depth,
       queue_size,
       sink_lag_ms,
       failed_batches,
       dropped_events,
       spool_replay_count
FROM sys.policy_audit_sink_metrics
LIMIT 1;
```

## Troubleshooting

- Empty audit table:
  - confirm `audit.enabled = true`.
  - confirm `audit.sink.index.enabled = true` and index/table name match.
- Growing queue depth:
  - increase batch/flush cadence or reduce audit event pressure.
- Non-zero dropped events:
  - review queue sizing, sink latency, and `drop_on_full` strategy.

## Recommended operations pattern

1. Keep sink mode deterministic in regulated environments.
2. Monitor queue depth and sink lag continuously.
3. Retain audit events in an immutable or long-retention tier.
