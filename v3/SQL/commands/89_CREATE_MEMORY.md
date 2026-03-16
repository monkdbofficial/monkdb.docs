# CREATE MEMORY

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
CREATE MEMORY [IF NOT EXISTS] memory_name [WITH (...)]
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
Creates a memory namespace for short-lived key/value state.

## SQL Statement

```sql
CREATE MEMORY [IF NOT EXISTS] memory_name [WITH (...)]
```

## Parameters

- `memory_name`: Memory namespace identifier.
- `WITH (...)`: Common options include `strict`, `entry_ttl_ms`, and `max_entries`.

## Privileges

Requires DDL privilege for memory objects.

## Example

```sql
CREATE MEMORY session_store
WITH (strict = true, entry_ttl_ms = 3600000, max_entries = 1000);

SELECT memory_name, options['strict'], options['entry_ttl_ms'], options['max_entries']
FROM memory.memories
WHERE memory_name = 'session_store';
```

## Notes

- Use `strict = true` for bounded-write behavior under capacity constraints.
- Query and mutate entries through `memory.memory_entries`.

## Related

- [ALTER MEMORY](./90_ALTER_MEMORY.md)
- [DROP MEMORY](./91_DROP_MEMORY.md)
- [Memory Feature Guide](../../features/memory.md)
