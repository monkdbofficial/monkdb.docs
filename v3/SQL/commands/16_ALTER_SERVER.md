# ALTER SERVER

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
ALTER SERVER server_name OPTIONS ( option_name 'value' [, ...] )
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
The `ALTER SERVER` statement in MonkDB is used to modify the options of an existing foreign server. This is particularly useful when you need to update connection parameters or other settings associated with a foreign data wrapper.

---

## SQL Statement

```sql
ALTER SERVER server_name OPTIONS ( option_name 'value' [, ...] )
```

---

##  Parameters

- **`server_name`**: The name of the foreign server to be altered.
- **`OPTIONS`**: A clause used to specify one or more options to be updated for the foreign server. Each option is provided as a key-value pair.

---

##  Modifiable Options

The options that can be modified depend on the foreign data wrapper associated with the server. For example, with the `jdbc` foreign data wrapper, you can modify:

- **`url`**: The JDBC connection string for the foreign server.
- **`schema_name`**: The schema to be used when accessing tables in the foreign system.
- **`table_name`**: The table name to be used when accessing tables in the foreign system.

---

## Yes Examples

Update the JDBC connection URL for a foreign server named `my_postgresql`:

```sql
ALTER SERVER my_postgresql OPTIONS (url 'jdbc:postgresql://newhost:5432/');
```

Change both schema and table name options for the same server:

```sql
ALTER SERVER my_postgresql OPTIONS (schema_name 'new_schema', table_name 'new_table');
```

---

##  Notes

- **Foreign Data Wrappers**: The `ALTER SERVER` statement is used in conjunction with foreign data wrappers to manage connections to external data sources.
- **Option Validation**: MonkDB does not validate the options set using `ALTER SERVER`. Ensure the options are compatible with the foreign data wrapper.
- **Restart Requirements**: Some changes may require reconnecting or remapping the foreign tables to take effect.

---

##  Permissions

- **Ownership**: You must own the server to execute `ALTER SERVER`.
- **Superuser**: Some options may require superuser privileges depending on the wrapper and settings.

---

##  Summary

| Command                                | Description                                 | Requires Ownership | Requires Superuser |
|----------------------------------------|---------------------------------------------|--------------------|--------------------|
| `ALTER SERVER server_name OPTIONS (...)` | Modify options of a foreign server          | Yes                | No (Yes for some)  |

---

##  See Also

- [CREATE SERVER](./32_CREATE_SERVER.md)
- [DROP SERVER](./51_DROP_SERVER.md)

---

By using `ALTER SERVER`, administrators can dynamically manage foreign server configurations and maintain seamless access to external data sources in MonkDB.

---

## See Also

- [Create a Server](./32_CREATE_SERVER.md)
- [Create A Foreign Table](./27_CREATE_FOREIGN_TABLE.md)
