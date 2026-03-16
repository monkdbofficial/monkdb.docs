# ALTER ROLE

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
ALTER ROLE role_name
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
The `ALTER ROLE` statement in MonkDB is used to modify attributes of an existing database role or user. This includes setting or resetting parameters such as passwords, JWT properties, and session settings.

---

## SQL Statement

```sql
ALTER ROLE role_name
    { SET ( parameter = value [, ...] )
    | RESET [parameter | ALL] }
```

---

##  Parameters

- **`role_name`**: The name of the role or user to be altered.
- **`SET`**: Assigns new values to specified parameters for the role.
- **`RESET`**: Restores specified parameters to their default values.

---

##  Modifiable Parameters

### `password`

Sets or removes the password for the user.

- Set password:

```sql
ALTER ROLE alice SET (password = 'secure_password');
```

- Remove password:

```sql
ALTER ROLE alice SET (password = NULL);
```

> Note: Passwords cannot be set for the `monkdb` superuser.

---

### `jwt`

Configures JWT (JSON Web Token) properties for user authentication.

- Set JWT properties:

```sql
ALTER ROLE alice SET (jwt = '{"iss": "issuer", "username": "alice", "aud": "audience"}');
```

- Remove JWT:

```sql
ALTER ROLE alice SET (jwt = NULL);
```

> Note: JWT properties must be unique across users.

---

### Session Settings

Set default session parameters, such as schema:

```sql
ALTER ROLE alice SET (search_path = 'myschema');
```

---

##  Resetting Parameters

- Reset specific parameter:

```sql
ALTER ROLE alice RESET search_path;
```

- Reset all parameters:

```sql
ALTER ROLE alice RESET ALL;
```

---

##  Notes

- A `ROLE` cannot log in and cannot have a password.
- A `USER` can log in and have a password.
- Session setting changes apply to **new** sessions.
- Users can modify **their own** roles without extra privileges.

---

##  Permissions

- **Superusers** can modify any role or user.
- Users with `ALTER` privilege on a role can modify it.
- Users can always modify their own roles.

---

##  Summary

| Command                            | Description                             | Requires Superuser | Requires `ALTER` Privilege | Self-Modifiable |
|------------------------------------|-----------------------------------------|--------------------|-----------------------------|-----------------|
| `ALTER ROLE role_name SET (...)`   | Set parameters for a role or user       | Yes Yes             | Yes Yes                      | Yes Yes          |
| `ALTER ROLE role_name RESET ...`   | Reset parameters to default values      | Yes Yes             | Yes Yes                      | Yes Yes          |

---

##  See Also

- [CREATE ROLE](./31_CREATE_ROLE.md)
- [DROP ROLE](./50_DROP_ROLE.md)

---

With `ALTER ROLE`, MonkDB enables robust control over user and role configurations, supporting password management, authentication setup, and user-specific defaults.
