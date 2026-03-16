# CREATE GRAPH

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
CREATE GRAPH [IF NOT EXISTS] graph_name [WITH (...)]
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
Creates a graph namespace used by `CREATE VERTEX TABLE` and `CREATE EDGE TABLE` metadata bindings.

## SQL Statement

```sql
CREATE GRAPH [IF NOT EXISTS] graph_name [WITH (...)]
```

## Parameters

- `graph_name`: Logical graph identifier.
- `WITH (...)`: Optional graph properties (implementation-specific).

## Privileges

Requires administrative DDL privilege.

## Example

```sql
CREATE GRAPH social;

SELECT *
FROM graph.graphs
WHERE name = 'social';
```

## Notes

- Create the graph before registering vertex and edge tables.
- Graph metadata does not create base data tables automatically; create table storage first.

## Related

- [CREATE VERTEX TABLE](./83_CREATE_VERTEX_TABLE.md)
- [CREATE EDGE TABLE](./86_CREATE_EDGE_TABLE.md)
- [SQL Command Catalog](../08-command-catalog.md)
