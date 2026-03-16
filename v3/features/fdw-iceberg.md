# FDW: Apache Iceberg

<div class="feature-tags"><span class="gh-label gh-label-release">25.12.1</span><span class="gh-label">FDW</span><span class="gh-label">Iceberg</span></div>

MonkDB supports read-only Iceberg FDW for catalog-backed table access.

## Capabilities

- Read Iceberg tables via SQL foreign tables.
- Projection pushdown.
- Filter pushdown for simple predicates.
- Time travel via `snapshot_id` or `as_of_timestamp`.
- Optional server connection validation (`validate_connection`).

## Supported catalogs

- `hadoop`
- `hive`
- `rest`
- `nessie`

## Important JDK 23 note

Hadoop/Hive catalogs are not supported on JDK 23+ due to Hadoop dependency on `Subject.getSubject`.

Use one of:

- JDK 17 or JDK 21
- REST/Nessie catalogs on JDK 23+

## Options

### Mandatory server options

- `catalog`
- `warehouse`

### Optional server options

- `uri`, `metastore_uri`
- `nessie_ref`, `nessie_ref_type`
- `io_impl`, `validate_connection`
- auth/identity: `token`, `oauth2_token`, `user`, `password`
- cloud creds: `aws.access_key`, `aws.secret_key`, `aws.session_token`, `aws.region`, `aws.s3.endpoint`, `aws.s3.path_style_access`, `gcs.credentials_file`

### Optional foreign table options

- `schema_name`
- `namespace`
- `table_name`
- `snapshot_id`
- `as_of_timestamp`

Only one of `snapshot_id` or `as_of_timestamp` may be set.

## Example: REST catalog

```sql
CREATE SERVER ice_rest
  FOREIGN DATA WRAPPER iceberg
  OPTIONS (
    catalog 'rest',
    uri 'https://iceberg-catalog:8181',
    warehouse '/data/iceberg',
    token 'YOUR_JWT_TOKEN'
  );

CREATE FOREIGN TABLE doc.ice_orders (
  order_id INT,
  customer TEXT,
  total DOUBLE
)
SERVER ice_rest
OPTIONS (table_name 'db.orders');

SELECT order_id, total
FROM doc.ice_orders
WHERE order_id > 100
LIMIT 10;
```

## Example: Nessie catalog

```sql
CREATE SERVER ice_nessie
  FOREIGN DATA WRAPPER iceberg
  OPTIONS (
    catalog 'nessie',
    uri 'http://nessie:19120/api/v1',
    warehouse '/data/iceberg',
    nessie_ref 'main',
    nessie_ref_type 'BRANCH',
    token 'YOUR_NESSIE_TOKEN'
  );
```

## Time-travel example

```sql
CREATE FOREIGN TABLE doc.ice_orders_snap (
  order_id INT,
  customer TEXT,
  total DOUBLE
)
SERVER ice_rest
OPTIONS (
  table_name 'db.orders',
  snapshot_id '123456789'
);
```

## Pushdown limitations (current)

Pushdown currently supports simple expression translation:

- comparisons (`=`, `>`, `>=`, `<`, `<=`)
- `AND`, `OR`, `NOT`
- `IS NULL`

Joins, aggregations, and complex expressions are executed in MonkDB.

## Local filesystem gate

Local file access is restricted for non-superusers unless:

```sql
SET GLOBAL TRANSIENT fdw.allow_local = true;
```

## Current limitations and support notes

- FDW path is read-only (no remote writes/DDL).
- Simple pushdowns only (scan-level filter + projection + time travel).
- Iceberg is a table format, not a remote query engine; join/aggregation pushdown is not available.
- JDK 23+: Hadoop/Hive catalogs fail fast by design.

Support notes from current implementation scope:

- REST catalog + S3: not a validated support path yet.
- Nessie catalog + S3: not a validated support path yet.
- Hadoop/Hive on JDK 23+: blocked.

Implementation note:

- S3 credential mapping currently follows existing integration paths; review before production rollout if your environment depends on mixed AWS SDK major versions.

## GCS credentials scope

`gcs.credentials_file` is a server/user mapping option, not a global YAML setting.

Example:

```sql
CREATE SERVER ice_rest_gcs
  FOREIGN DATA WRAPPER iceberg
  OPTIONS (
    catalog 'rest',
    uri 'https://iceberg-catalog:8181',
    warehouse 'gs://bucket/warehouse',
    gcs.credentials_file '/etc/gcp/sa.json'
  );
```
