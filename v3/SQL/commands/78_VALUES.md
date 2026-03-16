# VALUES

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | DQL |
| Mutates Data | No |
| Scope | Statement |
| Privilege Model | Requires read privilege (DQL) on referenced relations. |

## Purpose

Executes the VALUES SQL command with MonkDB distributed runtime semantics.

## Syntax

```sql
VALUES ( expression1 [, expression2, ...] ),
       ( expression1 [, expression2, ...] ),
       ...
```

## Operational Notes

- Use schema-qualified identifiers in automation and automation pipelines.
- Validate behavior in staging for cluster-impacting or governance-impacting changes.
- Confirm runtime effects through system tables and metrics before and after execution.

## When to Use

- Use for read/analytics workloads where query correctness and plan shape are primary concerns.
- Use when you need SQL-native filtering, joins, aggregation, or explainability.

## When Not to Use

- Avoid for heavy recurring ETL if precomputed tables or materialized pipelines are more efficient.
- Avoid unbounded scans in production without partition or predicate controls.

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
The `VALUES` expression is used to generate a result set of constant rows. It's like a virtual table that exists only for the duration of the query.

It can be:
- Queried directly (`SELECT`).
- Used in `INSERT` statements.
- Joined with other tables (in subqueries or CTEs).

## SQL Statement

```sql
VALUES ( expression1 [, expression2, ...] ),
       ( expression1 [, expression2, ...] ),
       ...
```

Each tuple (row) must have the same number of columns, and types must be consistent or implicitly castable (e.g., 1 and '1' would cause an error).

## Basic Example

```sql
VALUES (1, 'one'), (2, 'two'), (3, 'three');
```

Output:

| col1 | col2    |
|------|---------|
| 1    | one     |
| 2    | two     |
| 3    | three   |

## Use Cases in MonkDB
### 1. Yes Quick test datasets

You can use `VALUES` to return ad-hoc rows — great for testing functions, formatting, or expressions.

```sql
SELECT * FROM (
  VALUES (100, 'active'), (200, 'inactive')
) AS status_counts(id, status);
```

### 2. Yes Insert rows into a table

This is the most common use of `VALUES`.

```sql
INSERT INTO products (id, name, price)
VALUES (1, 'Keyboard', 49.99),
       (2, 'Mouse', 19.99),
       (3, 'Monitor', 129.99);
```

Each tuple maps to the column order defined.

### 3. Yes Use with JOIN or IN via subqueries

`VALUES` can be used as an inline table in a `JOIN`, `IN`, or `EXISTS` clause.
Example: Filter real table using `VALUES`

```sql
SELECT * FROM employees
WHERE department IN (
  SELECT col1 FROM (VALUES ('Engineering'), ('Sales')) AS temp(col1)
);
```

### 4. Yes UNION-friendly mock data

Combine `VALUES` with `UNION ALL` for static sets:

```sql
SELECT * FROM (
  VALUES ('MonkDB', 'Database'), ('PostgreSQL', 'Database'), ('Redis', 'Cache')
) AS tech(name, type)
WHERE type = 'Database';
```

## Type Consistency Rules

- All values in the same column position across rows must have compatible types.
- MonkDB will try implicit conversion, but mismatched types like 1 and 'one' in the same column will raise errors.

```sql
-- No Will fail due to type mismatch:
VALUES (1, 'one'), ('two', 2);
```

## Use with RETURNING

You can `INSERT` using `VALUES` and return the inserted values:

```sql
INSERT INTO cities (id, name)
VALUES (1, 'Berlin'), (2, 'Mumbai')
RETURNING *;
```

## Not Supported

| Feature                    | MonkDB Support | Notes                                      |
|----------------------------|-----------------|--------------------------------------------|
| `DEFAULT` in `VALUES`          | No Not supported | Must explicitly provide all values         |
| Multi-column type mismatch | No Error        | Ensure consistent column types             |
| Named `VALUES` without alias | No Error-prone   | Use `AS alias(col1, col2)` when needed       |

## Best Practices
- Use column aliases when selecting from `VALUES` to make the result clearer.
- When inserting, make sure column order and count match the target table.
- Great for bulk inserts, ad-hoc joins, and inline filtering.
