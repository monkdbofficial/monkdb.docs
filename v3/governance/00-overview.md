# Governance Overview

MonkDB governance controls combine policies, contracts, audit, lineage, and tagging controls to enforce and observe data usage.

## Building blocks

- Policies
  - Row filtering
  - Column masking
  - AI usage control
- Contracts
  - Data quality/business rule assertions
  - Warn/enforce modes
- Audit
  - Policy decision events
  - Sink metrics and persistent stores
- Lineage
  - Job and edge capture
  - Projected sink tables
- Metadata tags
  - Table and column tags with visibility controls

## Typical rollout order

1. Enable audit and lineage sinks.
2. Create baseline policies for row-level separation and masking.
3. Add contracts in `warn` mode and validate.
4. Promote selected contracts/policies to enforce mode.
5. Monitor sink metrics and violations continuously.

## Core SQL objects

- `CREATE POLICY`, `ALTER POLICY`, `DROP POLICY`
- `CREATE CONTRACT`, `ALTER CONTRACT`, `DROP CONTRACT`
- `VALIDATE TABLE`

## Deep-dive pages

- [Row Filter Policies](./01-row-filter-policies.md)
- [Column Masking Policies](./02-column-masking-policies.md)
- [Contracts and Validation](./03-contracts-and-validation.md)
- [Audit Operations](./04-audit-operations.md)
- [Lineage Operations](./05-lineage-operations.md)
- [AI Usage Policies](./06-ai-usage-policies.md)
