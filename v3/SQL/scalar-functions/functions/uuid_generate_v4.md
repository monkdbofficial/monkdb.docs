# uuid_generate_v4

> Enterprise scalar function reference.

## Function Snapshot

| Field | Value |
| --- | --- |
| Function | uuid_generate_v4 |
| Category | String and Text |
| Scope | Scalar expression |
| Discovery | SELECT * FROM pg_catalog.pg_proc WHERE proname = 'uuid_generate_v4'; |

## Purpose

Generates a random UUID v4 string.

## Syntax

~~~sql
SELECT uuid_generate_v4();
~~~

## Parameters

- No arguments.

## Returns

- Returns UUID string.

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
