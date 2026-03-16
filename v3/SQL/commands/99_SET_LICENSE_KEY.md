# SET LICENSE KEY

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | Platform Extensions |
| Mutates Data | Yes/Depends |
| Scope | Cluster / Object |
| Privilege Model | Requires administrative or feature-specific governance/cluster privileges. |

## Purpose

Applies cluster license state used for feature and node-limit enforcement.

## Syntax

```sql
SET LICENSE KEY 'MONK1....'
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
Applies or replaces the active cluster license token.

## SQL Statement

```sql
SET LICENSE KEY 'MONK1....'
```

## Parameters

- String literal license token.

## Privileges

Requires administrative privilege.

## Example

```sql
SET LICENSE KEY 'MONK1....';

SELECT
  "license"['status'],
  "license"['valid'],
  "license"['allowed_nodes'],
  "license"['current_nodes'],
  "license"['error']
FROM sys.cluster;
```

## 3-Node Workflow Check

```sql
SELECT id, master_node FROM sys.cluster;
SELECT id, name FROM sys.nodes ORDER BY name;
```

Apply the license, add nodes, then re-check `allowed_nodes` and `current_nodes`.

## Notes

- Apply licensing before scaling above default node limits.
- Keep token rotation and expiry checks in operational runbooks.

## Related

- [License Management](../../features/licensing.md)
- [SQL Command Catalog](../08-command-catalog.md)
