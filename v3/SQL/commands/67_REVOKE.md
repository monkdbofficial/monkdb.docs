# REVOKE

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | Security and Access Control |
| Mutates Data | Yes/Depends |
| Scope | Cluster / Object |
| Privilege Model | Requires administrative privilege for role, user, and privilege management. |

## Purpose

Manages permissions and access control behavior.

## Syntax

```sql
REVOKE { { DQL | DML | DDL | AL [,...] } | ALL [ PRIVILEGES ] }
[ON {SCHEMA | TABLE | VIEW} identifier [, ...]]
FROM name [, ...];
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
The `REVOKE` statement in MonkDB is a SQL command used to manage security by removing previously granted privileges or roles from users or roles. It ensures that access rights are appropriately controlled.

## SQL Statement

```sql
REVOKE { { DQL | DML | DDL | AL [,...] } | ALL [ PRIVILEGES ] }
[ON {SCHEMA | TABLE | VIEW} identifier [, ...]]
FROM name [, ...];
```
```sql
REVOKE role_name_to_revoke [, ...] FROM name [, ...];
```

## Key Components
- **Privileges**:
    - **DQL**: Data Query Language privileges (e.g., `SELECT`).
    - **DML**: Data Manipulation Language privileges (e.g., `INSERT`, `UPDATE`, `DELETE`).
    - **DDL**: Data Definition Language privileges (e.g., `CREATE`, `DROP`).
    - **AL**: Administrative privileges.
    - **ALL PRIVILEGES**: Revokes all privileges.
- **Object Types**:
    - `SCHEMA`, `TABLE`, `VIEW`: Specifies the type of database object from which privileges are revoked.
- **Role Revocation**: This removes a role from a user or another role, and the associated privileges inherited from the role are also revoked.
- **Cluster-Level Revocation**: If no object type is specified, privileges are revoked at the cluster level.

## Description

The `REVOKE` statement operates in two main ways:

+ **Privilege Revocation**: Removes specific permissions on database objects (e.g., tables, views) from users or roles.
+ **Role Revocation**: Removes roles assigned to users or other roles, effectively revoking all inherited permissions.

For example, if a user has been granted a role with specific privileges, revoking the role will also revoke those privileges.

## Parameters
- `identifier`:
    - Refers to the name of the object (e.g., table or view) for which permissions are being revoked.
    - Must be fully qualified if dealing with specific tables or views.
- `role_name_to_revoke`: Specifies the name of the role to be removed from a user or another role.
- `name`: Refers to the user or role from which privileges or roles are being revoked.

## Examples
### Example 1. Revoke Privileges on a Table

```sql
REVOKE SELECT ON SCHEMA.table_name FROM user_name;
```

This removes the SELECT privilege on a specific table from a user.

### Example 2. Revoke All Privileges

```sql
REVOKE ALL PRIVILEGES FROM user_name;
```

This revokes all access rights from a user across all objects.

### Example 3. Revoke Role

```sql
REVOKE role_name FROM user_name;
```

This removes the specified role and its associated privileges from a user.

### Example 4. Cluster-Level Revocation

```sql
REVOKE DML FROM role_name;
```

Revokes DML privileges at the cluster level for a role.

## Usage Notes
- The `REVOKE` statement is essential for maintaining database security and ensuring users and roles have only necessary access.
- It complements the `GRANT` statement, which is used to assign permissions.
- Administrators must have sufficient permissions to execute `REVOKE`.

---

## See Also

- [Grant](./61_GRANT.md)
