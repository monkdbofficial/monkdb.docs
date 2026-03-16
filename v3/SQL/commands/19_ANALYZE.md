# ANALYZE

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | DDL and Administration |
| Mutates Data | No |
| Scope | Cluster / Object |
| Privilege Model | Requires DDL/administrative privilege according to target object scope. |

## Purpose

Executes the ANALYZE SQL command with MonkDB distributed runtime semantics.

## Syntax

```sql
ANALYZE;
```

## Operational Notes

- Use schema-qualified identifiers in automation and automation pipelines.
- Validate behavior in staging for cluster-impacting or governance-impacting changes.
- Confirm runtime effects through system tables and metrics before and after execution.

## When to Use

- Use during planned schema and runtime administration changes.
- Use in automation pipelines with environment-specific validation and rollback strategy.

## When Not to Use

- Avoid during incident windows unless the command is part of approved mitigation.
- Avoid schema changes in peak traffic windows without staged rollout.

## Common Errors and Troubleshooting

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| Permission denied / unauthorized | Missing privilege on object or cluster scope | Re-run with required grants or elevated admin role. |
| Analysis/parse error | Syntax variant or object shape mismatch | Compare with canonical syntax and object definition. |
| Runtime failure under load | Resource limits, breaker pressure, or node state transitions | Check `sys.jobs`, `sys.operations`, `sys.checks`, and retry after mitigation. |

## Cross-References

- [SQL Command Catalog](../08-command-catalog.md)
- [SQL Commands Index](./README.md)
- [SQL Reference Overview](../01-sql-reference.md)

## Detailed Reference
The `ANALYZE` command in MonkDB is used to collect statistics about the contents of tables within the cluster. These statistics assist the query optimizer in generating efficient execution plans, thereby enhancing query performance.

---

## SQL Statement

```sql
ANALYZE;
```

##  Description

- **Purpose**: Collects and updates statistical information about table contents.​
- **Functionality**:
    + The gathered statistics are stored in the `pg_catalog.pg_stats` table.​
    + The query optimizer utilizes these statistics to create more efficient execution plans.​

##  Configuration

- Automatic Statistics Collection:
    + MonkDB periodically updates statistics automatically.​
    + The frequency of these updates can be configured using the `stats.service.interval` setting.​
- I/O Throughput Throttling:
    + To control the impact on system performance during statistics collection, I/O throughput can be throttled.​
    + This is managed via the `stats.service.max_bytes_per_sec` setting.​
    + Adjustments to this setting can be made dynamically, even while an analysis is in progress, allowing for optimization based on system performance observations.

## Performance Considerations:

- While the ANALYZE command is designed to collect samples and avoid processing all data, it can still impose load on the cluster.​
- To mitigate potential performance impacts, it's advisable to adjust the `stats.service.max_bytes_per_sec` setting appropriately.​
- Monitoring system performance during analysis can help in determining optimal settings.

##  Permissions

- Execution Rights:
    + The ANALYZE command can be executed by any user with appropriate privileges to run SQL statements.​
    + No special permissions are required to initiate the analysis process.​

##  Summary

| Command                            | Description                               | Special Permissions |
|------------------------------------|-------------------------------------------|--------------------|
| `ANALYZE`            | Collects statistics for all tables in cluster          | No                |
