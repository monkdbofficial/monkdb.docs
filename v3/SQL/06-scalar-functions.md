# Scalar Functions

MonkDB exposes a broad scalar function surface across numeric analytics, date/time, text, arrays, JSON/object operations, geospatial/vector, graph helpers, compatibility layers, and security introspection.

## Detailed scalar reference

- [Scalar Functions Detailed Index](./scalar-functions/README.md)
- [Scalar Function Matrix](./scalar-functions/function-matrix.md)
- [Scalar Function Discovery](../references/scalar-function-discovery.md)

## Key additions

- Vector similarity override support on `vector_similarity` and `knn_match` with strict literal validation.
- PostgreSQL compatibility helpers: `date_part`, `to_timestamp`, `from_unixtime`, regex family, `gen_random_uuid`, `uuid_generate_v4`.
- JSON/object utility set: `json_extract_path`, `json_set`/`jsonb_set`, `json_delete_path`, `json_each`, `json_typeof`, `json_contains`.
- Analytics helpers: `width_bucket`/`bucket`, `percentile_cont`, `zscore`, `normalize`, `try_parse_*`.

## Recommended validation workflow

1. Discover signatures in-cluster:

~~~sql
SELECT proname, pg_get_function_result(oid)
FROM pg_catalog.pg_proc
ORDER BY proname;
~~~

2. Verify target overload and behavior in a scratch schema.
3. Parameterize production queries and avoid ambiguous implicit coercions.
