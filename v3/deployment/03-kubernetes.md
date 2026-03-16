# Kubernetes Deployment Principles

This repository does not ship a full Helm chart in `docs/v3`, but the following principles are MonkDB-specific and production-safe.

## Workload type

Use `StatefulSet` for MonkDB nodes.

- Stable identity per pod.
- Persistent volume per pod.
- Ordered rollout control.

## Config and flags

You can configure MonkDB through:

- `monkdb.yml` mounted via ConfigMap.
- CLI flags (`-Ckey=value`) in container args.
- Environment variables for selected runtime values (`MONKDB_HEAP_SIZE`, etc.).

Example args pattern:

```yaml
args:
  - -Ccluster.name=prod-cluster
  - -Cnode.name=$(POD_NAME)
  - -Cnetwork.host=0.0.0.0
  - -Cdiscovery.seed_hosts=monkdb-0.monkdb,monkdb-1.monkdb,monkdb-2.monkdb
  - -Ccluster.initial_master_nodes=monkdb-0,monkdb-1,monkdb-2
```

## Storage

- Use SSD-backed PVCs for hot data.
- Separate blob/data paths if required by workload economics.
- Define storage classes with predictable latency.

## Scaling rules

- Add nodes gradually.
- Watch shard relocation and query latency during scale events.
- Avoid frequent oscillation in replica/shard topology.

## Security

- Use Kubernetes secrets for credentials and certificates.
- Restrict service exposure with NetworkPolicies/Ingress rules.
- Prefer mTLS/TLS end-to-end in production.
