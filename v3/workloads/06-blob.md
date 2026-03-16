# BLOB Workloads

Use BLOB tables for binary payload storage and retrieval via HTTP endpoints.

## Create BLOB table

```sql
CREATE BLOB TABLE media
CLUSTERED INTO 3 SHARDS;
```

## Upload / download / delete

MonkDB BLOBs are addressed by SHA-1 hash of content.

```bash
# upload
curl -X PUT "http://localhost:4200/_blobs/media/<SHA1>" --data-binary @sample.pdf

# download
curl -X GET "http://localhost:4200/_blobs/media/<SHA1>" -o downloaded.pdf

# delete
curl -X DELETE "http://localhost:4200/_blobs/media/<SHA1>"
```

## Production pattern: metadata table

BLOB tables do not provide rich SQL metadata browsing by default. Keep a relational metadata table:

```sql
CREATE TABLE IF NOT EXISTS doc.blob_metadata (
  file_id TEXT PRIMARY KEY,
  blob_sha1 TEXT,
  logical_path TEXT,
  content_type TEXT,
  uploaded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);
```

This enables list/filter/audit queries without scanning binary payload storage.

## Operational caveats

- Treat BLOB endpoint auth and TLS as mandatory in non-local environments.
- Use snapshot/backup strategy appropriate to your BLOB durability requirements.
- Prefer external object store integration when advanced object lifecycle/versioning is required.

