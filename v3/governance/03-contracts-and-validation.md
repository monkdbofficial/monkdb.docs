# Contracts and Validation

Contracts formalize data-quality and policy constraints on tables/columns. They can run in advisory mode (`warn`) or blocking mode (`enforce`) depending on rollout phase.

## Contract model

A contract typically includes:

- `expression`: boolean rule to validate.
- `severity`: business impact level (`low`, `medium`, `high`).
- `mode`: enforcement behavior (`warn` or `enforce`).
- `version`: controlled rollout/versioning signal.

## Core SQL pattern

```sql
CREATE CONTRACT <contract_name>
FOR TABLE <schema.table> COLUMN <column_name>
WITH (
  version = <integer>,
  severity = '<low|medium|high>',
  expression = '<boolean expression>',
  mode = '<warn|enforce>'
);
```

## End-to-end example

### Session A (admin/superuser): setup

```sql
DROP CONTRACT IF EXISTS users_email_format;
DROP CONTRACT IF EXISTS users_region_whitelist;
DROP TABLE IF EXISTS doc.users_contract;

CREATE TABLE doc.users_contract (
  id INT PRIMARY KEY,
  email STRING,
  region STRING
) WITH (number_of_replicas = 0);

INSERT INTO doc.users_contract (id, email, region) VALUES
  (1, 'ok@x.com', 'apac'),
  (2, 'invalid_email', 'na'),
  (3, 'ops@x.com', 'invalid_region');

CREATE CONTRACT users_email_format
FOR TABLE doc.users_contract COLUMN email
WITH (
  version = 1,
  severity = 'high',
  expression = 'email like ''%@%''',
  mode = 'warn'
);

CREATE CONTRACT users_region_whitelist
FOR TABLE doc.users_contract COLUMN region
WITH (
  version = 1,
  severity = 'medium',
  expression = 'region in (''apac'', ''emea'', ''na'')',
  mode = 'warn'
);
```

## Validate and inspect

```sql
VALIDATE TABLE doc.users_contract;

SELECT run_id, table_name, status, checked_contracts, violation_count
FROM governance.validation_runs
WHERE table_name = 'doc.users_contract'
ORDER BY started_at DESC
LIMIT 5;

SELECT run_id, contract_id, severity, message, timestamp
FROM governance.contract_violations
WHERE contract_id IN ('users_email_format', 'users_region_whitelist')
ORDER BY timestamp DESC
LIMIT 20;
```

## Promote from warn to enforce

Recommended rollout:

1. Start in `warn` mode.
2. Observe violations for at least one full workload cycle.
3. Remediate producers/ETL.
4. Promote to `enforce`.

```sql
ALTER CONTRACT users_email_format SET (mode = 'enforce', version = 2);
```

## Contract lifecycle operations

```sql
ALTER CONTRACT users_email_format SET (severity = 'high', version = 3);
ALTER CONTRACT users_email_format UNBIND;
ALTER CONTRACT users_email_format BIND TO TABLE doc.users_contract COLUMN email;
DROP CONTRACT users_region_whitelist;
```

## Observability and SLO checks

```sql
SELECT pass_count,
       fail_count,
       warn_count,
       reject_count,
       validation_runs,
       validation_latency_avg_ms,
       validation_latency_max_ms,
       warn_rate,
       reject_rate
FROM sys.governance_contract_metrics
LIMIT 1;
```

## Common mistakes

- Contracts never trigger:
  - wrong table/column binding.
  - no validation execution path.
- Excessive rejects after promotion:
  - contract moved to `enforce` before producer cleanup.
- High validation latency:
  - validating large tables without schedule windows.

## Operational guidance

- Use severity consistently to map business impact.
- Keep expressions explicit and testable in standalone SELECT checks.
- Version contracts on every semantic change for auditability.
