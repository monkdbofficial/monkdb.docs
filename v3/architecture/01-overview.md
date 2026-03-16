# Architecture Overview

MonkDB is a distributed, shared-nothing SQL engine designed to combine operational and analytical patterns in one system.

It supports:

- Relational SQL workloads
- Semi-structured JSON/object workloads
- Search (lexical/full-text)
- Vector similarity search
- Geospatial queries
- Time series workloads
- Native memory for agentic and RAG workflows
- Graph modeling and traversal interfaces
- External data federation through FDW
- Unstructured data in the form of blobs

## Design goals

- One engine for mixed SQL/search/vector/geo/graph/timeseries/full text/nosql/blob/memory workloads.
- Horizontal scale through shard-based distribution.
- High observability via system tables and runtime metrics.
- Strong governance controls (policies, contracts, audit, lineage) built into query/runtime path.

## Workload decision table

| If your primary need is... | Prefer | MonkDB capability | Why |
|----------------------------|--------|-------------------|-----|
| Running PostgreSQL-compatible applications | PGWire endpoint | Existing PostgreSQL clients, ORMs, and BI tools connect without modification. |
| Service-to-service SQL execution | HTTP SQL endpoint | Simplifies authentication, routing, and stateless query execution for API-driven systems. |
| Operational + analytical SQL in one engine | Distributed shared-nothing SQL execution | Eliminates the need for separate OLTP and analytics databases. |
| Semi-structured application payloads | OBJECT / JSON columns | Store nested application data without schema fragmentation or ETL pipelines. |
| Semantic search and RAG retrieval | FLOAT_VECTOR(N) + hybrid search | Combines vector similarity and lexical search in a single query path. |
| AI agent memory and state persistence | Native memory tables | Stores agent context, conversation state, and embeddings without external vector databases. |
| Hybrid document retrieval | Full-text + JSON + vector indexing | Enables knowledge search across documents, metadata, and embeddings in one system. |
| Time-series telemetry (IoT, sensors, logs) | Time-series optimized ingestion and querying | Handles high-frequency event streams with efficient storage and time-based queries. |
| Geospatial analytics | geo_point / geo_shape types | Native spatial indexing and queries without a separate GIS database. |
| Graph modeling and relationship traversal | Graph interfaces over relational/object tables | Enables graph queries and traversal without deploying a dedicated graph database. |
| Knowledge graph + vector search workloads | Graph + vector in same table | Supports AI knowledge graphs with semantic retrieval in one platform. |
| Large unstructured artifacts | Blob/object storage columns | Stores documents, images, and artifacts alongside metadata and embeddings. |
| Querying external systems without pipelines | Foreign Data Wrappers (FDW) | Access external databases without data duplication. |
| Hybrid semantic + structured analytics | SQL + vector + full-text in one query | Ranking logic stays inside the query engine rather than external services. |
| Fine-grained governance enforcement | Row filters, column masking, contracts, policies | Governance rules are enforced during query planning and execution. |
| Data usage traceability and compliance | Audit sinks + lineage sinks | Captures query execution, data flow, and access patterns for compliance. |
| Runtime system observability | System tables (sys.jobs, sys.nodes, sys.shards) | Provides deep cluster and query visibility directly through SQL. |
| Financial market data ingestion | Native FIX / ITCH / OUCH / FDC3 protocol support | Converts wire protocols directly into queryable structured data. |
| Cross-protocol trading analytics | Unified market data model | Correlates trader intent, order flow, exchange response, and market state. |
| Building AI + data applications without fragmented stacks | Multi-model engine (SQL + JSON + vector + geo + graph + time-series + blobs) | Replaces multiple specialized data systems with a single distributed platform. |



## Core architecture layers

![Core Architecture Layer](../assets/architectures/monkdb_arch_overview_1.png)


## Control plane and data plane

Control plane responsibilities:

- Cluster membership and node discovery
- Routing metadata (table/shard allocation)
- Dynamic cluster settings
- Policy/contract metadata and governance state

Data plane responsibilities:

- Query execution on shards
- Distributed merge/reduce
- Local indexing/storage lifecycle
- Replication and recovery traffic

## Node-level components

Each node can:

- Accept client traffic
- Parse/analyze/plan SQL
- Execute local shard operations
- Participate in distributed merge/reduce
- Store shard data and replicas

This avoids primary/secondary bottlenecks common in single-writer architectures.

## Query execution lifecycle

![Query exection lifecyle](../assets/architectures/query_exec.png)

Execution stages:

1. Parse and analyze SQL.
2. Resolve table/routing metadata and function signatures.
3. Build distributed plan (collect, merge, sort, join, projection nodes).
4. Dispatch shard-level operators to participating nodes.
5. Stream partial results back to coordinator for final merge.

## Query path decision flow

![Query path decision flow](../assets/architectures/query_path_flow.png)

## Multi-model model-in-one-table pattern

MonkDB allows mixed columns in one table, for example:

- Primary keys and typed relational columns
- Nested object columns for JSON payloads
- `FLOAT_VECTOR(N)` for embeddings
- `geo_point`/`geo_shape` for spatial context

This avoids cross-database synchronization for many applications.

## Governance in runtime path

Governance is enforced during query planning/execution:

- Row filter policies can constrain visible rows.
- Column masking policies can transform selected columns.
- Contracts and AI usage policies can warn/block based on configured modes.
- Audit and lineage sinks emit observability artifacts for policy and data-flow traceability.

## Built-in governance and observability surfaces

- Governance: policies, contracts, lineage, audit sinks
- System diagnostics: `sys.jobs`, `sys.operations`, `sys.nodes`, `sys.shards`, `sys.allocations`
- Information metadata: `information_schema.*`

## Architecture-related references

- [Storage, Consistency, Resiliency](./02-storage-consistency-resiliency.md)
- [Scaling and Clustering](./03-scaling-clustering.md)
- [Monitoring](../operations/monitoring.md)
- [Security, Auth, RBAC](../operations/security-auth-rbac.md)
