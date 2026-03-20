# Introduction

MonkDB is a distributed, multi-model SQL database built for operational and analytical workloads on one platform.

## What MonkDB unifies

- Relational tables and SQL analytics
- Semi-structured JSON/object data
- Full-text search
- Vector similarity search
- Geospatial data (`geo_point`, `geo_shape`)
- BLOB/object-like binary storage
- Graph metadata and traversal helpers
- Governance, audit, lineage, contracts, and policies

## Why teams adopt it

- One SQL surface across multiple data models
- Shared-nothing cluster architecture for horizontal scale
- Near real-time indexing and queryability
- PGWire + HTTP endpoints for broad tool compatibility
- Production operations support (monitoring, snapshots, security)

## Suggested reading order

1. Start with [Quickstart](./01-quickstart.md)
2. Validate host tuning in [System Prerequisites](./02-system-prerequisites.md)
3. Provision a node with [Provisioning with Docker Image](./03-provisioning-docker-image.md)
4. Configure runtime defaults in [monkdb.yaml / monkdb.yml Guide](./04-monkdb-yaml.md)
5. Choose deployment path from [Deployment](../deployment/01-docker-compose-2node.md)
6. Use [Workloads Overview](../workloads/00-workloads-overview.md) for domain examples
7. Use [SQL Command Catalog](../SQL/08-command-catalog.md) for parser-aligned SQL reference
