# DROP VIEW

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | DDL and Administration |
| Mutates Data | Yes/Depends |
| Scope | Cluster / Object |
| Privilege Model | Requires DDL/administrative privilege according to target object scope. |

## Purpose

Defines, changes, or removes schema and metadata objects.

## Syntax

```sql
DROP VIEW [ IF EXISTS ] view_name [,... ]
```

## Operational Notes

- Use schema-qualified identifiers in automation and automation pipelines.
- Validate behavior in staging for cluster-impacting or governance-impacting changes.
- Confirm runtime effects through system tables and metrics before and after execution.

## When to Use

- Use during planned schema and runtime administration changes.
- Use in automation pipelines with environment-specific validation and rollback strategy.

## When Not to Use

- Avoid during incident windows unless the command is part of approved mitigation.
- Avoid schema changes in peak traffic windows without staged rollout.

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
The `DROP VIEW` statement in MonkDB is used to remove one or more existing views from the database.

## SQL Statement

```sql
DROP VIEW [ IF EXISTS ] view_name [,... ]
```

## Description

- **Purpose**: The `DROP VIEW` statement is used to delete views that were previously created using the `CREATE VIEW` statement.
- **Behavior**: If a view does not exist and the `IF EXISTS` clause is not used, the command will return an error. However, if `IF EXISTS` is specified, the command will simply ignore non-existent views and drop only the existing ones.

## Key Points
- **Multiple Views**: You can drop multiple views with a single command by listing them after the `DROP VIEW` statement.
- **Privileges**: You need appropriate permissions to drop views.
- **Impact on Data**: Since views are logical constructs without physical data, dropping a view only affects metadata and does not delete any actual data.

## Example

To drop a view named `my_view`

```sql
DROP VIEW my_view;
```

To drop multiple views, including one that might not exist

```sql
DROP VIEW IF EXISTS my_view, another_view, non_existent_view;
```

This command will drop `my_view` and `another_view` if they exist, and will not throw an error if `non_existent_view` does not exist.

---

## See Also

- [Create View](./39_CREATE_VIEW.md)

