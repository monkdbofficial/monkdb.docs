# extract_day_of_week

> Enterprise scalar function reference.

## Function Snapshot

| Field | Value |
| --- | --- |
| Function | extract_day_of_week |
| Category | Date and Time |
| Scope | Scalar expression |
| Discovery | SELECT * FROM pg_catalog.pg_proc WHERE proname = 'extract_day_of_week'; |

## Purpose

Executes the scalar function extract day of week as registered in the MonkDB scalar function registry.

## Syntax

~~~sql
SELECT extract_day_of_week(current_timestamp);
~~~

## Parameters

- Timestamp/date/interval expression depending on field.

## Returns

- Returns function-specific scalar/array/object according to resolved overload.

## Null and Error Behavior

- Unsupported extract fields raise an error.
- extract_epoch returns floating-point seconds.

## Operational Notes

- Use schema-qualified objects and parameterized queries for production pipelines.
- Validate overload details in-cluster with pg_catalog.pg_proc and pg_get_function_result(oid).

## Cross-References

- [Scalar Functions Index](../README.md)
- [Scalar Function Discovery](../../../references/scalar-function-discovery.md)
- [SQL Functions Overview](../../05-functions-overview.md)
