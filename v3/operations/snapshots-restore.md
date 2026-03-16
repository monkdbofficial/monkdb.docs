# Snapshots and Restore

Snapshots are the core backup primitive for cluster data recovery.

## Inspect repositories and snapshots

```sql
SELECT * FROM sys.repositories;
SELECT * FROM sys.snapshots ORDER BY started DESC LIMIT 20;
```

## Create repository and snapshot

```sql
CREATE REPOSITORY fs_repo TYPE fs WITH (location = '/data/backups/monkdb');
CREATE SNAPSHOT fs_repo.snap_2026_03_14 ALL;
```

## Restore

```sql
RESTORE SNAPSHOT fs_repo.snap_2026_03_14 ALL;
```

Use table-targeted restores for selective recovery where possible.
