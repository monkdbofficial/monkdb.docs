# Configuration and Settings

## Configuration sources

MonkDB reads settings from:

1. `monkdb.yml`
2. CLI flags (`-Ckey=value`)
3. Environment variables (selected runtime knobs)

Typical precedence is runtime flag over static file.

## Example file (`monkdb.yml`)

```yaml
network.host: _local_,_site_
path:
  logs: /data/log
  data: /data/data
blobs:
  path: /data/blobs
```

## Repository file locations

- Primary source template: `config/monkdb.yml`
- Distribution config: `app/src/main/dist/config/monkdb.yml`
- App config copy: `app/config/monkdb.yml`
- Automation template: `automation_scripts/ansible/templates/monkdb.yml.j2`

## Common runtime flags

Examples used in this repository:

- `-Ccluster.name=...`
- `-Cnetwork.host=0.0.0.0`
- `-Cnetwork.publish_host=...`
- `-Ctransport.port=4300`
- `-Cnode.name=...`
- `-Cdiscovery.seed_hosts=...`
- `-Ccluster.initial_master_nodes=...`

## Node-level settings (examples)

- `path.data`, `path.logs`, `blobs.path`
- network/transport/http bind and publish addresses
- local JVM and heap sizing via env vars

## Cluster-level dynamic settings (examples)

- Governance and lineage feature flags (`governance.enabled`, `lineage.*`, `audit.*`)
- FDW local access gate (`fdw.allow_local`)
- breaker tuning (`indices.breaker.*`)

## Logging

Inspect and tune logger levels via cluster settings exposed in `sys.cluster['settings']['logger']`.
