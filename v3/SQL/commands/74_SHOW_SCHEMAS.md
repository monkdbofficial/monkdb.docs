# SHOW SCHEMAS

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | DDL and Administration |
| Mutates Data | No |
| Scope | Statement |
| Privilege Model | Requires DDL/administrative privilege according to target object scope. |

## Purpose

Executes the SHOW SCHEMAS SQL command with MonkDB distributed runtime semantics.

## Syntax

```sql
SHOW SCHEMAS [LIKE 'pattern' | WHERE expression];
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
The `SHOW SCHEMAS` command in MonkDB is used to list all the schemas (namespaces) defined within the current MonkDB cluster.

In MonkDB, schemas help organize tables, views, and other database objects logically. This is particularly useful in multi-tenant applications or for structuring large databases.

## SQL Statement

```sql
SHOW SCHEMAS [LIKE 'pattern' | WHERE expression];
```

## Description

- Returns a list of schema names, sorted alphabetically.
- Includes default schemas like `monkdb`, `information_schema`, `pg_catalog`, etc.
- You can filter results using `LIKE` or `WHERE`.

## Examples
### Example 1. Show all schemas

```sql
SHOW SCHEMAS;
```

Typical output

```text
monkdb
information_schema
pg_catalog
sys
```

### Example 2. Filter schemas using `LIKE`

```sql
SHOW SCHEMAS LIKE 'monk%';
```

This matches all schema names starting with `monk` (case-insensitive).

### Example 3. Use `WHERE` for complex conditions

```sql
SHOW SCHEMAS WHERE schema_name != 'pg_catalog';
```

## Default Schemas in MonkDB

This uses a boolean condition to filter results. You can use any SQL-compatible [expression](../11_monkdb_value_expressions.md).

| Schema Name          | Purpose                                                        |
|----------------------|----------------------------------------------------------------|
| `monkdb`                | Default schema for user-created tables                        |
| `information_schema` | Metadata about tables, columns, schemas, etc. (read-only)     |
| `pg_catalog`         | PostgreSQL compatibility layer (for clients/tools that expect PG) |
| `sys`                | MonkDB-specific system information (cluster, nodes, tables, etc.) |

## Use Cases

- **Multi-tenancy**: You might create separate schemas per tenant or application domain.
- **Metadata introspection**: Combine with other metadata queries to build a full database map.
- **DevOps/Automation**: Use in tooling/scripts to dynamically fetch and work with schemas.

## 🆚 vs SHOW TABLES

- `SHOW SCHEMAS` → Lists namespaces (organizational level)
- `SHOW TABLES` → Lists tables within a specific schema (typically monkdb)

---

## See Also

- [Show Tables](./75_SHOW_TABLES.md)
