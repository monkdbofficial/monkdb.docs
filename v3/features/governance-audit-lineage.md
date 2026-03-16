# Governance, Audit, Lineage

<div class="feature-tags"><span class="gh-label gh-label-release">26.3.1</span><span class="gh-label">Governance</span><span class="gh-label">Audit</span><span class="gh-label">Lineage</span><span class="gh-label">Policies</span><span class="gh-label">Contracts</span></div>

MonkDB includes governance primitives for row filtering, masking, AI usage controls, contracts, and lineage/audit sinks.

## Governance objects

- Policies (`CREATE/ALTER/DROP POLICY`)
- Contracts (`CREATE/ALTER/DROP CONTRACT`, `VALIDATE TABLE`)
- Governance tables in `governance` schema:
  - `governance.policies`
  - `governance.validation_runs`
  - `governance.contract_violations`

## Policy scopes

Supported policy `scope` values:

- `row_filter`
- `column_mask`
- `ai_usage`

Common policy properties:

- `scope`, `principal`, `precedence`
- `predicate` (row filter)
- `masking_expression` (column mask)
- `allowed_purposes`, `allowed_models`, `allowed_dataset_versions`, `max_contract_severity`, `mode`, `tenant_id` (AI usage)

## Contract properties

- `version` (>=1)
- `severity`
- `expression`
- `mode` (`off`, `warn`, `enforce`)

## Feature flags and sinks

Key dynamic settings include:

- `governance.enabled`
- `audit.enabled`, `audit.sink.*`
- `lineage.enabled`, `lineage.sink.*`
- `contracts.enforcement_mode`

## Example: row filter policy

```sql
CREATE TABLE doc.users_rf (id INT PRIMARY KEY, tenant_id INT, email STRING);
INSERT INTO doc.users_rf VALUES (1, 42, 'a@acme.com'), (2, 7, 'b@other.com');

CREATE POLICY users_rf_policy
FOR TABLE doc.users_rf
WITH (scope = 'row_filter', principal = '*', predicate = 'tenant_id = 42', precedence = 100);

GRANT DQL ON TABLE doc.users_rf TO testuser;
```

## Example: column masking policy

```sql
CREATE TABLE doc.users_mask (id INT PRIMARY KEY, email STRING);
INSERT INTO doc.users_mask VALUES (1, 'alpha@company.com'), (2, 'beta@company.com');

CREATE POLICY users_email_mask_policy
FOR TABLE doc.users_mask COLUMN email
WITH (scope = 'column_mask', principal = '*', masking_expression = '''***''', precedence = 100);
```

## Example: contract + validation

```sql
CREATE TABLE doc.users_contract (id INT PRIMARY KEY, email STRING);
INSERT INTO doc.users_contract VALUES (1, 'ok@x.com'), (2, 'invalid_email');

CREATE CONTRACT users_email_format
FOR TABLE doc.users_contract COLUMN email
WITH (version = 1, severity = 'high', expression = 'email like ''%@%''', mode = 'warn');

VALIDATE TABLE doc.users_contract;
```

## Example: AI usage policy

```sql
CREATE POLICY ai_usage_enforce_policy
FOR TABLE doc.ai_users
WITH (
  scope = 'ai_usage',
  principal = '*',
  allowed_purposes = 'fraud_scoring',
  allowed_models = 'risk-model-v1',
  max_contract_severity = 'medium',
  mode = 'enforce',
  precedence = 100
);
```

## Audit and lineage observability

Useful system views/tables:

- `sys.policy_audit_sink_metrics`
- `sys.governance_contract_metrics`
- `sys.lineage_jobs`, `sys.lineage_edges`, `sys.lineage_sink_metrics`

## Implementation status note

Current governance implementation includes persisted metadata, policy decisioning, and sink telemetry paths. Contract evaluation and full write-path enforcement continue to evolve; validate behavior in your target release before enforcing strict production gates.
