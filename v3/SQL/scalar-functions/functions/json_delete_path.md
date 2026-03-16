# json_delete_path

> Enterprise scalar function reference.

## Function Snapshot

| Field | Value |
| --- | --- |
| Function | json_delete_path |
| Category | JSON and Object |
| Scope | Scalar expression |
| Discovery | SELECT * FROM pg_catalog.pg_proc WHERE proname = 'json_delete_path'; |

## Purpose

Removes JSON content at a key or path and returns the updated object.

## Syntax

~~~sql
SELECT json_delete_path({"a":{"b":1}}, ['a','b']);
~~~

## Parameters

- Positional arguments as defined by overload signatures in pg_catalog.pg_proc.

## Returns

- Returns updated object value.

## Null and Error Behavior

- Missing keys/path elements generally return original/no-match semantics (path dependent).

## Operational Notes

- Use schema-qualified objects and parameterized queries for production pipelines.
- Validate overload details in-cluster with pg_catalog.pg_proc and pg_get_function_result(oid).

## Cross-References

- [Scalar Functions Index](../README.md)
- [Scalar Function Discovery](../../../references/scalar-function-discovery.md)
- [SQL Functions Overview](../../05-functions-overview.md)
