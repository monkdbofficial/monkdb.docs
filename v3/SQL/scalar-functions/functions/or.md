# or

> Enterprise scalar function reference.

## Function Snapshot

| Field | Value |
| --- | --- |
| Function | or |
| Category | Numeric and Analytics |
| Scope | Scalar expression |
| Discovery | SELECT * FROM pg_catalog.pg_proc WHERE proname = 'or'; |

## Purpose

Executes the scalar function or as registered in the MonkDB scalar function registry.

## Syntax

~~~sql
SELECT or(10, 3);
~~~

## Parameters

- Positional arguments as defined by overload signatures in pg_catalog.pg_proc.

## Returns

- Returns function-specific scalar/array/object according to resolved overload.

## Null and Error Behavior

- Bit string operands must have equal length; otherwise raises an error.

## Operational Notes

- Use schema-qualified objects and parameterized queries for production pipelines.
- Validate overload details in-cluster with pg_catalog.pg_proc and pg_get_function_result(oid).

## Cross-References

- [Scalar Functions Index](../README.md)
- [Scalar Function Discovery](../../../references/scalar-function-discovery.md)
- [SQL Functions Overview](../../05-functions-overview.md)
