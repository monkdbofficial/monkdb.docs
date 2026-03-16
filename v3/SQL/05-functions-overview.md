# Functions Overview

MonkDB function surface includes:

- Scalar functions
- Aggregate functions
- Table functions
- User-defined functions (UDFs)

## Function classes

## Scalar functions

Used in projection, filters, expressions, computed columns.

Examples:

```sql
SELECT lower(name), date_part('day', current_timestamp), array_length(tags, 1)
FROM doc.users;
```

## Aggregate functions

Used with grouping/aggregation pipelines.

Examples: `count`, `sum`, `avg`, `min`, `max`, percentile families.

## Table functions

Return row sets and are used in `FROM`.

Examples in graph domain:

- `graph_neighbors(...)`
- `traverse(...)`

## UDFs

Defined via `CREATE FUNCTION` and callable like built-in functions.

## Function discovery

Use runtime catalog queries to inspect the exact function set in your running build:

```sql
SELECT proname, oid::int
FROM pg_catalog.pg_proc
ORDER BY proname;
```

For workflows and examples, continue with:

- [Scalar Functions Catalog](./06-scalar-functions.md)
- [Scalar Functions Detailed Index](./scalar-functions/README.md)
- [Scalar Function Matrix](./scalar-functions/function-matrix.md)
- [UDFs](./07-udfs.md)
