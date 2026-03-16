# ALTER MEMORY

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
ALTER MEMORY [IF EXISTS] memory_name [WITH (...)]
ALTER MEMORY [IF EXISTS] memory_name COMPACT
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
Changes memory namespace options or compacts expired entries.

## SQL Statement

```sql
ALTER MEMORY [IF EXISTS] memory_name [WITH (...)]
ALTER MEMORY [IF EXISTS] memory_name COMPACT
```

## Parameters

- `memory_name`: Existing memory namespace.
- `WITH (...)`: Option updates such as `entry_ttl_ms` and `max_entries`.
- `COMPACT`: Triggers maintenance compaction.

## Privileges

Requires DDL privilege for memory objects.

## Examples

```sql
ALTER MEMORY session_store WITH (entry_ttl_ms = 1800000, max_entries = 2000);
ALTER MEMORY session_store COMPACT;

SELECT last_compacted_at, last_compaction_pruned_entries, total_compaction_pruned_entries
FROM memory.memories
WHERE memory_name = 'session_store';
```

## Notes

- Use compaction after large write/delete bursts to reclaim stale entry overhead.
- Validate runtime behavior via `memory.memory_status`.

## Related

- [CREATE MEMORY](./89_CREATE_MEMORY.md)
- [DROP MEMORY](./91_DROP_MEMORY.md)
