# pg_postmaster_start_time

> Enterprise scalar function reference.

## Function Snapshot

| Field | Value |
| --- | --- |
| Function | pg_postmaster_start_time |
| Category | Postgres Compatibility and System |
| Scope | Scalar expression |
| Discovery | SELECT * FROM pg_catalog.pg_proc WHERE proname = 'pg_postmaster_start_time'; |

## Purpose

Executes the scalar function pg postmaster start time as registered in the MonkDB scalar function registry.

## Syntax

~~~sql
SELECT pg_postmaster_start_time();
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
