# percentile_cont

> Enterprise scalar function reference.

## Function Snapshot

| Field | Value |
| --- | --- |
| Function | percentile_cont |
| Category | Numeric and Analytics |
| Scope | Scalar expression |
| Discovery | SELECT * FROM pg_catalog.pg_proc WHERE proname = 'percentile_cont'; |

## Purpose

Computes continuous percentile from an ordered numeric array input.

## Syntax

~~~sql
SELECT percentile_cont(0.95, [10.0, 20.0, 30.0, 40.0]);
~~~

## Parameters

- Positional arguments as defined by overload signatures in pg_catalog.pg_proc.

## Returns

- Returns function-specific scalar/array/object according to resolved overload.

## Null and Error Behavior

- Most overloads are deterministic and null-propagating unless documented otherwise.
- Validate concrete overload behavior with pg_catalog.pg_proc in your running build.

## Operational Notes

- Use schema-qualified objects and parameterized queries for production pipelines.
- Validate overload details in-cluster with pg_catalog.pg_proc and pg_get_function_result(oid).

## Cross-References

- [Scalar Functions Index](../README.md)
- [Scalar Function Discovery](../../../references/scalar-function-discovery.md)
- [SQL Functions Overview](../../05-functions-overview.md)
