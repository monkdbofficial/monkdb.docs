# ALTER CONTRACT

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
ALTER CONTRACT [IF EXISTS] contract_name SET (...)
ALTER CONTRACT [IF EXISTS] contract_name BIND TO TABLE schema.table [COLUMN column_name]
ALTER CONTRACT [IF EXISTS] contract_name UNBIND
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
Updates contract properties or rebinds/unbinds contract targets.

## SQL Statement

```sql
ALTER CONTRACT [IF EXISTS] contract_name SET (...)
ALTER CONTRACT [IF EXISTS] contract_name BIND TO TABLE schema.table [COLUMN column_name]
ALTER CONTRACT [IF EXISTS] contract_name UNBIND
```

## Parameters

- `contract_name`: Existing contract identifier.
- `SET (...)`: Property updates (`version`, `severity`, `expression`, `mode`).
- `BIND TO TABLE ...`: Re-associate contract to a target.
- `UNBIND`: Remove current table/column binding.

## Privileges

Requires governance/administrative DDL privilege.

## Examples

```sql
ALTER CONTRACT users_email_format SET (mode = 'enforce', version = 2);
ALTER CONTRACT users_email_format UNBIND;
ALTER CONTRACT users_email_format BIND TO TABLE doc.users_contract COLUMN email;
```

## Notes

- Changing to `mode = 'enforce'` should follow successful `VALIDATE TABLE` runs.
- Use `IF EXISTS` for idempotent deployment scripts.

## Related

- [CREATE CONTRACT](./92_CREATE_CONTRACT.md)
- [VALIDATE TABLE](./98_VALIDATE_TABLE.md)
