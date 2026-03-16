# DROP FOREIGN TABLE

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
DROP FOREIGN TABLE [ IF EXISTS ] name [, ...]
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
The `DROP FOREIGN TABLE` statement is a **DDL (Data Definition Language)** command used to remove a foreign table from a database. Here's an expanded overview of its syntax, description, parameters, and clauses, focusing on MonkDB and other relevant systems.

## SQL Statement

```sql
DROP FOREIGN TABLE [ IF EXISTS ] name [, ...]
```

## Description

`DROP FOREIGN TABLE` is used to delete a foreign table, which is a table that represents data from an external database accessed through a foreign data wrapper. Dropping a foreign table does not affect the actual data in the external database; it only removes the local reference to that data.

### Parameters

- **name**: The `name` of the foreign table to be dropped. Multiple tables can be specified by separating them with commas.

## Clauses

### IF EXISTS

By default, `DROP FOREIGN TABLE` raises an error if the specified table does not exist. The `IF EXISTS` clause prevents this error and instead issues a notice if the table does not exist.

## Permissions

In MonkDB, dropping a foreign table requires `AL` (Admin Level) permission on the table, schema, or cluster level. In other systems like PostgreSQL and Greenplum, only the owner of the foreign table can remove it.

## Examples

### Example 1. Dropping a Single Foreign Table

```sql
DROP FOREIGN TABLE my_foreign_table;
```

### Example 2. Dropping Multiple Foreign Tables

```sql
DROP FOREIGN TABLE my_foreign_table1, my_foreign_table2;
```

### Example 3. Using IF EXISTS to Avoid Errors

```sql
DROP FOREIGN TABLE IF EXISTS my_foreign_table;
```

---

## See Also

- [Create a foreign table](./27_CREATE_FOREIGN_TABLE.md)
