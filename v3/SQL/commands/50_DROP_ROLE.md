# DROP ROLE

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | Security and Access Control |
| Mutates Data | Yes/Depends |
| Scope | Cluster / Object |
| Privilege Model | Requires administrative privilege for role, user, and privilege management. |

## Purpose

Defines, changes, or removes schema and metadata objects.

## Syntax

```sql
DROP ROLE [ IF EXISTS ] name;
```

## Operational Notes

- Use schema-qualified identifiers in automation and automation pipelines.
- Validate behavior in staging for cluster-impacting or governance-impacting changes.
- Confirm runtime effects through system tables and metrics before and after execution.

## When to Use

- Use to implement least-privilege access and role governance.
- Use when onboarding users/roles or changing permission boundaries.

## When Not to Use

- Avoid broad wildcard grants/denials without impact review and audit traceability.

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
The `DROP ROLE` statement in MonkDB is used to remove an existing database user or role from the cluster.

## SQL Statement

```sql
DROP ROLE [ IF EXISTS ] name;
```

## Description

The `DROP ROLE` statement deletes a specified role or user from the MonkDB cluster. It is part of MonkDB's user and role management system, which allows administrators to manage access and permissions effectively

Key Features

- **IF EXISTS**: Prevents errors if the specified role does not exist. Instead, it issues a notice.
- **name**: Represents the unique identifier of the role or user to be removed. This follows SQL identifier principles

## Important Considerations

- **Role Dependencies**: A role cannot be dropped if it has been granted to other roles or users. You must revoke these grants first.
- **Ownership of Objects**: If the role owns database objects (e.g., schemas), those objects must either be reassigned to another role or dropped before removing the role.
- **Revoking Permissions**: Any privileges granted to the role must be revoked prior to using `DROP ROLE`.
- **Superuser Privileges**: To drop a superuser role, you must have superuser privileges. For non-superuser roles, the `CREATE ROLE` privilege is required

## Examples

If you want to drop a user/role in MonkDB:

```sql
DROP USER IF EXISTS role_name;
```

If you granted schema/table-level privileges earlier and want to revoke them.

```sql
REVOKE DQL, DML ON SCHEMA monkdb.{table_name} FROM role_name;
```

Then drop the user.

---

## See Also

- [Create role](./31_CREATE_ROLE.md)
