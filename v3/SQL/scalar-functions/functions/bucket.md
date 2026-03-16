# bucket

> Enterprise scalar function reference.

## Function Snapshot

| Field | Value |
| --- | --- |
| Function | bucket |
| Category | Numeric and Analytics |
| Scope | Scalar expression |
| Discovery | SELECT * FROM pg_catalog.pg_proc WHERE proname = 'bucket'; |

## Purpose

Assigns numeric values into equi-width bucket indexes for histogram-style analytics.

## Syntax

~~~sql
SELECT bucket(42.0, 0.0, 100.0, 5);
~~~

## Parameters

- value: numeric value to bucket.
- min, max: bucket bounds (min < max).
- count: positive integer bucket count.

## Returns

- Returns function-specific scalar/array/object according to resolved overload.

## Null and Error Behavior

- count <= 0 raises an error.
- min >= max raises an error.
- Values below min return 0; values >= max return count + 1.

## Operational Notes

- Use schema-qualified objects and parameterized queries for production pipelines.
- Validate overload details in-cluster with pg_catalog.pg_proc and pg_get_function_result(oid).

## Cross-References

- [Scalar Functions Index](../README.md)
- [Scalar Function Discovery](../../../references/scalar-function-discovery.md)
- [SQL Functions Overview](../../05-functions-overview.md)
