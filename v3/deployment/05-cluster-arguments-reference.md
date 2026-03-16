# Cluster Arguments Reference

This page documents practical cluster and runtime flags used in MonkDB deployments.

## Core runtime flags

- `-Cnode.data=true`
  Node stores shards and serves data-path operations.

- `-Cnetwork.host=_site_,_local_`
  Binds to site-local and loopback interfaces.

- `-Cdiscovery.seed_hosts=node1,node2,...`
  Initial peer list for discovery.

- `-Ccluster.initial_master_nodes=node1,node2,node3`
  Bootstrap setting for first cluster formation/master election.

- `-Cgateway.expected_data_nodes=3`
  Expected data node count used for recovery behavior/checks.

- `-Cgateway.recover_after_data_nodes=2`
  Minimum data nodes before selected recovery actions begin.

## Authentication-related examples

- `-Cauth.host_based.config.0.user=monkdb`
- `-Cauth.host_based.config.0.address=_local_`
- `-Cauth.host_based.config.0.method=trust`
- `-Cauth.host_based.config.99.method=password`

## Recommended usage pattern

1. Use [Docker Compose (3-node)](./01-docker-compose-3node.md) for cluster validation.
2. Start with minimal safe flags, then add environment-specific tuning.
3. Validate health after startup.

```sql
SELECT id, master_node FROM sys.cluster;
SELECT id, name FROM sys.nodes ORDER BY name;
SELECT * FROM sys.checks WHERE NOT passed ORDER BY severity DESC;
```

## Related

- [Production Topologies](./02-production-topologies.md)
- [Kubernetes Deployment Principles](./03-kubernetes.md)
- [Configuration and Settings](./04-configuration.md)
