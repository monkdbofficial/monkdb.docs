# CREATE POLICY

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
CREATE POLICY [IF NOT EXISTS] policy_name
FOR TABLE schema.table [COLUMN column_name]
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
Creates a governance policy for row filtering, column masking, or AI usage control.

## SQL Statement

```sql
CREATE POLICY [IF NOT EXISTS] policy_name
FOR TABLE schema.table [COLUMN column_name]
[WITH (...)]
```

## Parameters

- `policy_name`: Policy identifier.
- `schema.table`: Target table.
- `COLUMN column_name`: Required for column-scoped policies.
- `WITH (...)`: Policy properties such as `scope`, `principal`, `predicate`, `masking_expression`, `allowed_purposes`, `allowed_models`, `mode`, `precedence`.

## Privileges

Requires governance/administrative DDL privilege.

## Examples

```sql
CREATE POLICY users_rf_policy
FOR TABLE doc.users_rf
WITH (
  scope = 'row_filter',
  principal = '*',
  predicate = 'tenant_id = 42',
  precedence = 100
);

CREATE POLICY users_email_mask_policy
FOR TABLE doc.users_mask COLUMN email
WITH (
  scope = 'column_mask',
  principal = '*',
  masking_expression = '''***''',
  precedence = 100
);
```

## Notes

- Use explicit `scope` values (`row_filter`, `column_mask`, `ai_usage`).
- Keep precedence conventions stable to avoid ambiguous policy outcomes.

## Related

- [ALTER POLICY](./96_ALTER_POLICY.md)
- [DROP POLICY](./97_DROP_POLICY.md)
- [Governance, Audit, Lineage](../../features/governance-audit-lineage.md)
