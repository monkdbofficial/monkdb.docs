# json_set

> Enterprise scalar function reference.

## Function Snapshot

| Field | Value |
| --- | --- |
| Function | json_set |
| Category | JSON and Object |
| Scope | Scalar expression |
| Discovery | SELECT * FROM pg_catalog.pg_proc WHERE proname = 'json_set'; |

## Purpose

Writes or updates a value at a JSON path with optional create_missing behavior.

## Syntax

~~~sql
SELECT json_set({"a":{"b":1}}, ['a','c'], 2, true);
~~~

## Parameters

- json_obj: input object.
- path: array(string) path segments.
- new_value: scalar/object/array value to write.
- Optional create_missing: boolean flag (default true).

## Returns

- Returns updated object value.

## Null and Error Behavior

- create_missing=false preserves original when path does not exist.
- Null create_missing input yields null result.

## Operational Notes

- Use schema-qualified objects and parameterized queries for production pipelines.
- Validate overload details in-cluster with pg_catalog.pg_proc and pg_get_function_result(oid).

## Cross-References

- [Scalar Functions Index](../README.md)
- [Scalar Function Discovery](../../../references/scalar-function-discovery.md)
- [SQL Functions Overview](../../05-functions-overview.md)
