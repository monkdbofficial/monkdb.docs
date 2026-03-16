# DROP SERVER

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | Federation (FDW) |
| Mutates Data | Yes/Depends |
| Scope | Cluster / Object |
| Privilege Model | Requires administrative privilege on foreign server, table, and mapping objects. |

## Purpose

Defines, changes, or removes schema and metadata objects.

## Syntax

```sql
DROP SERVER [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## Operational Notes

- Use schema-qualified identifiers in automation and automation pipelines.
- Validate behavior in staging for cluster-impacting or governance-impacting changes.
- Confirm runtime effects through system tables and metrics before and after execution.

## When to Use

- Use to register and query external data systems through SQL federation.
- Use when centralized query execution is preferred over external engine orchestration.

## When Not to Use

- Avoid expecting full pushdown for complex joins/aggregations unless explicitly supported.

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
`DROP SERVER` is a DDL statement used in MonkDB to remove one or more foreign servers. Dropping a server requires AL (Admin Level) permission on the cluster level.

## SQL Statement

```sql
DROP SERVER [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## Parameters
- **name**: The name of the server to drop. Multiple server names can be specified by separating them with commas.

## Clauses

### IF EXISTS

By default, `DROP SERVER` raises an error if the specified server does not exist. Using the `IF EXISTS` clause prevents this error and instead issues a notice if the server does not exist.

### CASCADE | RESTRICT
- **RESTRICT**: This is the default behavior. It causes `DROP SERVER` to raise an error if any foreign tables or user mappings depend on the server being dropped.
- **CASCADE**: Drops the server and automatically deletes all dependent foreign tables and user mappings.

## Example

To drop a server named my_server if it exists, without raising an error if it does not exist, and also delete any dependent objects:

```sql
DROP SERVER IF EXISTS my_server CASCADE;
```

This command will drop `my_server` and remove any foreign tables or user mappings that depend on it, provided you have the necessary permissions.

---

## See Also

- [Create Server](./32_CREATE_SERVER.md)

