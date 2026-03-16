# json_extract_path

> Enterprise scalar function reference.

## Function Snapshot

| Field | Value |
| --- | --- |
| Function | json_extract_path |
| Category | JSON and Object |
| Scope | Scalar expression |
| Discovery | SELECT * FROM pg_catalog.pg_proc WHERE proname = 'json_extract_path'; |

## Purpose

Navigates a JSON or object path and returns raw or text representation of the value.

## Syntax

~~~sql
SELECT json_extract_path({"a":{"b":42}}, 'a', 'b');
~~~

## Parameters

- json_obj: input object or array structure.
- path...: one or more text path elements.

## Returns

- Returns extracted JSON/object value (dynamic type).

## Null and Error Behavior

- Missing keys/path elements generally return original/no-match semantics (path dependent).

## Operational Notes

- Use schema-qualified objects and parameterized queries for production pipelines.
- Validate overload details in-cluster with pg_catalog.pg_proc and pg_get_function_result(oid).

## Cross-References

- [Scalar Functions Index](../README.md)
- [Scalar Function Discovery](../../../references/scalar-function-discovery.md)
- [SQL Functions Overview](../../05-functions-overview.md)
