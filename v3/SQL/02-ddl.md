# DDL

## Core table DDL

```sql
CREATE TABLE doc.t (
  id TEXT PRIMARY KEY,
  value DOUBLE PRECISION
);

ALTER TABLE doc.t SET (number_of_replicas = '1');
DROP TABLE IF EXISTS doc.t;
```

## Graph DDL

```sql
CREATE GRAPH social;

CREATE TABLE doc.users (
  id TEXT PRIMARY KEY,
  name TEXT
);

CREATE TABLE doc.follows (
  src_id TEXT,
  dst_id TEXT,
  PRIMARY KEY (src_id, dst_id)
);

CREATE VERTEX TABLE doc.users FOR GRAPH social KEY id;
CREATE EDGE TABLE doc.follows FOR GRAPH social SOURCE KEY src_id TARGET KEY dst_id;
```

## Memory DDL

```sql
CREATE MEMORY session_store
WITH (strict = true, entry_ttl_ms = 3600000, max_entries = 1000);

ALTER MEMORY session_store SET (entry_ttl_ms = 7200000);
ALTER MEMORY session_store COMPACT;

DROP MEMORY session_store;
```

## Governance DDL

```sql
CREATE CONTRACT users_email_format
FOR TABLE doc.users column email
WITH (version = 1, severity = 'high', expression = 'email like ''%@%''', mode = 'warn');

CREATE POLICY users_rf_policy
FOR TABLE doc.users
WITH (scope = 'row_filter', principal = '*', predicate = 'tenant_id = 42', precedence = 100);

ALTER CONTRACT users_email_format SET (mode = 'enforce', version = 2);
ALTER POLICY users_rf_policy SET (precedence = 200);

VALIDATE TABLE doc.users;
```

## FDW DDL

```sql
CREATE SERVER ext_pg
  FOREIGN DATA WRAPPER jdbc
  OPTIONS (url 'jdbc:postgresql://db:5432/app');

CREATE USER MAPPING FOR monkdb
  SERVER ext_pg
  OPTIONS (user 'app', password 'secret');

CREATE FOREIGN TABLE doc.remote_orders (
  id INT,
  total DOUBLE PRECISION
)
SERVER ext_pg
OPTIONS (schema_name 'public', table_name 'orders');
```

## FLOAT_VECTOR type options

`FLOAT_VECTOR` supports a type-level `WITH` option on column definition:

```sql
CREATE TABLE doc.embeddings (
  id TEXT PRIMARY KEY,
  embedding FLOAT_VECTOR(768) WITH (similarity = 'cosine')
);
```

Supported values:

- `euclidean` (default)
- `cosine`
- `dot_product`
- `maximum_inner_product` (aliases include `mips`, `max_inner_product`)

Any unsupported `WITH` option on `FLOAT_VECTOR` is rejected at analyze time.
