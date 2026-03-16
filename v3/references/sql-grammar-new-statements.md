# SQL Grammar: New Statement Families

This page captures the key statement surface visible in current SQL grammar.

## New/extended statement families

- `VALIDATE TABLE <table>`
- `SET LICENSE KEY '<token>'`

### Graph

- `CREATE GRAPH [IF NOT EXISTS] <name> [WITH (...)]`
- `ALTER GRAPH [IF EXISTS] <name> [WITH (...)]`
- `DROP GRAPH [IF EXISTS] <name>`
- `CREATE VERTEX TABLE ... FOR GRAPH ... KEY ...`
- `CREATE EDGE TABLE ... FOR GRAPH ... SOURCE KEY ... TARGET KEY ...`

### Memory

- `CREATE MEMORY [IF NOT EXISTS] <name> WITH (...)`
- `ALTER MEMORY [IF EXISTS] <name> WITH (...)`
- `ALTER MEMORY [IF EXISTS] <name> COMPACT`
- `DROP MEMORY [IF EXISTS] <name>`

### Contracts and policies

- `CREATE CONTRACT [IF NOT EXISTS] ... FOR TABLE ... [COLUMN ...] WITH (...)`
- `ALTER CONTRACT [IF EXISTS] ... SET (...)`
- `ALTER CONTRACT [IF EXISTS] ... BIND TO TABLE ... [COLUMN ...]`
- `ALTER CONTRACT [IF EXISTS] ... UNBIND`
- `DROP CONTRACT [IF EXISTS] ...`
- `CREATE POLICY [IF NOT EXISTS] ... FOR TABLE ... [COLUMN ...] WITH (...)`
- `ALTER POLICY [IF EXISTS] ... SET (...)`
- `ALTER POLICY [IF EXISTS] ... BIND TO TABLE ... [COLUMN ...]`
- `DROP POLICY [IF EXISTS] ...`

### FDW

- `CREATE SERVER [IF NOT EXISTS] ... FOREIGN DATA WRAPPER ... OPTIONS (...)`
- `ALTER SERVER ... OPTIONS (...)`
- `DROP SERVER [IF EXISTS] ...`
- `CREATE USER MAPPING [IF NOT EXISTS] FOR <user> SERVER <server> OPTIONS (...)`
- `DROP USER MAPPING [IF EXISTS] FOR <user> SERVER <server>`
- `CREATE FOREIGN TABLE [IF NOT EXISTS] ... SERVER <server> OPTIONS (...)`
- `DROP FOREIGN TABLE [IF EXISTS] ...`
