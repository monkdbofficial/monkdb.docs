# Production Topologies

## Single region, multi-AZ baseline

- 3+ master-eligible data nodes.
- At least one replica for critical tables.
- Zone-aware node spread and shard allocation awareness.

## Large analytics cluster

- Separate ingest-heavy and query-heavy workloads by node sizing.
- Increase replicas for read-heavy dashboards.
- Partition large fact tables by time.

## Hybrid operational + AI/search workload

- Co-locate structured rows with vectors and text for hybrid search.
- Use `FLOAT_VECTOR` + `MATCH` pipelines for relevance blending.
- Keep query memory protections (breakers) tuned.

## Docker Swarm

MonkDB runs in Swarm, but stateful scheduling and volume guarantees need strict ops discipline.

- Prefer node labels for deterministic placement.
- Ensure persistent volumes follow service constraints.
- Control rolling updates to avoid shard churn.

## Recommended production defaults

- JVM heap explicitly set.
- TLS enabled for HTTP/PGWire/transport as required.
- Snapshot repositories configured early.
- Monitoring stack enabled before go-live.
