# SHOW SESSION SETTINGS

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | Session and Transaction Control |
| Mutates Data | No |
| Scope | Session / Transaction |
| Privilege Model | Session-scoped variants require session rights; global variants require administrative privilege. |

## Purpose

Executes the SHOW SESSION SETTINGS SQL command with MonkDB distributed runtime semantics.

## Syntax

```sql
SHOW { parameter_name | ALL }
```

## Operational Notes

- Use schema-qualified identifiers in automation and automation pipelines.
- Validate behavior in staging for cluster-impacting or governance-impacting changes.
- Confirm runtime effects through system tables and metrics before and after execution.

## When to Use

- Use to control session behavior, cursors, or transaction compatibility settings.
- Use when client compatibility or session-scoped runtime behavior must be explicit.

## When Not to Use

- Avoid relying on PostgreSQL-compatible clauses whose behavior is intentionally no-op in MonkDB.

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
The `SHOW` statement in MonkDB is used to retrieve the value of session settings. These settings apply only to the currently connected client session and can be modified using the `SET` statement. The `SHOW` statement is distinct from other `SHOW` commands, such as `SHOW TABLES`, and focuses exclusively on session-specific configurations.

## SQL Statement

```sql
SHOW { parameter_name | ALL }
```
- `parameter_name`: Displays the value of a specific session setting.
- `ALL`: Displays all active session settings.

## Examples

Retrieve a Specific Session Setting

```sql
SHOW search_path;
```

This command displays the current value of the `search_path` setting for the session.

Retrieve All Session Settings

```sql
SHOW ALL;
```

This command lists all active session settings along with their values.

### Modifying Session Settings

Session settings can be changed using the `SET` statement. For example

```sql
SET SESSION search_path TO myschema, doc;
```

This modifies the `search_path` for the current session. Changes made using `SET SESSION` are temporary and last only for the duration of the session.

Alternatively, you can modify certain settings permanently for a user by configuring default values per role.

## Key Session Settings in MonkDB

Some notable session settings include

- `statement_timeout`:
    - Defines the maximum duration (in milliseconds) for a query before it is canceled.
    - Default: `0` (queries run indefinitely).
    - Example:
    ```sql
    SET SESSION statement_timeout = '50000ms';
    ```

- `memory.operation_limit`:
    - Specifies the maximum memory (in bytes) an operation can consume before triggering an error.
    - Default: `0` (unlimited).
    - Example:
    ```sql
    SET SESSION memory.operation_limit = '1073741824'; -- 1GB
    ```
## Persistence Options

Session settings can also be configured at a global level using keywords like `PERSISTENT` or `TRANSIENT`. For example

### Persistent Cluster-Wide Setting

```sql
SET GLOBAL PERSISTENT statement_timeout = '30m';
```

### Transient Cluster-Wide Setting

```sql
SET GLOBAL TRANSIENT statement_timeout = '15m';
```

Persistent settings are saved to disk and survive cluster restarts, while transient settings are discarded upon cluster shutdown or restart.
