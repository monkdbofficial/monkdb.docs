# License Provisioning for Larger Clusters

This guide demonstrates staged license provisioning for a multi-node cluster.

For enterprise/commercial licensing, contact: `hello@monkdb.com`.

## 1) Clean and initialize 3-node lab

```bash
docker compose -f docker-compose.3node.yml down -v --remove-orphans
docker rm -f monkdb001 monkdb002 monkdb003 2>/dev/null || true
docker volume rm monkdb_monkdb001-data monkdb_monkdb002-data monkdb_monkdb003-data 2>/dev/null || true
```

Start first two nodes together:

```bash
docker compose -f docker-compose.3node.yml up -d monkdb001 monkdb002
```

## 2) Verify from both ports

```bash
psql -h 127.0.0.1 -p 5432 -U monkdb -d monkdb -c "select id, master_node from sys.cluster;"
psql -h 127.0.0.1 -p 5433 -U monkdb -d monkdb -c "select id, master_node from sys.cluster;"
```

## 3) Validate cluster and nodes before license

```sql
-- a) master node
select id, master_node from sys.cluster;

-- b) node inventory
select id, name from sys.nodes order by name;
```

Expected before license (2 nodes):

```text
select id, name from sys.nodes order by name;
             id           |   name
--------------------------+-----------
 STWGKEWIQEmUaMEdlVltuA   | monkdb001
 GyCvzQ8MTWm1mGxfcA779Q   | monkdb002
(2 rows)
```

## 4) Apply license key

```sql
SET LICENSE KEY 'MONK1.eyJiaW5kIjp7Im1vZGUiOiJmaXJzdF91c2UifSwiY2hhbm5lbCI6eyJ0eXBlIjoiZGlyZWN0In0sImN1c3QiOnsibG9jIjp7ImNpdHkiOiJVZGFpcHVyIiwiY291bnRyeSI6IklOIiwic3RhdGUiOiJSSiJ9LCJvcmciOiJBY21lIE1pbmluZyBMdGQiLCJvdSI6IlVuZGVyZ3JvdW5kIE9wcyIsInNwb2NfZW1haWwiOiJyYXZpQGFjbWUuY29tIiwic3BvY19uYW1lIjoiUmF2aSBLdW1hciJ9LCJleHAiOiIyMDI3LTAzLTE0VDA0OjUzOjU4WiIsImlhdCI6IjIwMjYtMDMtMTRUMDQ6NTM6NThaIiwiaXNzdWVfaWQiOiJMSUMtVEVTVC0wMDAxIiwia2lkIjoiazEiLCJsaW1pdHMiOnsibWF4X25vZGVzIjo4fSwibmJmIjoiMjAyNi0wMy0xNFQwNDo0ODo1OFoiLCJwcm9kIjoibW9ua2RiIiwic2NvcGUiOnsiaWQiOiJJTlYtVEVTVC0wMDAxIn0sInYiOjF9.05teqlMntLfPDKu9GsEgu9ZEqaxadAe4xxxxxxxxxxxxxxxxxxxxxxxx';
```

Check license status:

```sql
select "license"['status'],
       "license"['valid'],
       "license"['allowed_nodes'],
       "license"['current_nodes'],
       "license"['error']
from sys.cluster;
```

Expected before adding third node:

```text
license['status'] | license['valid'] | license['allowed_nodes'] | license['current_nodes'] | license['error']
------------------+------------------+--------------------------+--------------------------+------------------
normal            | t                |                        8 |                        2 |
```

## 5) Add third node and re-validate

```bash
docker compose -f docker-compose.3node.yml up -d monkdb003
```

```sql
select id, name from sys.nodes order by name;
```

Expected after node addition:

```text
             id           |   name
--------------------------+-----------
 STWGKEWIQEmUaMEdlVltuA   | monkdb001
 GyCvzQ8MTWm1mGxfcA779Q   | monkdb002
 lS5DpegDTcKzfZNCONxhlQ   | monkdb003
(3 rows)
```

Check updated license counters:

```sql
select "license"['status'],
       "license"['valid'],
       "license"['allowed_nodes'],
       "license"['current_nodes'],
       "license"['error']
from sys.cluster;
```

Expected after third node joins:

```text
license['status'] | license['valid'] | license['allowed_nodes'] | license['current_nodes'] | license['error']
------------------+------------------+--------------------------+--------------------------+------------------
normal            | t                |                        8 |                        3 |
```

## 6) Operational checks

- Ensure `current_nodes <= allowed_nodes`.
- Monitor `license['error']` for enforcement warnings.
- Re-run checks from every service endpoint/port after scaling events.
