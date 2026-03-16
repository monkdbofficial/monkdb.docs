# Provisioning with Docker Image

## Spawning MonkDB Container

Create a dedicated network to manage persistence and container communication.

```bash
docker network create monkdb
```

## Pull image

### AMD64

If your system is based on AMD64 chipset processor:

```bash
docker pull rg.fr-par.scw.cloud/monkdb/monkdb:26.3.1-amd64
```

### ARM64

If your system is based on ARM64 chipset processor:

```bash
docker pull rg.fr-par.scw.cloud/monkdb/monkdb:26.3.1-arm64
```

Current stable release in this guide: `26.3.1`.
Update the tag when a newer release is published.

## Verify image

```bash
docker images
```

Example output on AMD64:

```text
IMAGE                                              ID             DISK USAGE   CONTENT SIZE   EXTRA
rg.fr-par.scw.cloud/monkdb/monkdb:26.3.1-amd64   508f75ddee28        878MB             0B
```

Example output on ARM64:

```text
IMAGE                                              ID             DISK USAGE   CONTENT SIZE   EXTRA
rg.fr-par.scw.cloud/monkdb/monkdb:26.3.1-arm64   508f75ddee28        878MB             0B
```

## Run container (sample)

You can tune args and values based on your `monkdb.yml` settings.

```bash
docker run -d \
  --publish=4200:4200 \
  --publish=5432:5432 \
  --env MONKDB_HEAP_SIZE=1g \
  --env MONKDB_INDICES_FIELDDATA_BREAKER_LIMIT=60% \
  --net=monkdb \
  --name=monkdb01 \
  rg.fr-par.scw.cloud/monkdb/monkdb:26.3.1-amd64 \
  -Cnetwork.host=_site_,_local_ \
  -Cnode.name=monkdb01 \
  -Cauth.host_based.config.0.user=monkdb \
  -Cauth.host_based.config.0.address=_local_ \
  -Cauth.host_based.config.0.method=trust \
  -Cauth.host_based.config.99.method=password
```

## What each setting does

- `4200` is the HTTP endpoint for SQL-over-HTTP API clients.
- `5432` is PGWire endpoint for PostgreSQL-compatible clients (`psql`, drivers, BI tools).
- `MONKDB_HEAP_SIZE=1g` configures JVM heap for MonkDB process.
- `--net=monkdb` attaches the container to the dedicated network.
- `--name=...` sets container name for ops automation.
- `-Cnetwork.host=_site_,_local_` binds to site-local and loopback interfaces.
- `-Cnode.name=...` sets stable node identity for clustering/ops.
- `auth.host_based.config.0.*` sets local superuser trust access.
- `auth.host_based.config.99.method=password` enforces password auth for the broader rule set.

## Check container status

```bash
docker ps
```

If output is empty, inspect container logs and fix startup errors.

## `psql` client prerequisite

Install `psql` client before running SQL steps.
Use [System Prerequisites](./02-system-prerequisites.md) for installation commands by OS.

## Creating a normal user in MonkDB

Use a normal user for client access instead of relying on superuser for apps.

```bash
psql -h localhost -p 5432 -U monkdb -d monkdb
```

```sql
CREATE USER testuser WITH (password = 'testpassword');
GRANT ALL PRIVILEGES TO testuser;
```

Replace credentials with your organization standards.

## Full `monkdb.yml` / `monkdb.yaml` configuration

Use the complete configuration page:

- [monkdb.yaml / monkdb.yml (Complete Reference)](./04-monkdb-yaml.md)
