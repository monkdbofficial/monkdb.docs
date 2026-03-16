# CREATE SERVER

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | Federation (FDW) |
| Mutates Data | Yes/Depends |
| Scope | Cluster / Object |
| Privilege Model | Requires administrative privilege on foreign server, table, and mapping objects. |

## Purpose

Defines, changes, or removes schema and metadata objects.

## Syntax

```sql
CREATE SERVER [IF NOT EXISTS] server_name FOREIGN DATA WRAPPER fdw_name
[ OPTIONS ( option value [, ...] ) ]
```

## Operational Notes

- Use schema-qualified identifiers in automation and automation pipelines.
- Validate behavior in staging for cluster-impacting or governance-impacting changes.
- Confirm runtime effects through system tables and metrics before and after execution.

## When to Use

- Use to register and query external data systems through SQL federation.
- Use when centralized query execution is preferred over external engine orchestration.

## When Not to Use

- Avoid expecting full pushdown for complex joins/aggregations unless explicitly supported.

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
The `CREATE SERVER` statement is used to define a connection to an external data source, creating a foreign server within MonkDB. This allows you to access and query data residing in other systems as if they were local tables.

---

## SQL Statement

```sql
CREATE SERVER [IF NOT EXISTS] server_name FOREIGN DATA WRAPPER fdw_name
[ OPTIONS ( option value [, ...] ) ]
```

---

## Description

The `CREATE SERVER` statement establishes a connection to a foreign data source. This connection is represented as a foreign server, which is then used by foreign tables to access data in the external system.

### Key Components:
- **Foreign Data Wrappers (FDWs):** MonkDB uses FDWs to handle communication with different types of external systems. You must specify the FDW to use when creating a server.
- **Connection Parameters:** The `OPTIONS` clause allows you to specify connection parameters specific to the chosen FDW, such as the URL, username, and password.

---

## Parameters

| Parameter        | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| **server_name**   | A unique name for the foreign server.                                      |
| **fdw_name**      | The name of the foreign data wrapper to use (e.g., `jdbc`).                |

---

## Clauses

### **IF NOT EXISTS**
Prevents an error if the server already exists. If a server with the given name already exists, the statement does nothing.

### **OPTIONS**
Specifies connection options for the foreign server. These options are specific to the FDW being used.

| Option  | Description                                                                      |
|---------|----------------------------------------------------------------------------------|
| `url`   | The connection string or URL for the external system (e.g., JDBC URL).            |
| `user`  | The username for authentication with the external system.                         |
| `password`| The password for authentication with the external system.                        |
| ...     | Other FDW-specific options (e.g., `database`, `schema`, `table`).              |

---

## Examples

### Example 1: Creating a JDBC Server
Create a foreign server named `my_postgresql` using the `jdbc` FDW to connect to a PostgreSQL database:

```sql
CREATE SERVER my_postgresql FOREIGN DATA WRAPPER jdbc
OPTIONS (url 'jdbc:postgresql://example.com:5432/my_database');
```

This defines the connection to the database using a JDBC URL.

---

<!-- ### Example 2: Creating a Server with Authentication
Create a server with username and password:

```sql
CREATE SERVER my_sql_server FOREIGN DATA WRAPPER jdbc
OPTIONS (
url 'jdbc:postgresql://example.com:5432/my_database',
user 'my_user',
password 'my_password'
);
```

This includes authentication credentials in the server definition. -->

Use `CREATE USER MAPPING` to manage foreign username and password during connections.
---

### Example 3: Using IF NOT EXISTS
Create a server that only gets created if it doesn't already exist:

```sql
CREATE SERVER IF NOT EXISTS my_postgresql FOREIGN DATA WRAPPER jdbc
OPTIONS (url 'jdbc:postgresql://example.com:5432/my_database');
```

This command will not produce an error if `my_mongodb` already exists.

---

## Notes

1. **FDW Installation:** Ensure that the necessary FDW is installed in MonkDB before creating a server that uses it.
2. **Privileges Required:** Creating a server requires `AL` (Admin Level) privileges on the cluster.
3. **Server Visibility:** Servers created using `CREATE SERVER` are visible in `information_schema.foreign_servers`.
4. **Option Information:** Options for foreign servers are available in `information_schema.foreign_server_options`.
5. **Security:** Be mindful of storing sensitive information like passwords in plain text within the server definition. Consider using more secure methods for managing credentials.

---

##  Permissions

- **Creating a Foreign Server**:
  - Requires `AL` (Admin Level) privileges on the cluster.
- **Modifying or Dropping a Server**:
  - Only the user who created the server or a superuser can modify or drop it.
- **Using a Server in Foreign Tables**:
  - Requires `USAGE` privilege on the foreign server.
- **Authentication Mapping**:
  - Use `CREATE USER MAPPING` to associate MonkDB users with remote credentials. This can be scoped per server.

>  Passwords and secrets passed as options should be managed carefully. Consider restricting access to the server definitions if storing sensitive data.

---

##  Summary

| Feature                        | Supported / Required                                       |
|--------------------------------|------------------------------------------------------------|
| Foreign Data Wrapper Required  | Yes Yes (`jdbc`, etc.)                                     |
| Custom Connection Options      | Yes Yes (via `OPTIONS`)                                    |
| Supports IF NOT EXISTS         | Yes Yes                                                    |
| Authentication Support         | Yes Yes (via `CREATE USER MAPPING`)                        |
| Permissions Required           | Yes `AL` (Admin Level) to create/modify                     |
| Server Listing                 | Yes Via `information_schema.foreign_servers`               |
| Server Option Metadata         | Yes Via `information_schema.foreign_server_options`        |
| Grants for Table Use           | Yes Must have `USAGE` privilege on the foreign server      |

---

## See also

- [Create Foreign Table](./27_CREATE_FOREIGN_TABLE.md)
- [Alter Server](./16_ALTER_SERVER.md)
- [Drop Server](./51_DROP_SERVER.md)
