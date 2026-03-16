# DROP SNAPSHOT

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | Replication and Backup |
| Mutates Data | Yes/Depends |
| Scope | Cluster / Object |
| Privilege Model | Requires administrative privilege on replication and backup objects. |

## Purpose

Defines, changes, or removes schema and metadata objects.

## Syntax

```sql
DROP SNAPSHOT repository_name.snapshot_name
```

## Operational Notes

- Use schema-qualified identifiers in automation and automation pipelines.
- Validate behavior in staging for cluster-impacting or governance-impacting changes.
- Confirm runtime effects through system tables and metrics before and after execution.

## When to Use

- Use for snapshot lifecycle, repository operations, and logical replication setup.
- Use as part of disaster recovery and data mobility runbooks.

## When Not to Use

- Avoid assuming restore/snapshot compatibility across untested version boundaries.

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
The `DROP SNAPSHOT` statement in MonkDB is used to delete an existing snapshot and all files that are exclusively referenced by this snapshot. This operation is crucial for managing database backups and snapshots efficiently.

## SQL Statement

```sql
DROP SNAPSHOT repository_name.snapshot_name
```

## Description

- **Purpose**: The primary purpose of `DROP SNAPSHOT` is to remove a snapshot from a specified repository. This operation also deletes any files that are only referenced by the snapshot being dropped.
- **Impact on Ongoing Snapshots**: If a snapshot is currently being created when the `DROP SNAPSHOT` statement is executed, the creation process is aborted. All files created during the snapshot creation process up to that point are deleted.

## Parameters
- **repository_name**: This is the name of the repository where the snapshot is stored. It is specified as an identifier.
- **snapshot_name**: This is the name of the snapshot to be dropped. It is also specified as an identifier.

## Example

To drop a snapshot named `my_snapshot` stored in a repository named `my_repository`, you would use the following SQL command

```sql
DROP SNAPSHOT my_repository.my_snapshot;
```

## Best Practices
- **Regular Cleanup**: Regularly dropping old snapshots helps manage storage space and ensures that only relevant backups are retained.
- **Automation**: Consider automating the process of dropping snapshots using workflows or scripts to maintain a consistent backup policy.

## Additional Considerations
- **Incremental Snapshots**: MonkDB supports incremental snapshots, meaning that each new snapshot only includes data that has changed since the last snapshot. This approach helps reduce storage requirements and improve efficiency.
- **Repository Management**: Ensure that the repository name and snapshot name are correctly specified to avoid errors during the drop operation.

---

## See Also

- [Create a Snapshot](./33_CREATE_SNAPSHOT.md)

