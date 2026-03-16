# SQL Command Catalog

This catalog maps supported SQL statements into operational groups.

Companion per-command pages:

- [SQL Commands (Individual Pages)](./commands/README.md)

## Query and expression statements

- `SELECT`
- `VALUES`
- `WITH`
- `EXPLAIN`

## Transaction/session statements

- `BEGIN`
- `START TRANSACTION`
- `COMMIT`
- `END`
- `SET TRANSACTION`
- `SET SESSION AUTHORIZATION`
- `RESET SESSION AUTHORIZATION`
- `SHOW TRANSACTION ISOLATION LEVEL`

## Data modification and movement

- `INSERT`
- `UPDATE`
- `DELETE`
- `COPY FROM`
- `COPY TO`

## Core schema and object DDL

- `CREATE TABLE`
- `CREATE TABLE AS`
- `ALTER TABLE`
- `DROP TABLE`
- `CREATE VIEW`
- `DROP VIEW`
- `CREATE FUNCTION`
- `DROP FUNCTION`
- `CREATE ANALYZER`
- `DROP ANALYZER`
- `CREATE BLOB TABLE`
- `ALTER BLOB TABLE`
- `DROP BLOB TABLE`

## Security and role management

- `CREATE USER` / `CREATE ROLE`
- `ALTER USER` / `ALTER ROLE`
- `DROP USER` / `DROP ROLE`
- `GRANT`
- `REVOKE`
- `DENY`

## Replication and backup objects

- `CREATE PUBLICATION`
- `ALTER PUBLICATION`
- `DROP PUBLICATION`
- `CREATE SUBSCRIPTION`
- `ALTER SUBSCRIPTION`
- `DROP SUBSCRIPTION`
- `CREATE REPOSITORY`
- `DROP REPOSITORY`
- `CREATE SNAPSHOT`
- `RESTORE SNAPSHOT`
- `DROP SNAPSHOT`

## Cluster/runtime administration

- `ALTER CLUSTER ...`
- `OPTIMIZE TABLE`
- `REFRESH TABLE`
- `ANALYZE`
- `KILL`
- `SET GLOBAL`
- `RESET GLOBAL`
- `SET` / `SHOW`
- `DEALLOCATE`
- `DECLARE`, `FETCH`, `CLOSE`
- `DISCARD`

## FDW statements

- `CREATE SERVER`
- `ALTER SERVER`
- `DROP SERVER`
- `CREATE FOREIGN TABLE`
- `DROP FOREIGN TABLE`
- `CREATE USER MAPPING`
- `DROP USER MAPPING`

## Graph statements

- `CREATE GRAPH`
- `ALTER GRAPH`
- `DROP GRAPH`
- `CREATE VERTEX TABLE`
- `ALTER VERTEX TABLE`
- `DROP VERTEX TABLE`
- `CREATE EDGE TABLE`
- `ALTER EDGE TABLE`
- `DROP EDGE TABLE`

## Memory statements

- `CREATE MEMORY`
- `ALTER MEMORY ... SET (...)`
- `ALTER MEMORY ... COMPACT`
- `DROP MEMORY`

## Governance statements

- `CREATE CONTRACT`
- `ALTER CONTRACT ... SET (...)`
- `ALTER CONTRACT ... BIND TO TABLE ...`
- `ALTER CONTRACT ... UNBIND`
- `DROP CONTRACT`
- `CREATE POLICY`
- `ALTER POLICY ... SET (...)`
- `ALTER POLICY ... BIND TO TABLE ...`
- `DROP POLICY`
- `VALIDATE TABLE`

## Licensing statement

- `SET LICENSE KEY '<token>'`

## Canonical syntax snippets for newer families

### Graph

```sql
CREATE GRAPH [IF NOT EXISTS] graph_name [WITH (...)]
ALTER GRAPH [IF EXISTS] graph_name [WITH (...)]
DROP GRAPH [IF EXISTS] graph_name
```

### Memory

```sql
CREATE MEMORY [IF NOT EXISTS] memory_name WITH (...)
ALTER MEMORY [IF EXISTS] memory_name SET (...)
ALTER MEMORY [IF EXISTS] memory_name COMPACT
DROP MEMORY [IF EXISTS] memory_name
```

### Governance

```sql
CREATE CONTRACT [IF NOT EXISTS] contract_name FOR TABLE schema.table [COLUMN col] WITH (...)
ALTER CONTRACT [IF EXISTS] contract_name SET (...)
ALTER CONTRACT [IF EXISTS] contract_name BIND TO TABLE schema.table [COLUMN col]
ALTER CONTRACT [IF EXISTS] contract_name UNBIND
DROP CONTRACT [IF EXISTS] contract_name

CREATE POLICY [IF NOT EXISTS] policy_name FOR TABLE schema.table [COLUMN col] WITH (...)
ALTER POLICY [IF EXISTS] policy_name SET (...)
ALTER POLICY [IF EXISTS] policy_name BIND TO TABLE schema.table [COLUMN col]
DROP POLICY [IF EXISTS] policy_name
```

### License

```sql
SET LICENSE KEY 'MONK1....'
```

For parser-authoritative behavior, treat `SqlBaseParser.g4` as source of truth and this page as curated operational reference.
