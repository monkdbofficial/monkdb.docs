# FDW: JDBC

<div class="feature-tags"><span class="gh-label">FDW</span><span class="gh-label">JDBC</span></div>

MonkDB supports `jdbc` as a built-in foreign data wrapper.

## What it enables

- Read access to remote JDBC tables through SQL.
- Projection and predicate pushdown for safe predicates.

## Server/table/user mapping options

### `CREATE SERVER ... FOREIGN DATA WRAPPER jdbc`

Mandatory server option:

- `url`

### `CREATE FOREIGN TABLE ... OPTIONS (...)`

Optional table options:

- `schema_name`
- `table_name`

### `CREATE USER MAPPING ... OPTIONS (...)`

Optional user options:

- `user`
- `password`

## Example

```sql
CREATE SERVER ext_pg
  FOREIGN DATA WRAPPER jdbc
  OPTIONS (url 'jdbc:postgresql://postgres:5432/appdb');

CREATE USER MAPPING FOR monkdb
  SERVER ext_pg
  OPTIONS (user 'app', password 'secret');

CREATE FOREIGN TABLE doc.remote_orders (
  id INT,
  customer TEXT,
  total DOUBLE PRECISION
)
SERVER ext_pg
OPTIONS (schema_name 'public', table_name 'orders');

SELECT id, total
FROM doc.remote_orders
WHERE total > 100
ORDER BY total DESC
LIMIT 10;
```

## Localhost safety gate

Non-superusers cannot access localhost JDBC endpoints unless cluster setting is enabled:

```sql
SET GLOBAL TRANSIENT fdw.allow_local = true;
```

Use carefully in production.
