# ALTER EDGE TABLE

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | Platform Extensions |
| Mutates Data | Yes/Depends |
| Scope | Cluster / Object |
| Privilege Model | Requires administrative or feature-specific governance/cluster privileges. |

## Purpose

Defines, changes, or removes schema and metadata objects.

## Syntax

```sql
ALTER EDGE TABLE [IF EXISTS] schema.table [WITH (...)]
```

## Operational Notes

- Use schema-qualified identifiers in automation and automation pipelines.
- Validate behavior in staging for cluster-impacting or governance-impacting changes.
- Confirm runtime effects through system tables and metrics before and after execution.

## When to Use

- Use for graph, memory, governance, and licensing lifecycle management.
- Use when feature-specific metadata and policy controls are required.

## When Not to Use

- Avoid enabling strict enforcement modes before validation and staged verification.

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
Updates mutable properties on a registered edge table.

## SQL Statement

```sql
ALTER EDGE TABLE [IF EXISTS] schema.table [WITH (...)]
```

## Parameters

- `schema.table`: Registered edge table.
- `WITH (...)`: Property updates.

## Privileges

Requires DDL privilege on graph metadata.

## Example

```sql
ALTER EDGE TABLE IF EXISTS doc.follows WITH (description = 'follow relationships');
```

## Notes

- Supported keys are release-dependent; verify in your environment.
- Use `IF EXISTS` for idempotent automation pipelines.

## Related

- [CREATE EDGE TABLE](./86_CREATE_EDGE_TABLE.md)
- [DROP EDGE TABLE](./88_DROP_EDGE_TABLE.md)
