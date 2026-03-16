# array_reverse

> Enterprise scalar function reference.

## Function Snapshot

| Field | Value |
| --- | --- |
| Function | array_reverse |
| Category | Arrays and Collections |
| Scope | Scalar expression |
| Discovery | SELECT * FROM pg_catalog.pg_proc WHERE proname = 'array_reverse'; |

## Purpose

Executes the scalar function array reverse as registered in the MonkDB scalar function registry.

## Syntax

~~~sql
SELECT array_reverse([1,2,3], [2,3,4]);
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
