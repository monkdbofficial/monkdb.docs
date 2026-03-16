# SHOW CREATE TABLE

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | DDL and Administration |
| Mutates Data | No |
| Scope | Statement |
| Privilege Model | Requires DDL/administrative privilege according to target object scope. |

## Purpose

Executes the SHOW CREATE TABLE SQL command with MonkDB distributed runtime semantics.

## Syntax

```sql
SHOW CREATE TABLE <schema_name>.<table_name>;
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
The `SHOW CREATE TABLE` statement in MonkDB is a useful SQL command that returns the SQL definition used to create an existing table, including its columns, data types, primary key constraints, partitioning, clustering, generated columns, and other table settings.

This command is extremely helpful when:

- You want to inspect the schema of an existing table.
- You're reverse engineering a table's definition for backup, documentation, or recreation in another environment.
- You're debugging schema-related issues or reviewing how certain table-level options were configured.

> It gives you the `CREATE TABLE` or `CREATE FOREIGN TABLE` statement that you would use to recreate the same table structure.

## SQL Statement

```sql
SHOW CREATE TABLE <schema_name>.<table_name>;
```

Or if you're working in the default `monkdb` schema:

```sql
SHOW CREATE TABLE <table_name>;
```

> **PS**: MonkDB contains only one schema- `monkdb`, and the tables, etc are created under it.

Where `table_name` is the name of the table (optionally schema-qualified) whose schema needs to be displayed.

## Key Features
- **Schema Retrieval**: Displays the complete schema of a table, including column definitions, indexes, constraints, and other properties.

## Things to Note

- **Only shows current schema**: If a table was altered after creation, the output reflects the latest state.
- **Doesn’t show data**: This is purely about schema, not the contents.
- No `IF NOT EXISTS` or `CREATE OR REPLACE`: The generated SQL is suitable for fresh creation and schema recreation workflows.

## Use Cases

- **Portability**: You can copy the output and use it to recreate the table in another MonkDB cluster.
- **Versioning Schema**: Useful for maintaining schema versions in version control systems.
- **Auditing**: When managing large MonkDB deployments, quickly reviewing table definitions across databases can help spot inconsistencies or misconfigurations.

## Example

If you have a table called `sensor_data` in `monkdb` schema, and you run:

```sql
SHOW CREATE TABLE sensor_data;
```

You might get something like:

```sql
CREATE TABLE "doc"."sensor_data" (
   "id" TEXT,
   "temperature" DOUBLE PRECISION,
   "timestamp" TIMESTAMP WITH TIME ZONE,
   PRIMARY KEY ("id", "timestamp")
)
CLUSTERED INTO 4 SHARDS
PARTITIONED BY ("timestamp")
WITH ("number_of_replicas" = '1');
```

This tells you:
- Table columns and types
- Composite primary key (id, timestamp)
- It’s clustered into 4 shards
- Partitioned by the timestamp column
- Replication is set to 1 replica

---

## See Also

- [Create Table](./35_CREATE_TABLE.md)
- [Create Foreign Table](./27_CREATE_FOREIGN_TABLE.md)
