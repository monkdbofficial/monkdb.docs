# Diagnostics with System Tables

When issues appear and root cause is unclear, diagnose in this order.

## 1) Health checks first

```sql
SELECT description, severity
FROM sys.checks
WHERE NOT passed
ORDER BY severity DESC;
```

## 2) Live cluster activity

```sql
SELECT id AS job_uuid, started, stmt
FROM sys.jobs
ORDER BY started DESC;

SELECT node['name'], node['id'], id, job_id, name, started, used_bytes
FROM sys.operations
ORDER BY used_bytes DESC;
```

## 3) Finished activity history

```sql
SELECT id, started, ended, stmt
FROM sys.jobs_log
ORDER BY started DESC
LIMIT 100;

SELECT job_id, name, started, ended, used_bytes
FROM sys.operations_log
ORDER BY started DESC
LIMIT 200;
```

## 4) Node health and resource imbalance

```sql
SELECT name, load['1'], mem['used_percent'], os_info['jvm']['version']
FROM sys.nodes
ORDER BY name;

SELECT name, mem['used_percent']
FROM sys.nodes
WHERE mem['used_percent'] > 98;
```

## 5) Shard state and recovery

```sql
SELECT node['name'], table_name, id, routing_state, state,
       recovery['stage'], recovery['size']['percent']
FROM sys.shards
WHERE routing_state IN ('RELOCATING','INITIALIZING')
ORDER BY table_name, id;
```

## 6) Allocation blockers

```sql
SELECT table_name, shard_id, node_id, explanation
FROM sys.allocations
WHERE table_schema = 'doc' AND table_name = 'my_table'
ORDER BY current_state, shard_id;
```

## 7) Cluster metadata and license state

```sql
SELECT id, name, master_node, "license"['status'], "license"['valid']
FROM sys.cluster;
```

## 8) Tag and visibility diagnostics

```sql
SELECT * FROM information_schema.table_tags WHERE table_schema='doc';
SELECT * FROM information_schema.column_tags WHERE table_schema='doc';
```

## 9) Snapshot fallback path

```sql
SELECT * FROM sys.repositories;
SELECT * FROM sys.snapshots ORDER BY started DESC LIMIT 20;
```

If remediation fails, plan controlled restore.
