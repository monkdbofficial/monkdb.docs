# DECLARE

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | Session and Transaction Control |
| Mutates Data | Yes/Depends |
| Scope | Session / Transaction |
| Privilege Model | Session-scoped variants require session rights; global variants require administrative privilege. |

## Purpose

Executes the DECLARE SQL command with MonkDB distributed runtime semantics.

## Syntax

```sql
DECLARE name [ ASENSITIVE | INSENSITIVE ] [ [ NO ] SCROLL ]
CURSOR [ { WITH | WITHOUT } HOLD ] FOR query
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
The `DECLARE` command in MonkDB is used to create a cursor, which allows efficient retrieval of query results in manageable batches. This is particularly useful for handling large datasets and implementing pagination.

---

## SQL Statement

```sql
DECLARE name [ ASENSITIVE | INSENSITIVE ] [ [ NO ] SCROLL ]
CURSOR [ { WITH | WITHOUT } HOLD ] FOR query
```

In this context, `name` refers to a chosen identifier for the cursor, while `query` represents a `SELECT` statement.

## Description

A cursor allows for the retrieval of a limited number of rows at once from a query that produces a larger result set. Once a cursor is established, rows can be retrieved using the `FETCH` command.

Declared cursors can be found in the `pg_catalog.pg_cursors` table.

## Clauses

### WITH | WITHOUT HOLD

The default setting is `WITHOUT HOLD`, which ties the cursor's lifespan to the duration of a transaction. It is considered an error to use `WITHOUT HOLD` when there is no active transaction initiated by a `BEGIN` statement.

Using `WITH HOLD` alters the cursor's lifespan to match that of the connection.

When a transaction is committed, all cursors established with `WITHOUT HOLD` are closed. Additionally, closing a connection will terminate all cursors created during that connection.

> MonkDB does not fully support transactions. Once a transaction is initiated, it cannot be rolled back, and any write operations within a `BEGIN` clause may be visible to other statements prior to the transaction being committed.

### [ ASENSITIVE | INSENSITIVE ]

This provision is irrelevant as MonkDB Cursors are inherently insensitive.

### [ NO ] SCROLL

The default setting, `NO SCROLL`, indicates that the cursor is restricted to forward movement only.

In contrast, `SCROLL` permits backward navigation with the cursor but introduces additional memory usage.

---

## Examples

### 1. Declaring a Cursor

```sql
BEGIN;
DECLARE sales_cursor NO SCROLL CURSOR FOR
SELECT mobile_brand, unit_sale FROM mobile_sales WHERE unit_sale > 3000;
```

Creates a cursor named `sales_cursor` for fetching rows from the `mobile_sales` table.

### 2. Fetching Data

```sql
FETCH 5 FROM sales_cursor;
```

Retrieves 5 rows at a time from the cursor.

### 3. Closing the Cursor

```sql
END;
```

Ends the transaction and closes all cursors declared with `WITHOUT HOLD`.

---

## See Also

- [Begin](./20_BEGIN.md)
- [Close](./21_CLOSE.md)
- [Fetch](./60_FETCH.md)

