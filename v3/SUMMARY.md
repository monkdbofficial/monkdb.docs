# Documentation Summary

## Releases

- [Release Notes](./release.md)

## Getting Started

- [Introduction](./getting-started/00-introduction.md)
- [Quickstart](./getting-started/01-quickstart.md)
- [System Prerequisites](./getting-started/02-system-prerequisites.md)
- [Provisioning with Docker Image](./getting-started/03-provisioning-docker-image.md)
- [monkdb.yaml / monkdb.yml Guide](./getting-started/04-monkdb-yaml.md)

## Architecture

- [Overview](./architecture/01-overview.md)
- [Storage, Consistency, Resiliency](./architecture/02-storage-consistency-resiliency.md)
- [Scaling and Clustering](./architecture/03-scaling-clustering.md)

## Deployment

- [Docker Compose (3-node)](./deployment/01-docker-compose-3node.md)
- [Production Topologies](./deployment/02-production-topologies.md)
- [Kubernetes Deployment Principles](./deployment/03-kubernetes.md)
- [Configuration and Settings](./deployment/04-configuration.md)
- [Cluster Arguments Reference](./deployment/05-cluster-arguments-reference.md)

## SQL

- [SQL Reference Overview](SQL/01-sql-reference.md)
- [DDL](SQL/02-ddl.md)
- [DML](SQL/03-dml.md)
- [DQL](SQL/04-dql.md)
- [Functions Overview](SQL/05-functions-overview.md)
- [Scalar Functions Catalog](SQL/06-scalar-functions.md)
- [Scalar Functions Detailed Index](SQL/scalar-functions/README.md)
- [Scalar Function Matrix](SQL/scalar-functions/function-matrix.md)
- [UDFs](SQL/07-udfs.md)
- [SQL Command Catalog](SQL/08-command-catalog.md)
- [SQL Commands (Individual Pages)](SQL/commands/README.md)
- [SQL Constraints](SQL/10_monkdb_sql_constraints.md)
- [SQL Value Expressions](SQL/11_monkdb_value_expressions.md)

## Workloads

- [Workloads Overview](./workloads/00-workloads-overview.md)
- [Time-Series Workloads](./workloads/01-time-series.md)
- [Vector Workloads](./workloads/02-vector-search.md)
- [Full-Text Search Workloads](./workloads/03-full-text-search.md)
- [Geospatial Workloads](./workloads/04-geospatial.md)
- [Document/JSON Workloads](./workloads/05-document-json.md)
- [BLOB Workloads](./workloads/06-blob.md)
- [Graph Workloads](./workloads/07-graph.md)
- [Memory Workloads](./workloads/08-memory.md)
- [Governance Controls Workloads](./workloads/09-governance-controls.md)

## Governance

- [Governance Overview](./governance/00-overview.md)
- [Row Filter Policies](./governance/01-row-filter-policies.md)
- [Column Masking Policies](./governance/02-column-masking-policies.md)
- [Contracts and Validation](./governance/03-contracts-and-validation.md)
- [Audit Operations](./governance/04-audit-operations.md)
- [Lineage Operations](./governance/05-lineage-operations.md)
- [AI Usage Policies](./governance/06-ai-usage-policies.md)

## Features

- [FLOAT_VECTOR Similarity](./features/float-vector-similarity.md)
- [UUID Data Type](./features/uuid.md)
- [FDW: JDBC](./features/fdw-jdbc.md)
- [FDW: Iceberg](./features/fdw-iceberg.md)
- [Graph and Gremlin Gateway](./features/graph-and-gremlin.md)
- [Memory](./features/memory.md)
- [Governance, Audit, Lineage](./features/governance-audit-lineage.md)
- [Governance E2E Lab](./features/governance-e2e-lab.md)
- [Geospatial WKB and 3D Retention](./features/geospatial-wkb-3d.md)
- [Financial Protocol Ingest](./features/financial-wire-protocols.md)
- [License Management](./features/licensing.md)

## Operations

- [Monitoring](./operations/monitoring.md)
- [Memory and Circuit Breakers](./operations/memory-and-circuit-breakers.md)
- [Diagnostics with System Tables](./operations/diagnostics-system-tables.md)
- [Snapshots and Restore](./operations/snapshots-restore.md)
- [Security, Auth, RBAC](./operations/security-auth-rbac.md)
- [Endpoints (HTTP/PGWire)](./operations/endpoints.md)
- [Logical Replication](./operations/logical-replication.md)
- [Java Flight Recorder (JFR)](./operations/jfr.md)
- [Query Optimization](./operations/query-optimization.md)
- [License Provisioning for Larger Clusters](./operations/license-provisioning-large-cluster.md)
- [Production Runbook](./operations/production-runbook.md)

## References

- [FDW Options Reference](./references/fdw-options-reference.md)
- [Environment Variables and Runtime Flags](./references/environment-variables.md)
- [SQL Grammar: New Statement Families](./references/sql-grammar-new-statements.md)
- [Scalar Function Discovery](./references/scalar-function-discovery.md)
