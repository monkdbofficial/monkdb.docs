# COMMIT

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | Session and Transaction Control |
| Mutates Data | Yes/Depends |
| Scope | Session / Transaction |
| Privilege Model | Session-scoped variants require session rights; global variants require administrative privilege. |

## Purpose

Executes the COMMIT SQL command with MonkDB distributed runtime semantics.

## Syntax

```sql
COMMIT;
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
The `COMMIT` statement in MonkDB is accepted for compatibility with PostgreSQL clients but does not perform any transactional operations, as MonkDB does not support transactions. Its primary function is to close all existing cursors within the current session.

---

## SQL Statement

```sql
COMMIT;
```

##  Description

- **Purpose**: In MonkDB, issuing a COMMIT command closes all existing cursors in the current session.​
- **Behavior**:
    + Since MonkDB operates with auto-commit behavior for each individual statement, the `COMMIT` command does not commit transactions but serves to close cursors.​

## Yes Example

To close all cursors in the current session:​

```sql
COMMIT;
```

##  Notes

- **Transaction Support**: MonkDB does not support traditional transactions. Commands like `BEGIN`, `COMMIT`, and `ROLLBACK` are accepted for compatibility purposes but do not alter database behavior. ​
- **Cursor Management**: Executing `COMMIT` will close all cursors within the current session. It's advisable to manage cursors appropriately to ensure efficient resource utilization.

##  Permissions

- **Execution Rights**: Any user with the ability to execute SQL statements can issue the `COMMIT` command. No special permissions are required.

##  Summary

| Command | Description                                     | Transaction Support | Cursor Management |
|---------|-------------------------------------------------|---------------------|-------------------|
| COMMIT  | Closes all existing cursors in the current session | No                  | Yes               |

##  See Also

- [BEGIN](./20_BEGIN.md)
- [CLOSE](./21_CLOSE.md)

