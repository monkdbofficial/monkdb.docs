# DROP SUBSCRIPTION

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
DROP SUBSCRIPTION [ IF EXISTS ] name
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
## SQL Statement

```sql
DROP SUBSCRIPTION [ IF EXISTS ] name
```

## Description

The `DROP SUBSCRIPTION` command in MonkDB is used to remove an existing subscription from the cluster. Once a subscription is dropped, the replication process for that subscription stops, and any tables associated with it become regular writable tables.

> It is important to note that once a subscription is dropped, it cannot be resumed.

## Parameters

- **name**: This is the name of the subscription that you want to delete. It must be a valid subscription name within the cluster.

## Steps to Drop a Subscription

- **Identify the Subscription**: Ensure you have the correct name of the subscription you wish to drop.
- **Execute the Command**: Use the `DROP SUBSCRIPTION` command followed by the name of the subscription. If you are unsure whether the subscription exists, you can use `IF EXISTS` to avoid errors.

```sql
DROP SUBSCRIPTION IF EXISTS my_subscription;
```

After executing the command, verify that the subscription has been successfully removed and that replication has stopped.

## Considerations
- **Replication Stop**: Dropping a subscription stops the replication process for the tables involved. These tables will no longer receive updates from the publisher.
- **Table Accessibility**: After dropping a subscription, the tables become writable on the subscriber cluster, allowing local modifications.
- **Irreversibility**: Once a subscription is dropped, it cannot be resumed. You would need to recreate the subscription if you want to restart replication.

## Examples

Suppose you have a subscription named `my_subscription` that you no longer need. You can drop it using the following command:

```sql
DROP SUBSCRIPTION my_subscription;
```

If you are unsure whether `my_subscription` exists, use:

```sql
DROP SUBSCRIPTION IF EXISTS my_subscription;
```

---

## See Also

- [Create Subscription](./34_CREATE_SUBSCRIPTION.md)

