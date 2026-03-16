# WITH

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | DQL |
| Mutates Data | No |
| Scope | Statement |
| Privilege Model | Requires read privilege (DQL) on referenced relations. |

## Purpose

Executes the WITH SQL command with MonkDB distributed runtime semantics.

## Syntax

```sql
WITH with_query [, ...]
SELECT ...
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
The `WITH` clause defines named subqueries that you can refer to as temporary tables in your main `SELECT` query. These subqueries exist only for the duration of that query.

This improves:
- Query clarity
- Reusability of logic
- Performance (especially when using the same derived table multiple times)

## SQL Statement

```sql
WITH with_query [, ...]
SELECT ...
```

Where a with_query is defined as:

```sql
name [ (column1, column2, ...) ] AS (
    SELECT ...
)
```

## Notes
- Each `with_query` must have a unique name.
- You can define multiple subqueries separated by commas.
- Column names can be explicitly declared or inferred from the subquery.
- CTEs cannot be used across different SQL statements — they’re scoped only to the current query.

## Basic Example

```sql
WITH recent_orders AS (
  SELECT * FROM orders WHERE order_date >= current_date - INTERVAL '30 days'
)
SELECT customer_id, COUNT(*) AS order_count
FROM recent_orders
GROUP BY customer_id;
```

`recent_orders` is a temporary named result set (CTE).

It filters recent orders, then the outer query aggregates by `customer_id`.

## Example with Column Aliases

```sql
WITH region_sales (region, total_sales) AS (
  SELECT region, SUM(amount) FROM sales GROUP BY region
)
SELECT * FROM region_sales WHERE total_sales > 100000;
```

- Declares columns `region` and `total_sales` explicitly.
- Makes the final query more self-descriptive and readable.

## Multiple CTEs

You can define and chain multiple CTEs:

```sql
WITH top_customers AS (
    SELECT customer_id, SUM(total) AS total_spent
    FROM orders
    GROUP BY customer_id
    HAVING SUM(total) > 5000
),
customer_names AS (
    SELECT id, name FROM customers
)
SELECT c.name, t.total_spent
FROM top_customers t
JOIN customer_names c ON c.id = t.customer_id;
```

## Why Use `WITH` in MonkDB?

- Break complex queries into logical parts
- Avoid repeating long subqueries or filters
- Improve maintainability of SQL
- Act as inline read-only temp views

## Limitations in MonkDB

| Feature | Status in MonkDB |
|---------|-------------------|
| Recursive CTEs | No Not supported |
| INSERT/UPDATE with CTE | Yes Supported (for INSERT) |
| CTEs in DML | Yes WITH for INSERT works |
| Reusing across queries | No Not supported — scoped per query |

## INSERT Example with WITH

```sql
WITH valid_users AS (
  SELECT id, email FROM users WHERE email IS NOT NULL
)
INSERT INTO audit_log (user_id, message)
SELECT id, 'Email validated' FROM valid_users;
```

## CTE vs Subquery — When to Use

| Use Case | Subquery | CTE (WITH) |
|----------|----------|------------|
| Simple filter or join | Yes Good | Moderate Overhead |
| Reuse same subquery multiple times | No Verbose | Yes Cleaner |
| Step-by-step logic | No Hard to follow | Yes Easy to structure |
| Recursive queries | No (N/A) | No Not supported |

## CTE + RETURNING (for supported DML)

```sql
WITH to_insert AS (
  SELECT * FROM (VALUES (1, 'Alpha'), (2, 'Beta')) AS v(id, name)
)
INSERT INTO tags (id, name)
SELECT id, name FROM to_insert
RETURNING *;
```
