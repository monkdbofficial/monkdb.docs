# has_database_privilege

> Enterprise scalar function reference.

## Function Snapshot

| Field | Value |
| --- | --- |
| Function | has_database_privilege |
| Category | Privileges and Security |
| Scope | Scalar expression |
| Discovery | SELECT * FROM pg_catalog.pg_proc WHERE proname = 'has_database_privilege'; |

## Purpose

Evaluates whether a user has the requested privilege at the target scope.

## Syntax

~~~sql
SELECT has_database_privilege('monkdb', 'DQL');
~~~

## Parameters

- Positional arguments as defined by overload signatures in pg_catalog.pg_proc.

## Returns

- Returns boolean.

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
