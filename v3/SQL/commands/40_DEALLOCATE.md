# DEALLOCATE

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | Session and Transaction Control |
| Mutates Data | Yes/Depends |
| Scope | Statement |
| Privilege Model | Session-scoped variants require session rights; global variants require administrative privilege. |

## Purpose

Executes the DEALLOCATE SQL command with MonkDB distributed runtime semantics.

## Syntax

```sql
DEALLOCATE [PREPARE] { name | ALL }
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
## SQL Statement

```sql
DEALLOCATE [PREPARE] { name | ALL }
```

## Description
The `DEALLOCATE` command serves to release resources linked to a previously prepared SQL statement. While prepared statements are automatically deallocated at the conclusion of a session, this command provides a means for explicit deallocation. It is frequently utilized by clients, such as `libpq`, as an alternative to the protocol's `Close (F)` message.

### Key Points:
- **Automatic Deallocation**: Prepared statements are automatically deallocated at the end of a session.
- **Explicit Deallocation**: Use the `DEALLOCATE` command to manually free resources associated with a specific prepared statement or all prepared statements.

## Parameters
- **name**: Specifies the identifier of the prepared statement that is to be deallocated.
- **ALL**: Removes all prepared statements associated with the current session.

## Examples

### Example 1: Deallocate a Specific Prepared Statement

```sql
DEALLOCATE emp_info;
```

This command explicitly deallocates the prepared statement named `emp_info`.

### Example 2: Deallocate All Prepared Statements

```sql
DEALLOCATE ALL;
```

This command frees resources for all prepared statements in the current session.

### Verification
To confirm that a prepared statement has been deallocated:

```sql
SELECT name, statement FROM pg_prepared_statements;
```

After executing `DEALLOCATE`, the specified statement will no longer appear in this view.

## Notes
- The `PREPARE` keyword in the syntax is optional and ignored.
- The SQL standard includes a `DEALLOCATE` statement, but it is primarily used in embedded SQL contexts.

---

## See Also

- [Create a View](./39_CREATE_VIEW.md)
