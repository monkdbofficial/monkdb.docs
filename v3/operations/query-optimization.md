# Query Optimization

## Baseline process

1. Identify expensive queries from `sys.jobs` / `sys.jobs_log`.
2. Inspect operation-level memory and runtime from `sys.operations*`.
3. Reduce scanned data with partition filters and selective predicates.
4. Validate join keys and avoid accidental cross joins.
5. Tune shard/replica strategy for dominant workload shape.

## High-impact practices

- Filter early and on indexed columns.
- Use time partition pruning for large event tables.
- Pre-aggregate where recurring dashboards re-run the same heavy query.
- Limit result sets (`LIMIT`) and project only needed columns.

## Vector + lexical hybrid

When combining `KNN_MATCH` and full-text:

- Keep vector candidate set bounded.
- Re-rank with lexical/business signals in final projection/order step.

## Memory-sensitive queries

- Watch breaker exceptions and large merge phases.
- Reduce concurrent heavy joins/aggregations during peak ingest windows.
