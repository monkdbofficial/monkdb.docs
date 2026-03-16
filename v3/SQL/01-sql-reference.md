# SQL Reference Overview

MonkDB exposes a PostgreSQL-compatible SQL surface with MonkDB-specific extensions.

## Command families

- DDL: schemas, tables, graph/memory/governance objects, FDW objects.
- DML: `INSERT`, `UPDATE`, `DELETE`, `COPY FROM`.
- DQL: `SELECT`, CTEs, joins, aggregations, window functions, search/vector/geospatial predicates.
- Administrative SQL: `SET GLOBAL`, cluster reroute, snapshots, license key.

## Platform SQL extensions

- Graph DDL: `CREATE/ALTER/DROP GRAPH`, `CREATE/DROP VERTEX TABLE`, `CREATE/DROP EDGE TABLE`.
- Memory DDL: `CREATE/ALTER/DROP MEMORY`, `ALTER MEMORY ... COMPACT`.
- Governance DDL: `CREATE/ALTER/DROP CONTRACT`, `CREATE/ALTER/DROP POLICY`, `VALIDATE TABLE`.
- FDW SQL: `CREATE SERVER`, `CREATE USER MAPPING`, `CREATE FOREIGN TABLE`.
- Licensing SQL: `SET LICENSE KEY '...';`.

## Compatibility notes

- MonkDB is distributed and not a classic single-node OLTP engine.
- Some PostgreSQL features are accepted for compatibility but may have different semantics.

## Deep dives

- [SQL Commands (Individual Pages)](./commands/README.md)
- [SQL Constraints](./10_monkdb_sql_constraints.md)
- [SQL Value Expressions](./11_monkdb_value_expressions.md)
