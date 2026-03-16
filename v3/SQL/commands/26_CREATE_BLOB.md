# CREATE BLOB

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | DDL and Administration |
| Mutates Data | Yes/Depends |
| Scope | Cluster / Object |
| Privilege Model | Requires DDL/administrative privilege according to target object scope. |

## Purpose

Defines, changes, or removes schema and metadata objects.

## Syntax

```sql
CREATE BLOB TABLE table_name
[CLUSTERED INTO num_shards SHARDS]
[ WITH ( storage_parameter [= value] [, ... ] ) ]
```

## Operational Notes

- Use schema-qualified identifiers in automation and automation pipelines.
- Validate behavior in staging for cluster-impacting or governance-impacting changes.
- Confirm runtime effects through system tables and metrics before and after execution.

## When to Use

- Use during planned schema and runtime administration changes.
- Use in automation pipelines with environment-specific validation and rollback strategy.

## When Not to Use

- Avoid during incident windows unless the command is part of approved mitigation.
- Avoid schema changes in peak traffic windows without staged rollout.

## Common Errors and Troubleshooting

| Symptom | Likely Cause | Action |
| --- | --- | --- |
| Permission denied / unauthorized | Missing privilege on object or cluster scope | Re-run with required grants or elevated admin role. |
| Analysis/parse error | Syntax variant or object shape mismatch | Compare with canonical syntax and object definition. |
| Runtime failure under load | Resource limits, breaker pressure, or node state transitions | Check `sys.jobs`, `sys.operations`, `sys.checks`, and retry after mitigation. |

## Cross-References

- [SQL Command Catalog](../08-command-catalog.md)
- [SQL Commands Index](./README.md)
- [SQL Reference Overview](../01-sql-reference.md)

## Detailed Reference
Creates a new table for storing Binary Large Objects (BLOBs) in monkdb.

---

## SQL Statement

```sql
CREATE BLOB TABLE table_name
[CLUSTERED INTO num_shards SHARDS]
[ WITH ( storage_parameter [= value] [, ... ] ) ]
```

---

## Description

The `CREATE BLOB TABLE` statement creates a dedicated table for storing unstructured binary data (BLOBs). These tables are automatically sharded based on the BLOB's digest (hash) for efficient distribution across nodes.

---

## Clauses

### **CLUSTERED**
Specifies the sharding configuration for the BLOB table:

```sql
CLUSTERED INTO num_shards SHARDS
```
- **num_shards**:
  - *Type:* integer > 0
  - Defines how many shards the BLOB table will be split into.
  - BLOB tables are always sharded by their digest (hash value), not by user-defined columns.

### **WITH**
Configures storage parameters for the BLOB table:
```sql
WITH (
    blobs_path = 'path/to/directory',
    number_of_replicas = value
)
```
### Supported parameters:

| Parameter              | Type     | Default      | Description                                                                 |
|------------------------|----------|--------------|-----------------------------------------------------------------------------|
| **blobs_path**         | text     | Global config | Custom path for BLOB storage (absolute or relative to `MONKDB_HOME`).       |
| **number_of_replicas** | integer  | 1            | Number of replicas per shard. Set to `0` to disable replication.           |

---

## Key Parameters

### **blobs_path**
- Overrides the global BLOB storage path for this table
- Must be writable by the monkdb system user
- Example paths:
  - Absolute: `/mnt/monkdb_blobs/cust_table_data`
  - Relative: `custom_blobs` (resolves to `MONKDB_HOME/custom_blobs`)

---

## Examples

### Basic BLOB Table
Create a BLOB table with 3 shards and default settings:
```sql
CREATE BLOB TABLE my_images
CLUSTERED INTO 3 SHARDS;
```

### Custom Storage Path
Create a BLOB table with dedicated storage location:
```sql
CREATE BLOB TABLE audit_logs
CLUSTERED INTO 5 SHARDS
WITH (
    blobs_path = '/var/lib/monkdb/secure_blobs',
    number_of_replicas = 0
);
```

---

## Additional Operations

### Modify Replica Count
```sql
ALTER BLOB TABLE my_images SET (number_of_replicas = 1);
```

### Delete BLOB Table
```sql
DROP BLOB TABLE my_images;
```

---

##  Notes
1. **Shard Allocation**: BLOBs are automatically distributed based on their SHA-1 digest
2. **Access Control**: Use the `blob` schema prefix for queries (e.g., `SELECT * FROM blob.my_images`)
3. **Backup Limitation**: BLOB tables cannot be backed up via monkdb's snapshot/restore functionality
4. **Path Priority**: Table-specific `blobs_path` overrides global configuration
5. **Security**: Ensure filesystem permissions match monkdb's runtime user

##  Permissions

- **DDL Rights**: The user must have `CREATE` privileges in the database to define new `BLOB` tables.
- **Filesystem Access**: The MonkDB process must have write permissions on the directory specified in `blobs_path` (if used).
- **`DROP/ALTER` Access**: Only the creator or a superuser can alter or drop the `BLOB` table.

##  Summary

| Feature                          | Supported / Behavior                              |
|----------------------------------|--------------------------------------------------|
| Stores Binary Data               | Yes Yes (BLOBs only)                              |
| Digest-Based Sharding            | Yes Automatic using **SHA-1**                        |
| Custom Storage Path              | Yes via `blobs_path`                                 |
| Replication                      | Yes Configurable via `number_of_replicas`           |
| Column Definitions                | No Not supported (binary content only)           |
| Accessible via blob schema       | Yes Yes                                           |
| Included in Backups              | No No                                            |
| Requires CREATE Privilege        | Yes Yes                                           |
| Per-Table Storage Path Isolation  | Yes Optional via `WITH (blobs_path = ...)`          |

