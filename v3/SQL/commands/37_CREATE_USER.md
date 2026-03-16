# CREATE USER

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
CREATE USER username
[ WITH ( user_parameter = value [, ...]) ] |
[ [ WITH ] user_parameter [value] [ ... ] ]
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
The `CREATE USER` command is utilized to establish a new database user within the MonkDB cluster. Users can log in to MonkDB and receive specific privileges to carry out different tasks.

---

## SQL Statement

```sql
CREATE USER username
[ WITH ( user_parameter = value [, ...]) ] |
[ [ WITH ] user_parameter [value] [ ... ] ]
```

---

## Description

The `CREATE USER` statement creates a new database user. By default, the newly created user does not have any privileges, and these must be assigned explicitly using the privileges management system.

### Key Features:
- **Authentication:** Users can authenticate against MonkDB using passwords or JWT-based authentication.
- **Privileges:** Newly created users do not have special privileges by default. Privileges must be granted separately.
- **User vs Role:**
  - A `USER` can log in to the database and be assigned a password but cannot be granted to another `USER` or `ROLE`.
  - A `ROLE` cannot log in or have a password but can be granted to other `USERS` or `ROLES`.

---

## Parameters

| Parameter   | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| **username** | The unique name of the database user. Must follow SQL identifier rules.    |

---

## Clauses

### **WITH**

The `WITH` clause allows you to specify parameters for defining a new user account.

#### Supported Parameters:

1. **password**
   - *Type:* text
   - Specifies the password for the user as a cleartext string literal.
   - **Examples:**
     ```sql
     CREATE USER john WITH (password = 'foo');
     CREATE USER john WITH password 'foo';
     CREATE USER john password 'foo';
     ```

2. **jwt**
   - *Type:* JSON object
   - Defines properties for JWT-based authentication.
   - Supported fields:
     - **iss**: The JWK endpoint containing public keys (*Required*).
     - **username**: The username in a third-party application (*Required*).
     - **aud**: The intended recipient of the JWT (*Optional*; defaults to cluster ID if not provided).
   - Combination of `iss` and `username` must be unique.
   - **Example:**
     ```sql
     CREATE USER john WITH (jwt = {
         "iss" = 'https://yourdomain.com',
         "username" = 'test@yourdomain.com',
         "aud" = 'test_aud'
     });
     ```

---

## Examples

### Example 1: Create a User with Password Authentication
Create a user named `john` with a password:

```sql
CREATE USER john WITH (password = 'secure_password');
```

---

### Example 2: Create a User with JWT-Based Authentication
Create a user named `api_user` with JWT properties:

```sql
CREATE USER api_user WITH (jwt = {
"iss" = 'https://auth.yourdomain.com',
"username" = 'api_user@yourdomain.com',
"aud" = 'api_audience'
});
```

---

### Example 3: Create a User Without Authentication Parameters
Create a user named `guest` without specifying authentication details:

```sql
CREATE USER guest;
```

This user can only authenticate if host-based authentication (HBA) allows it.

---

## Notes

1. **Authentication Requirements:**
   - Passwords are optional if password authentication is disabled.
   - If JWT-based authentication is enabled (`auth.host_based.jwt.iss` is set), user-specific JWT properties are ignored, and cluster-wide JWT settings are used instead.
2. **Privileges:** Users must be explicitly assigned privileges using statements like `GRANT`.
3. **Unique Identifiers:** Ensure usernames are unique within the cluster.
4. **Security Considerations:** Avoid storing sensitive information like passwords in plain text unless necessary.

---

##  Permissions

- **Create User**:
  - Requires `AL` (Admin Level) privileges on the cluster.

- **Password Management**:
  - Only superusers or Admin-level users can assign passwords during user creation.
  - Passwords must comply with any configured password policy (if enforced).

- **JWT-Based Authentication**:
  - Users must have `jwt` fields (`iss`, `username`) properly configured.
  - The `iss` + `username` combination must be unique across all users.

- **Granting Privileges**:
  - Requires `GRANT` privileges on the relevant database objects (schemas, tables, etc.) to assign access rights after user creation.

>  Security Best Practice: Grant the minimum required privileges after user creation, and rotate passwords or JWT tokens regularly if applicable.

---

##  Summary

| Feature                         | Supported / Required                                             |
|----------------------------------|------------------------------------------------------------------|
| Supports Login                  | Yes Yes                                                           |
| Password Authentication         | Yes Optional (if supported by cluster)                            |
| JWT Authentication              | Yes Optional                                                      |
| HBA-Only Access (no credentials)| Yes Yes, if allowed by host-based authentication config           |
| Requires Admin Privileges       | Yes Yes (`AL`)                                                    |
| Assignable Privileges           | Yes Must be granted post-creation                                 |
| Can Be Altered                  | Yes Via `ALTER USER`                                              |
| Can Be Dropped                  | Yes Via `DROP USER`                                               |
| Can Be Granted to Other Users   | No No (only `ROLES` can be granted to users)                     |
| Can Belong to Roles             | Yes Yes (via `GRANT role_name TO user_name`)                      |

---

## See Also

- [Alter User](./18_ALTER_USER.md)

