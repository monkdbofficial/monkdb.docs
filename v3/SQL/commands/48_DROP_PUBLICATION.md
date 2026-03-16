# DROP PUBLICATION

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
DROP PUBLICATION [ IF EXISTS ] name;
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
The `DROP PUBLICATION` command in MonkDB is used to remove an existing publication from the cluster. This operation stops replication for all subscriptions associated with the publication.

## SQL Statement

```sql
DROP PUBLICATION [ IF EXISTS ] name;
```

## Description

The command deletes a publication, effectively stopping replication for all tables included in the publication. On the subscriber cluster, tables that were replicated via this publication will revert to regular writable tables after the publication is dropped.

## Parameters

- **name**- Specifies the name of the publication to be removed.
- **IF EXISTS**- Optional clause that prevents an error if the specified publication does not exist. Instead, a notice is issued.

## Behavior

- Dropping a publication does not delete the replicated tables on the subscriber cluster; these tables remain intact but lose their replication properties.
- This ensures that data integrity is maintained on the subscriber side while allowing further modifications.

## Examples

### Example 1. Drop a publication

To drop a publication named `my_publication`

```sql
DROP PUBLICATION my_publication;
```

### Example 2. Using IF EXISTS to avoid errors if the publication does not exist

```sql
DROP PUBLICATION IF EXISTS my_publication;
```

## Notes

- Ensure that all subscriptions tied to the publication are properly managed before dropping it to avoid unexpected replication issues.
- After dropping a publication, any changes made to tables on the publishing cluster will no longer propagate to subscribers.
- This command is particularly useful for managing replication setups and cleaning up unused publications in MonkDB environments.

---

## See Also

- [Create publication](./29_CREATE_PUBLICATION.md)
