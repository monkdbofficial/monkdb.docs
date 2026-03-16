# ALTER PUBLICATION

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
ALTER PUBLICATION publication_name
  { ADD TABLE table_name [, ...]
  | SET TABLE table_name [, ...]
  | DROP TABLE table_name [, ...] }
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
The `ALTER PUBLICATION` statement in MonkDB allows you to modify the list of tables included in an existing publication. This is essential for managing logical replication by dynamically adjusting the set of tables whose data changes are replicated to subscribers.

---

## SQL Statement

```sql
ALTER PUBLICATION publication_name
  { ADD TABLE table_name [, ...]
  | SET TABLE table_name [, ...]
  | DROP TABLE table_name [, ...] }
```

---

##  Subcommands

### 1. `ADD TABLE`

Adds one or more tables to the existing publication.

- **Usage:** Incorporate additional tables into a publication to start replicating their data changes to subscribers.

#### Yes Example

```sql
ALTER PUBLICATION sales_pub ADD TABLE new_orders, archived_orders;
```

---

### 2. `SET TABLE`

Replaces the current list of tables in the publication with the specified tables.

- **Usage:** Define a new set of tables for the publication, removing any previously included tables not specified in the new list.

#### Yes Example

```sql
ALTER PUBLICATION sales_pub SET TABLE current_orders, pending_orders;
```

---

### 3. `DROP TABLE`

Removes one or more tables from the publication.

- **Usage:** Stop replicating data changes of specific tables to subscribers by removing them from the publication.

#### Yes Example

```sql
ALTER PUBLICATION sales_pub DROP TABLE archived_orders;
```

---

##  Notes

- **Impact on Subscriptions:** Removing a table from a publication halts its replication to all subscribers. However, data already replicated remains on the subscriber clusters. To re-subscribe to these tables, they must be added back to the publication, and subscribers need to refresh their subscriptions.

- **Subscriber Table Behavior:** Tables on subscriber clusters that are removed from a publication become regular writable tables. They will no longer receive updates from the publisher but can be modified independently.

- **Replication Scope:** Ensure that any table added to a publication is intended for replication, as all data changes (`INSERT`, `UPDATE`, `DELETE`, and schema changes) will be propagated to subscribers.

---

##  Permissions

- **Publication Ownership:** You must own the publication to execute `ALTER PUBLICATION` commands.

- **Table Ownership:** Adding a table to a publication requires ownership of that table.

- **Superuser Requirements:** Using `ADD TABLES IN SCHEMA` or `SET TABLES IN SCHEMA` requires superuser privileges.

- **Owner Change Restrictions:** To alter the owner of a publication, you must have the ability to `SET ROLE` to the new owning role, and that role must have `CREATE` privilege on the database. Additionally, the new owner of a `FOR ALL TABLES` or `FOR TABLES IN SCHEMA` publication must be a superuser. However, a superuser can change the ownership of a publication regardless of these restrictions.

---

##  Summary

| Subcommand  | Purpose                                           | Requires Ownership | Requires Superuser |
|-------------|---------------------------------------------------|--------------------|--------------------|
| `ADD TABLE` | Add tables to the publication                     | Yes                | No                 |
| `SET TABLE` | Replace the publication's table list              | Yes                | No                 |
| `DROP TABLE`| Remove tables from the publication                | Yes                | No                 |

---

##  See Also

- [CREATE PUBLICATION](./29_CREATE_PUBLICATION.md)
- [DROP PUBLICATION](./48_DROP_PUBLICATION.md)

---

By utilizing the `ALTER PUBLICATION` statement, you can effectively manage the tables included in your publications, ensuring that the appropriate data changes are replicated to subscriber clusters as needed.
