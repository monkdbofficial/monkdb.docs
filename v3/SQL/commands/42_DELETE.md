# DELETE

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | DML |
| Mutates Data | Yes/Depends |
| Scope | Statement |
| Privilege Model | Requires write privilege (DML) and read privilege where predicates reference source relations. |

## Purpose

Mutates table rows while honoring MonkDB indexing, routing, and write-path semantics.

## Syntax

```sql
DELETE FROM table_ident [ [AS] table_alias ] [ WHERE condition ]
```

## Operational Notes

- Use schema-qualified identifiers in automation and automation pipelines.
- Validate behavior in staging for cluster-impacting or governance-impacting changes.
- Confirm runtime effects through system tables and metrics before and after execution.

## When to Use

- Use for controlled data mutations and ingest/export workflows.
- Use when transactional scope is statement-level and operational visibility is available.

## When Not to Use

- Avoid large write bursts without capacity checks for breakers, disk, and shard health.
- Avoid ad-hoc production mutations without clear idempotency or rollback plan.

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
The `DELETE` command in MonkDB (and SQL in general) is used to remove rows from a table based on specified conditions.

## SQL Statement

```sql
DELETE FROM table_ident [ [AS] table_alias ] [ WHERE condition ]
```

## Description

The `DELETE` statement removes rows from a designated table that meet the conditions specified in the `WHERE` clause. If the `WHERE` clause is omitted, all rows in the table will be deleted, resulting in a valid but empty table.

## Parameters

- **table_ident**: The name of an existing table from which rows will be deleted, which can include an optional schema qualification.
- **table_alias**: An alternative name for the target table. When an alias is used, it conceals the actual table name entirely. For instance, in the statement `DELETE FROM foo AS f`, all subsequent references to this table must use f instead of foo.
- **condition**: A boolean expression that determines which rows will be deleted. Only those rows for which this expression evaluates to true will be removed.

---

## Examples

### Example 1. Delete Specific Rows

To remove rows based on a condition:

```sql
DELETE FROM employees WHERE department = 'HR';
```

This deletes all rows where the department column has the value `HR`.

### Example 2. Delete Using Table Alias

You can use an alias for the table to simplify references:

```sql
DELETE FROM employees AS e WHERE e.department = 'Finance';
```

This deletes rows from the employees table where the department is `Finance`, using the alias `e`.

### Example 3. Delete Rows Based on Multiple Conditions

Combine conditions with logical operators:

- Using AND:

```sql
DELETE FROM employees WHERE department = 'Sales' AND age > 40;
```

Deletes rows where both conditions are true.

- Using OR:

```sql
DELETE FROM employees WHERE department = 'Marketing' OR age < 25;
```

Deletes rows where either condition is true.

### Example 4. Delete All Rows

To empty a table without dropping its structure:

```sql
DELETE FROM employees;
```

This removes all rows from the employees table, leaving it empty but intact.

### Example 5. Delete with Schema Qualification

Specify a schema-qualified table name:

```sql
DELETE FROM company.employees WHERE department = 'IT';
```

Deletes rows from the employees table within the company schema where the department is `IT`.

### Example 6. Delete and Return Deleted Rows

MonkDB supports returning information about deleted rows:

```sql
DELETE FROM employees WHERE department = 'HR' RETURNING id, name;
```

This deletes rows and returns their id and name.
