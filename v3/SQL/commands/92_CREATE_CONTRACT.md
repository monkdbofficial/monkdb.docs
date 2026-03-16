# CREATE CONTRACT

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
CREATE CONTRACT [IF NOT EXISTS] contract_name
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
Defines a governance contract on a table or specific column.

## SQL Statement

```sql
CREATE CONTRACT [IF NOT EXISTS] contract_name
FOR TABLE schema.table [COLUMN column_name]
[WITH (...)]
```

## Parameters

- `contract_name`: Contract identifier.
- `schema.table`: Target table.
- `COLUMN column_name`: Optional column-level binding.
- `WITH (...)`: Contract properties such as `version`, `severity`, `expression`, `mode`.

## Privileges

Requires governance/administrative DDL privilege.

## Example

```sql
CREATE CONTRACT users_email_format
FOR TABLE doc.users_contract COLUMN email
WITH (
  version = 1,
  severity = 'high',
  expression = 'email like ''%@%''',
  mode = 'warn'
);
```

## Notes

- `expression` should be deterministic and cheap to evaluate at scale.
- Start with `mode = 'warn'` before moving to stricter enforcement modes.

## Related

- [ALTER CONTRACT](./93_ALTER_CONTRACT.md)
- [DROP CONTRACT](./94_DROP_CONTRACT.md)
- [VALIDATE TABLE](./98_VALIDATE_TABLE.md)
