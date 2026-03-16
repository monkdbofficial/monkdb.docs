# knn_match

> Enterprise scalar function reference.

## Function Snapshot

| Field | Value |
| --- | --- |
| Function | knn_match |
| Category | Vector |
| Scope | Scalar expression |
| Discovery | SELECT * FROM pg_catalog.pg_proc WHERE proname = 'knn_match'; |

## Purpose

Applies approximate nearest-neighbor filtering for FLOAT_VECTOR columns in WHERE clauses.

## Syntax

~~~sql
SELECT id
FROM doc.items
WHERE knn_match(embedding, [0.1, 0.2, 0.3]::float_vector(3), 10);
~~~

## Parameters

- vector_column: FLOAT_VECTOR(N) column.
- query_vector: vector literal or parameter with matching dimensions.
- k: number of nearest neighbors to match.
- Optional similarity: literal, non-null, must match column similarity.

## Returns

- Returns boolean predicate result for ANN filtering.

## Null and Error Behavior

- Similarity override must be a non-null literal string.
- Override mismatch with column-declared similarity fails at planning.

## Operational Notes

- Use inside WHERE to trigger vector index execution; pair with ORDER BY vector_similarity(...) for ranking output.
- Validate overload details in-cluster with pg_catalog.pg_proc and pg_get_function_result(oid).

## Cross-References

- [Scalar Functions Index](../README.md)
- [Scalar Function Discovery](../../../references/scalar-function-discovery.md)
- [SQL Functions Overview](../../05-functions-overview.md)
