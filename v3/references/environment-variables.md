# Environment Variables and Runtime Flags

## Common environment variables

Examples used in local cluster compose:

- `MONKDB_HEAP_SIZE=1g`
- `MONKDB_INDICES_FIELDDATA_BREAKER_LIMIT=60%`

Use env vars for containerized runtime defaults and operational overrides.

## Common `-C` runtime flags

Examples:

- `-Ccluster.name=...`
- `-Cnetwork.host=...`
- `-Cnetwork.publish_host=...`
- `-Ctransport.port=...`
- `-Cnode.name=...`
- `-Cdiscovery.seed_hosts=...`
- `-Ccluster.initial_master_nodes=...`

## Configuration file location

Typical file: `monkdb.yml`

Example baseline in this repo:

```yaml
network.host: _local_,_site_
path:
  logs: /data/log
  data: /data/data
blobs:
  path: /data/blobs
```

## Where to set what

- Use `monkdb.yml` for stable node baseline.
- Use `-C` flags for deployment-time topology wiring.
- Use environment variables for container/JVM operational values.
