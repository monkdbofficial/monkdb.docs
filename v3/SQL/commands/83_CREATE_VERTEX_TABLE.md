# CREATE VERTEX TABLE

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | Platform Extensions |
| Mutates Data | Yes/Depends |
| Scope | Cluster / Object |
| Privilege Model | Requires administrative or feature-specific governance/cluster privileges. |

## Purpose

Defines, changes, or removes schema and metadata objects.

## Syntax

```sql
CREATE VERTEX TABLE [IF NOT EXISTS] schema.table
FOR GRAPH graph_name
KEY key_column
[WITH (...)]
```

## Operational Notes

- Use schema-qualified identifiers in automation and automation pipelines.
- Validate behavior in staging for cluster-impacting or governance-impacting changes.
- Confirm runtime effects through system tables and metrics before and after execution.

## When to Use

- Use for graph, memory, governance, and licensing lifecycle management.
- Use when feature-specific metadata and policy controls are required.

## When Not to Use

- Avoid enabling strict enforcement modes before validation and staged verification.

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
Registers a relational table as a graph vertex table for a named graph.

## SQL Statement

```sql
CREATE VERTEX TABLE [IF NOT EXISTS] schema.table
FOR GRAPH graph_name
KEY key_column
[WITH (...)]
```

## Parameters

- `schema.table`: Existing table that stores vertex rows.
- `graph_name`: Existing graph namespace.
- `key_column`: Vertex identifier column.
- `WITH (...)`: Optional registration properties.

## Privileges

Requires DDL privilege on graph metadata and table metadata.

## Example

```sql
CREATE TABLE doc.users (
  id TEXT PRIMARY KEY,
  name TEXT,
  segment TEXT
);

CREATE GRAPH social;

CREATE VERTEX TABLE doc.users FOR GRAPH social KEY id;
```

## Notes

- Ensure `key_column` uniquely identifies vertices for traversal correctness.
- Registering a vertex table does not alter existing table data.

## Related

- [CREATE GRAPH](./80_CREATE_GRAPH.md)
- [CREATE EDGE TABLE](./86_CREATE_EDGE_TABLE.md)
