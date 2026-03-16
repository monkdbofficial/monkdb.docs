# VALIDATE TABLE

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | Platform Extensions |
| Mutates Data | Yes/Depends |
| Scope | Statement |
| Privilege Model | Requires administrative or feature-specific governance/cluster privileges. |

## Purpose

Runs governance contract validation checks against table data.

## Syntax

```sql
VALIDATE TABLE schema.table
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
Runs governance contract validation against table data.

## SQL Statement

```sql
VALIDATE TABLE schema.table
```

## Parameters

- `schema.table`: Table to validate against bound contracts.

## Privileges

Requires governance/administrative privilege to run validations.

## Example

```sql
VALIDATE TABLE doc.users_contract;

SELECT run_id, table_name, status, checked_contracts, violation_count
FROM governance.validation_runs
WHERE table_name = 'doc.users_contract'
ORDER BY started_at DESC
LIMIT 5;

SELECT run_id, contract_id, severity, message, timestamp
FROM governance.contract_violations
WHERE contract_id = 'users_email_format'
ORDER BY timestamp DESC
LIMIT 10;
```

## Notes

- Run validation before switching contracts from `warn` to `enforce`.
- Keep validation in CI and scheduled production checks for drift detection.

## Related

- [CREATE CONTRACT](./92_CREATE_CONTRACT.md)
- [ALTER CONTRACT](./93_ALTER_CONTRACT.md)
