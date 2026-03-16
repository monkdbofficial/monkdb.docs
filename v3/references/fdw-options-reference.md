# FDW Options Reference

## FDW wrappers in MonkDB

Supported built-in wrappers:

- `jdbc`
- `iceberg`

## Cluster gate

Local resource access by non-superusers is gated by:

- `fdw.allow_local` (default `false`)

---

## JDBC wrapper

### `CREATE SERVER ... FOREIGN DATA WRAPPER jdbc`

Mandatory server options:

- `url`

### `CREATE FOREIGN TABLE ... OPTIONS (...)`

Optional table options:

- `schema_name`
- `table_name`

### `CREATE USER MAPPING ... OPTIONS (...)`

Optional user options:

- `user`
- `password`

---

## Iceberg wrapper

### `CREATE SERVER ... FOREIGN DATA WRAPPER iceberg`

Mandatory server options:

- `catalog`
- `warehouse`

Optional server options:

- `uri`
- `metastore_uri`
- `nessie_ref`
- `nessie_ref_type`
- `io_impl`
- `validate_connection`
- `token`
- `oauth2_token`
- `user`
- `password`
- `aws.access_key`
- `aws.secret_key`
- `aws.session_token`
- `aws.region`
- `aws.s3.endpoint`
- `aws.s3.path_style_access`
- `gcs.credentials_file`

Supported `catalog` values:

- `hadoop`
- `hive`
- `rest`
- `nessie`

### `CREATE FOREIGN TABLE ... OPTIONS (...)`

Optional table options:

- `schema_name`
- `namespace`
- `table_name`
- `snapshot_id`
- `as_of_timestamp`

### `CREATE USER MAPPING ... OPTIONS (...)`

Optional user mapping options:

- `token`
- `oauth2_token`
- `user`
- `password`
- `aws.access_key`
- `aws.secret_key`
- `aws.session_token`
- `aws.region`
- `aws.s3.endpoint`
- `aws.s3.path_style_access`
- `gcs.credentials_file`
