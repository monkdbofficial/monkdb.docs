# DROP REPOSITORY

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
DROP REPOSITORY repository_name;
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
The `DROP REPOSITORY` statement in MonkDB is used to de-register a repository, making it unavailable for use.

## SQL Statement

```sql
DROP REPOSITORY repository_name;
```

## Description

When you execute the `DROP REPOSITORY` statement, MonkDB removes the repository's configuration from the system, specifically deleting the corresponding record from sys.repositories. However, this action does not affect any existing snapshots stored in the backend data storage associated with the repository. If you create a new repository using the same backend data storage, any existing snapshots will become accessible again.

### Parameters
- **repository_name**: The name of the repository to be de-registered.

## Important Considerations
- **Repository Usage**: A repository can only be dropped if it is not currently in use. This means there should be no ongoing snapshot operations.
- **Snapshot Persistence**: Dropping a repository does not delete the snapshots themselves; it merely removes the repository's configuration. This allows you to reuse the backend storage for a new repository, making existing snapshots available again.
- **Recreating a Repository**: If you need to change repository parameters, you must first drop the repository and then recreate it with the desired settings using the `CREATE REPOSITORY` statement.

## Example

To drop a repository named `OldRepository`, you would use the following command

```sql
DROP REPOSITORY "OldRepository";
```

This command removes the `OldRepository` from the system, but any snapshots it contained remain in the backend storage until manually deleted or reused by a new repository.

---

## See Also

- [Create Repository](./30_CREATE_REPOSITORY.md)

