# Production Operations Runbook

This runbook is a practical checklist for day-2 MonkDB operations.

## Daily checks

```sql
SELECT description, severity FROM sys.checks WHERE NOT passed ORDER BY severity DESC;
SELECT name, load['1'], mem['used_percent'], heap['used'] FROM sys.nodes ORDER BY name;
SELECT table_name, id, routing_state, state FROM sys.shards ORDER BY table_name, id;
```

## During latency incident

1. Identify top active jobs/operations by memory and runtime.
2. Check node imbalance (`sys.nodes`).
3. Check relocating/initializing shards (`sys.shards`).
4. Inspect breaker exceptions and reduce heavy concurrency.

## During node failure/restart

1. Confirm master election and cluster availability.
2. Track shard recovery and allocation explanations.
3. Avoid concurrent disruptive maintenance until recovery stabilizes.

## Release/maintenance window

- Use rolling strategy.
- Validate shard health between each node change.
- Keep snapshots recent before major version/config change.

## Snapshot hygiene

```sql
SELECT * FROM sys.repositories;
SELECT * FROM sys.snapshots ORDER BY started DESC LIMIT 20;
```

## Governance/audit/lineage checks

```sql
SELECT * FROM sys.policy_audit_sink_metrics LIMIT 1;
SELECT * FROM sys.governance_contract_metrics LIMIT 1;
SELECT * FROM sys.lineage_sink_metrics LIMIT 1;
```

## License state checks

```sql
SELECT "license"['status'], "license"['valid'], "license"['allowed_nodes'], "license"['current_nodes'], "license"['error']
FROM sys.cluster;
```
