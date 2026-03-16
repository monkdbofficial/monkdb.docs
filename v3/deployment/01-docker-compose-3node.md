# Docker Compose (3-node)

This guide maps directly to `docker-compose.3node.yml` in this repository.

## Topology

- `monkdb001`: HTTP `4200`, PGWire `5432`, transport `4300`
- `monkdb002`: HTTP `4201`, PGWire `5433`, transport `4301`

All nodes share cluster name `monkdb-licensing-lab` and join via `discovery.seed_hosts=monkdb001`.

## Start

```bash
docker network create monkdb || true
docker compose -f docker-compose.3node.yml up -d monkdb001 monkdb002
```

`docker-compose.3node.yml` uses an external network named `monkdb`, so `docker network create monkdb` is required before first startup.

## Compose File (Current)

```yaml
services:
  monkdb001:
    image: rg.fr-par.scw.cloud/monkdb/monkdb:26.3.1-amd64
    container_name: monkdb001
    hostname: monkdb001
    environment:
      MONKDB_HEAP_SIZE: 1g
      MONKDB_INDICES_FIELDDATA_BREAKER_LIMIT: 60%
    command:
      - -Ccluster.name=monkdb-licensing-lab
      - -Cnetwork.host=0.0.0.0
      - -Cnetwork.publish_host=monkdb001
      - -Ctransport.port=4300
      - -Cnode.name=monkdb001
      - -Cdiscovery.seed_hosts=monkdb001
      - -Ccluster.initial_master_nodes=monkdb001
      - -Cauth.host_based.config.0.user=monkdb
      - -Cauth.host_based.config.0.address=_local_
      - -Cauth.host_based.config.0.method=trust
      - -Cauth.host_based.config.99.method=password
    ports:
      - "4200:4200"
      - "5432:5432"
      - "4300:4300"
    volumes:
      - monkdb001-data:/data
    networks:
      - monkdb

  monkdb002:
    image: rg.fr-par.scw.cloud/monkdb/monkdb:26.3.1-amd64
    container_name: monkdb002
    hostname: monkdb002
    environment:
      MONKDB_HEAP_SIZE: 1g
      MONKDB_INDICES_FIELDDATA_BREAKER_LIMIT: 60%
    command:
      - -Ccluster.name=monkdb-licensing-lab
      - -Cnetwork.host=0.0.0.0
      - -Cnetwork.publish_host=monkdb002
      - -Ctransport.port=4300
      - -Cnode.name=monkdb002
      - -Cdiscovery.seed_hosts=monkdb001
      - -Ccluster.initial_master_nodes=monkdb001
      - -Cauth.host_based.config.0.user=monkdb
      - -Cauth.host_based.config.0.address=_local_
      - -Cauth.host_based.config.0.method=trust
      - -Cauth.host_based.config.99.method=password
    ports:
      - "4201:4200"
      - "5433:5432"
      - "4301:4300"
    volumes:
      - monkdb002-data:/data
    networks:
      - monkdb

volumes:
  monkdb001-data:
  monkdb002-data:

networks:
  monkdb:
    external: true
    name: monkdb
```

**PS**: If you are trying to use `ARM64` instance to deploy MonkDB image, please pull appropriate MonkDB image for `ARM64` architecture.

## Verify

```bash
psql -h 127.0.0.1 -p 5432 -U monkdb -d monkdb -c "select id, master_node from sys.cluster;"
psql -h 127.0.0.1 -p 5432 -U monkdb -d monkdb -c "select id, name from sys.nodes order by name;"
```

## Stop

```bash
docker compose -f docker-compose.3node.yml down
```

## Reset data volumes

```bash
docker compose -f docker-compose.3node.yml down -v --remove-orphans
docker rm -f monkdb001 monkdb002 monkdb003 2>/dev/null || true
docker volume rm monkdb_monkdb001-data monkdb_monkdb002-data monkdb_monkdb003-data 2>/dev/null || true
```

## For 3+ nodes

A license need to be procured for 3+ nodes of MonkDB provisioning. MonkDB is free for 2 nodes.
