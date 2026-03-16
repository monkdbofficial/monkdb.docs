# Monitoring and Observability

A production MonkDB setup should combine:

1. SQL-native observability (`sys.*`, `information_schema.*`)
2. JVM and breaker telemetry (JMX)
3. Time-series dashboards and alerts (Prometheus + Grafana)

## Layer 1: SQL-native observability

### Health status

```sql
SELECT description, severity
FROM sys.checks
WHERE NOT passed
ORDER BY severity DESC;
```

### Active workload

```sql
SELECT id, stmt, started FROM sys.jobs;

SELECT node['name'], job_id, name, used_bytes, started
FROM sys.operations
ORDER BY used_bytes DESC;
```

### Node pressure

```sql
SELECT name,
       load['1'] AS load_1m,
       mem['used_percent'] AS mem_used_pct,
       heap['used'] AS heap_used,
       fs['total'],
       fs['used']
FROM sys.nodes
ORDER BY name;
```

### Shard state

```sql
SELECT table_name, id, routing_state, state,
       recovery['stage'], recovery['size']['percent']
FROM sys.shards
ORDER BY table_name, id;
```

## Layer 2: JMX instrumentation

Track at minimum:

- JVM heap/non-heap usage
- GC pause and throughput
- thread pools
- circuit breaker utilization/trips
- request/operation latency trends

## Layer 3: Prometheus + Grafana

Recommended pipeline:

1. JMX exporter sidecar/agent per node.
2. Prometheus scrape targets for MonkDB nodes.
3. Grafana dashboards with SLO-focused panels.

Recommended dashboards:

- Cluster health and node pressure
- Query throughput, p95/p99 latency
- Breaker headroom/trip rates
- Shard relocation/recovery activity
- Governance/audit/lineage sink metrics

## Governance and sink metrics

When enabled:

```sql
SELECT * FROM sys.policy_audit_sink_metrics LIMIT 1;
SELECT * FROM sys.governance_contract_metrics LIMIT 1;
SELECT * FROM sys.lineage_sink_metrics LIMIT 1;
```

## Alerting baselines

- Sustained high heap usage
- Breaker trip rate increase
- Growing queue depth in sink metrics
- Relocation stuck/slow recovery
- High ratio of failed queries
