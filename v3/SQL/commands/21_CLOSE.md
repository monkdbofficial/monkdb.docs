# CLOSE

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | Session and Transaction Control |
| Mutates Data | No |
| Scope | Session / Transaction |
| Privilege Model | Session-scoped variants require session rights; global variants require administrative privilege. |

## Purpose

Executes the CLOSE SQL command with MonkDB distributed runtime semantics.

## Syntax

```sql
CLOSE { cursor_name | ALL };
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
The `CLOSE` statement in MonkDB is used to close cursors that have been previously declared using the `DECLARE` statement. Closing a cursor releases the resources associated with it.

---

## SQL Statement

```sql
CLOSE { cursor_name | ALL };
```

---

##  Description

- `CLOSE cursor_name`: Closes the cursor identified by `cursor_name`. Attempting to close a cursor that does not exist will result in an error.​
- `CLOSE ALL`: Closes all open cursors within the current session.

---

##  Parameters

- `cursor_name`: The name of the cursor to be closed. This must match the name used in the corresponding DECLARE statement.

---

## Yes Example

Assuming a cursor named `my_cursor` has been declared, you can close it using:​

```sql
CLOSE my_cursor;
```

To close all open cursors in the current session:​

```sql
CLOSE ALL;
```

##  Notes

Closing a cursor that has already been closed or does not exist will result in an error. It's good practice to ensure that cursors are properly managed to avoid such errors.​

MonkDB does not support transactions; therefore, cursors are managed independently of transactional control statements.

---

## See Also

- [Begin](./20_BEGIN.md)
