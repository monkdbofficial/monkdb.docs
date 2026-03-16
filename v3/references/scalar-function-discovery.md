# Scalar Function Discovery

The scalar surface is broad and evolves over releases. Use SQL discovery queries for authoritative in-cluster visibility.

## Discover functions via `pg_catalog`

```sql
SELECT proname,
       oid::int,
       pg_get_function_result(oid) AS return_type
FROM pg_catalog.pg_proc
ORDER BY proname;
```

## Discover overloads and argument signatures

```sql
SELECT proname,
       pg_get_function_result(oid) AS return_type,
       pg_get_expr(proargdefaults, 0) AS defaults
FROM pg_catalog.pg_proc
WHERE proname IN ('date_part', 'regexp_like', 'json_set', 'array_intersect', 'vector_similarity')
ORDER BY proname;
```

## Suggested verification workflow

1. Query `pg_catalog.pg_proc` for target function names.
2. Run small `SELECT` examples in a scratch schema.
3. Validate null/error behavior with edge-case inputs.

## Registry families (implementation groups)

Current scalar registry includes modules for:

- arithmetic, bitwise, casts
- string and regex
- date/time and intervals
- arrays and object/json
- geospatial
- conditional
- postgres-compat and privilege helpers
- graph helpers
- vector similarity and kNN predicates
- UUID generation and parsing helpers
