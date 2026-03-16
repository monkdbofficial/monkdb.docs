# Quickstart

This quickstart starts a local multi-node MonkDB environment, connects over PGWire, and runs basic SQL.

## 1) Start the cluster

Use the repository's `docker-compose.3node.yml`.

```bash
docker network create monkdb || true
docker compose -f docker-compose.3node.yml up -d monkdb001 monkdb002 monkdb003
```

## 2) Verify cluster membership

```bash
psql -h 127.0.0.1 -p 5432 -U monkdb -d monkdb -c "select id, master_node from sys.cluster;"
psql -h 127.0.0.1 -p 5432 -U monkdb -d monkdb -c "select id, name from sys.nodes order by name;"
```

## 3) Create and query a table

```sql
CREATE TABLE IF NOT EXISTS doc.quickstart_users (
  id TEXT PRIMARY KEY,
  name TEXT,
  created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO doc.quickstart_users (id, name)
VALUES ('u1', 'Alice'), ('u2', 'Bob');

REFRESH TABLE doc.quickstart_users;

SELECT * FROM doc.quickstart_users ORDER BY id;
```

## 4) Verify SQL + system schemas

```sql
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema IN ('doc', 'sys', 'information_schema')
ORDER BY table_schema, table_name
LIMIT 50;
```

## 5) Stop and clean up

```bash
docker compose -f docker-compose.3node.yml down
```

If you need to remove volumes too:

```bash
docker compose -f docker-compose.3node.yml down -v --remove-orphans
```
