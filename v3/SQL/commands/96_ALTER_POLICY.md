# ALTER POLICY

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
ALTER POLICY [IF EXISTS] policy_name SET (...)
ALTER POLICY [IF EXISTS] policy_name BIND TO TABLE schema.table [COLUMN column_name]
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
Updates policy properties or rebinds a policy target.

## SQL Statement

```sql
ALTER POLICY [IF EXISTS] policy_name SET (...)
ALTER POLICY [IF EXISTS] policy_name BIND TO TABLE schema.table [COLUMN column_name]
```

## Parameters

- `policy_name`: Existing policy identifier.
- `SET (...)`: Property updates (for example `precedence`, `mode`, `allowed_models`).
- `BIND TO TABLE ...`: Re-associate policy target.

## Privileges

Requires governance/administrative DDL privilege.

## Examples

```sql
ALTER POLICY ai_usage_enforce_policy SET (
  allowed_models = 'risk-model-v2',
  precedence = 120
);

ALTER POLICY users_email_mask_policy BIND TO TABLE doc.users_mask COLUMN email;
```

## Notes

- Use controlled rollouts for mode/precedence changes.
- Validate outcomes through audit and governance metric tables.

## Related

- [CREATE POLICY](./95_CREATE_POLICY.md)
- [DROP POLICY](./97_DROP_POLICY.md)
