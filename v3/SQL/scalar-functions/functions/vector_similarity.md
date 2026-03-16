# vector_similarity

> Enterprise scalar function reference.

## Function Snapshot

| Field | Value |
| --- | --- |
| Function | vector_similarity |
| Category | Vector |
| Scope | Scalar expression |
| Discovery | SELECT * FROM pg_catalog.pg_proc WHERE proname = 'vector_similarity'; |

## Purpose

Computes similarity score between vectors using the column default or explicit similarity override.

## Syntax

~~~sql
SELECT vector_similarity(
  [0.1, 0.2, 0.3]::float_vector(3),
  [0.2, 0.1, 0.4]::float_vector(3)
);
~~~

## Parameters

- left_vector, right_vector: vectors with identical dimensions.
- Optional similarity: literal, non-null override; must match column similarity when used against indexed vectors.

## Returns

- Returns numeric similarity score (double precision).

## Null and Error Behavior

- Similarity override must be a non-null literal string.
- Override mismatch with column-declared similarity fails at planning.

## Operational Notes

- Prefer relying on column-declared similarity unless an explicit literal override is required.
- Validate overload details in-cluster with pg_catalog.pg_proc and pg_get_function_result(oid).

## Cross-References

- [Scalar Functions Index](../README.md)
- [Scalar Function Discovery](../../../references/scalar-function-discovery.md)
- [SQL Functions Overview](../../05-functions-overview.md)
