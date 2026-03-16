# Logical Replication

MonkDB supports publication/subscription style logical replication between clusters.

## Key operations

- `CREATE PUBLICATION`
- `CREATE SUBSCRIPTION`
- `ALTER PUBLICATION`
- `ALTER SUBSCRIPTION`
- `DROP PUBLICATION`
- `DROP SUBSCRIPTION`

## Use cases

- Cross-cluster reporting consolidation.
- Geo-distributed read replicas.
- Staged cutovers between source and target clusters.

## Basic flow

1. Create publication on source cluster.
2. Create subscription on target cluster with connection info and publication set.
3. Validate lag/state in system metadata.
