# DROP USER

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
DROP USER [ IF EXISTS ] username;
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
## SQL Statement

```sql
DROP USER [ IF EXISTS ] username;
```

## Description

The `DROP USER` statement in MonkDB is used to remove an existing database user or role. Its syntax and functionality are identical to the `DROP ROLE` statement in MonkDB.

## Parameters
- **IF EXISTS**: This clause prevents the statement from failing if the specified user does not exist. Instead, it returns a warning for each non-existent user.
- **username**: The unique name of the database user or role to be removed. The name must follow SQL identifier principles.

## Usage Notes
- **Role Dependencies**: If a role is granted to other roles or users, it cannot be dropped until these grants are revoked.
- **Permissions**: The user executing this command must have appropriate permissions to manage users or roles in the database.
- **Effect on Sessions**: Dropping a user does not automatically close any open sessions. The user is effectively dropped after their session is closed.

## Examples

To drop a user named `exampleuser`, you would use:

```sql
DROP USER exampleuser;
```

If you want to avoid errors when dropping a user that might not exist, use the `IF EXISTS` clause:

```sql
DROP USER IF EXISTS exampleuser;
```

## Additional Considerations
- **Security Context**: Dropping a user does not automatically invalidate or drop databases or objects created by that user. You may need to manually manage these resources after dropping the user.
- **Scripting**: The `IF EXISTS` clause is particularly useful in scripts to prevent errors when attempting to drop non-existent users.

---

## See Also

- [Drop Role](./50_DROP_ROLE.md)
- [Create User](./37_CREATE_USER.md)
- [Alter User](./18_ALTER_USER.md)

