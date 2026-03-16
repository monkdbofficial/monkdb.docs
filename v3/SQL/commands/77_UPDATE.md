# UPDATE

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | DML |
| Mutates Data | Yes/Depends |
| Scope | Statement |
| Privilege Model | Requires write privilege (DML) and read privilege where predicates reference source relations. |

## Purpose

Mutates table rows while honoring MonkDB indexing, routing, and write-path semantics.

## Syntax

```sql
UPDATE table_ident [ [AS] table_alias ]
SET column1 = expression1 [, column2 = expression2, ...]
[WHERE condition]
[RETURNING { * | expression [AS alias] | relation.* } [, ...]];
```

## Operational Notes

- Use schema-qualified identifiers in automation and automation pipelines.
- Validate behavior in staging for cluster-impacting or governance-impacting changes.
- Confirm runtime effects through system tables and metrics before and after execution.

## When to Use

- Use for controlled data mutations and ingest/export workflows.
- Use when transactional scope is statement-level and operational visibility is available.

## When Not to Use

- Avoid large write bursts without capacity checks for breakers, disk, and shard health.
- Avoid ad-hoc production mutations without clear idempotency or rollback plan.

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
The `UPDATE` statement is used to modify existing rows in a table. You can update one or more columns, conditionally target specific rows using a `WHERE` clause, and even return updated values using `RETURNING`.

MonkDB supports rich expressions in both the `SET` clause and `RETURNING`, making updates powerful and flexible; especially useful when dealing with object-type columns, arrays, or complex filters.

## SQL Statement

```sql
UPDATE table_ident [ [AS] table_alias ]
SET column1 = expression1 [, column2 = expression2, ...]
[WHERE condition]
[RETURNING { * | expression [AS alias] | relation.* } [, ...]];
```

## Parameters
### table_ident

The name of the target table. It can be schema-qualified:

```sql
UPDATE monkdb.my_table ...
```

### table_alias

A temporary name for the table in this query. Required if you want to reference the table with a shorter alias:

```sql
UPDATE users AS u SET u.active = false WHERE u.last_login < now() - INTERVAL '1 year';
```

When an alias is used, the table must be referred to by that alias in the rest of the query.

### SET column = expression

Defines which columns to update and what values to assign. You can:

- Use expressions (e.g., math, string functions)
- Use object/array subscript notation
- Use other columns from the same row

```sql
UPDATE metrics SET value = value * 1.1;
UPDATE users SET metadata['last_updated'] = now();
```

### WHERE condition

Controls which rows are updated. Only rows where the condition evaluates to `TRUE` will be modified.

Examples:

```sql
UPDATE orders SET status = 'cancelled' WHERE status = 'pending' AND created_at < now() - INTERVAL '30 days';
```

### RETURNING

Returns the result of the update operation — after the update is applied.

```sql
UPDATE employees SET salary = salary * 1.05
WHERE department = 'engineering'
RETURNING name, salary;
```

This is especially useful when:
- You need to see what was changed
- You’re using MonkDB programmatically and want to capture the result of updates without a follow-up `SELECT`.

## Working with Complex Types

MonkDB supports nested object fields and arrays, so you can update them directly using subscript syntax.

Update an object field:

```sql
UPDATE devices SET config['threshold'] = 70 WHERE id = 'dev42';
```

Update an array element:

```sql
UPDATE sensors SET tags[1] = 'critical' WHERE id = 'sensor123';
```

## Notes

| Feature | Supported in MonkDB? | Notes |
|---------|-----------------------|-------|
| Multi-table `UPDATE` | No No | Only one table can be updated at a time |
| `JOIN` in `UPDATE` | No No | Not supported (workaround: precompute IDs in a subquery) |
| Subqueries in `SET` | No Limited | Only scalar expressions allowed in SET |
| Object & array updates | Yes Yes | Supports deep updates into nested structures |
| `RETURNING` clause | Yes Yes | Very useful in pipelines or when debugging |

## Examples
### Example 1. Mark users inactive

```sql
UPDATE users SET active = false
WHERE last_login < now() - INTERVAL '6 months'
RETURNING id, email;
```

### Example 2. Increment time series value

```sql
UPDATE metrics SET value = value + 1
WHERE series_id = 'temp_sensor_001' AND ts = '2025-04-01T10:00:00Z';
```

### Example 3. Update nested object field

```sql
UPDATE logs SET metadata['severity'] = 'high'
WHERE message ILIKE '%error%';
```

## Performance Consideration in MonkDB

- Updates in MonkDB are internally handled as copy-on-write: the row is reindexed.
- Avoid frequent updates in high-ingest time series scenarios. Instead, consider event-based modeling or append-only logs when possible.
- If performance becomes an issue, consider bulk updates during low-usage hours.
