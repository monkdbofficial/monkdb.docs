# SET RESET

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | Session and Transaction Control |
| Mutates Data | Yes/Depends |
| Scope | Session / Transaction |
| Privilege Model | Session-scoped variants require session rights; global variants require administrative privilege. |

## Purpose

Executes the SET RESET SQL command with MonkDB distributed runtime semantics.

## Syntax

```sql
SET [ SESSION | LOCAL ] setting_ident { = | TO } { setting_value | 'setting_value' | DEFAULT }
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
MonkDB provides the `SET` and `RESET` commands to change or restore runtime settings. These commands allow for dynamic configuration adjustments at both session and global levels, depending on the scope and persistence required.

## SQL Statement

### SET
#### Session/Local Settings

```sql
SET [ SESSION | LOCAL ] setting_ident { = | TO } { setting_value | 'setting_value' | DEFAULT }
```

- `SESSION`: Applies the setting to the current session (default behavior).
- `LOCAL`: Applies the setting only for the current transaction. Ignored by MonkDB but included for PostgreSQL compatibility.

#### Global Settings

```sql
SET GLOBAL [ PERSISTENT | TRANSIENT ] { setting_ident [ = | TO ] { value | ident } } [, ...]
```
- `PERSISTENT`: Saves the setting permanently to disk, surviving cluster restarts.
- `TRANSIENT`: Applies the setting temporarily; discarded after cluster restart.

### RESET Command

Reset global settings to their default values,

```sql
RESET GLOBAL setting_ident [, ...]
```
## Description

### SET GLOBAL
- Modifies cluster-wide settings dynamically.
- Can use `PERSISTENT` for permanent changes or `TRANSIENT` for temporary changes.
- If a setting is unsupported or invalid, MonkDB logs it with an INFO level message.

### SET SESSION/LOCAL
- Affects only the current session or transaction if supported.
- `SET LOCAL` has no effect on MonkDB configurations but ensures compatibility with third-party applications using PostgreSQL's wire protocol.

### RESET GLOBAL
- Restores a global cluster setting to its default value or the value defined in the configuration file during node startup.

## Parameters

- `setting_ident`: Fully qualified identifier of the setting to modify or reset.
- `value`: The new value assigned to a setting (string, number, identifier, or comma-separated list).
- `DEFAULT`: Resets a parameter to its default value.

## Persistence

- `TRANSIENT` (default): Changes are temporary and lost after a cluster restart.
- `PERSISTENT`: Changes are saved to disk and retained across restarts.

> **Note**: The `PERSISTENT` keyword is applicable only within a `SET GLOBAL` statement.

## Examples

Set a Global Setting Temporarily

```sql
SET GLOBAL TRANSIENT indices.recovery.max_bytes_per_sec = '40mb';
```

Set a Persistent Global Setting

```sql
SET GLOBAL PERSISTENT discovery.zen.minimum_master_nodes = 2;
```

Reset a Global Setting

```sql
RESET GLOBAL indices.recovery.max_bytes_per_sec;
```

Set Session Parameters

```sql
SET SESSION search_path TO my_schema, public;
```

Set Local Parameters (Ignored in MonkDB)

```sql
SET LOCAL timezone TO 'UTC';
```

## Key Notes

- Only settings marked with Runtime: yes can be modified at runtime.
- Unsupported settings will not result in errors but will be logged for informational purposes.
- These commands ensure compliance with PostgreSQL applications while enabling dynamic configuration management in MonkDB.

