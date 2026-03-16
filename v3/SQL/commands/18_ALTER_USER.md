# ALTER USER

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
ALTER USER username
    { SET ( parameter = value [, ...] )
    | RESET [parameter | ALL] }
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
The `ALTER USER` statement in MonkDB is used to modify attributes of an existing database user. This includes setting or resetting parameters such as passwords, JWT properties, and session settings. The `ALTER USER` statement functions identically to the `ALTER ROLE` statement.

---

## SQL Statement

```sql
ALTER USER username
    { SET ( parameter = value [, ...] )
    | RESET [parameter | ALL] }
```

##  Parameters

- `username`: The name of the user to be altered.​
- `SET`: Assigns new values to specified parameters for the user.​
- `RESET`: Restores specified parameters to their default values.

##  See Also

- [ALTER ROLE](./15_ALTER_ROLE.md)
- [CREATE ROLE](./31_CREATE_ROLE.md)
- [DROP ROLE](./50_DROP_ROLE.md)
