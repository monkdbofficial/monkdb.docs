# KILL

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | Session and Transaction Control |
| Mutates Data | Yes/Depends |
| Scope | Cluster / Object |
| Privilege Model | Session-scoped variants require session rights; global variants require administrative privilege. |

## Purpose

Executes the KILL SQL command with MonkDB distributed runtime semantics.

## Syntax

```sql
KILL (ALL | job_id)
```

## Operational Notes

- Use schema-qualified identifiers in automation and automation pipelines.
- Validate behavior in staging for cluster-impacting or governance-impacting changes.
- Confirm runtime effects through system tables and metrics before and after execution.

## When to Use

- Use to control session behavior, cursors, or transaction compatibility settings.
- Use when client compatibility or session-scoped runtime behavior must be explicit.

## When Not to Use

- Avoid relying on PostgreSQL-compatible clauses whose behavior is intentionally no-op in MonkDB.

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
The KILL statement in MonkDB is used to terminate active jobs within a cluster.

## SQL Statement

```sql
KILL (ALL | job_id)
```

where,

- `KILL ALL`: Terminates all active jobs owned by the current user across the MonkDB cluster.
- `KILL job_id`: Terminates a specific job identified by its `job_id`, provided it was initiated by the current user.

## Parameters
- `job_id`: The UUID of the currently active job that needs to be terminated, provided as a string literal.

## Description
### Functionality
- The `KILL` command is available for all users on MonkDB clusters.
- The **monkdb** superuser has additional privileges to terminate jobs initiated by other users.

### Behavior
- **No Rollback**: MonkDB does not support transactions. If a data-modifying operation (e.g., `UPDATE`) is killed, changes already applied will not be rolled back, potentially leaving data in an inconsistent state.
- **Fast Operations**: Certain quick operations may complete before the `KILL` command is processed. In such cases, the client might receive an error despite the operation being completed.
- **Context Count**: Both `KILL ALL` and `KILL job_id` return the number of contexts terminated per node. For example, if a query spans three nodes, the result will indicate three contexts killed.

## Examples

Kill all active jobs.

```sql
KILL ALL;
```

Kill a specific job by its UUID.

```sql
KILL '175011ce-9bbc-45f2-a86a-5b7f993a93a6';
```

## Usage Considerations

Use system tables like `sys.jobs` to identify active jobs and their corresponding `job_id`. For example:

```sql
SELECT id AS job_uuid, stmt FROM sys.jobs;
```

To monitor distributed operations, use `sys.operations`:

```sql
SELECT node['name'], node['id'], * FROM sys.operations;
```

Review logs of finished jobs in tables like `sys.jobs_log` and `sys.operations_log` for historical analysis.

> **Exercise caution when using `KILL`, especially with data-modifying operations, to avoid leaving data in an inconsistent state**
