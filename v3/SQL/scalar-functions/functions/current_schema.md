# current_schema

> Enterprise scalar function reference.

## Function Snapshot

| Field | Value |
| --- | --- |
| Function | current_schema |
| Category | Postgres Compatibility and System |
| Scope | Scalar expression |
| Discovery | SELECT * FROM pg_catalog.pg_proc WHERE proname = 'current_schema'; |

## Purpose

Returns server or session metadata for compatibility and diagnostics.

## Syntax

~~~sql
SELECT current_schema();
~~~

## Parameters

- No arguments.

## Returns

- Returns function-specific scalar/array/object according to resolved overload.

## Null and Error Behavior

- Most overloads are deterministic and null-propagating unless documented otherwise.
- Validate concrete overload behavior with pg_catalog.pg_proc in your running build.

## Operational Notes

- This function exists mainly for PostgreSQL tooling compatibility and metadata introspection.
- Validate overload details in-cluster with pg_catalog.pg_proc and pg_get_function_result(oid).

## Cross-References

- [Scalar Functions Index](../README.md)
- [Scalar Function Discovery](../../../references/scalar-function-discovery.md)
- [SQL Functions Overview](../../05-functions-overview.md)
