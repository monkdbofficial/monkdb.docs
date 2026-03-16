# AI Usage Policies

AI usage policies restrict AI-context query execution using purpose, model, and contract-severity gates.

Typical use cases:

- Allow only approved model IDs for sensitive data domains.
- Restrict purpose to approved business intents (`fraud_scoring`, `risk_assessment`, etc.).
- Block AI usage when contract severity exceeds policy limits.

## How AI usage policies work

At execution time, MonkDB evaluates:

- session context (`purpose`, `model_id`)
- policy scope (`scope = 'ai_usage'`)
- allowed purpose/model lists
- contract envelope (`max_contract_severity`)
- policy mode (`warn` or `enforce`)

If policy mode is `enforce`, non-compliant contexts are denied.

## Core SQL pattern

```sql
CREATE POLICY <policy_name>
FOR TABLE <schema.table>
WITH (
  scope = 'ai_usage',
  principal = '<user|role|*>',
  allowed_purposes = '<comma-separated list>',
  allowed_models = '<comma-separated list>',
  max_contract_severity = '<low|medium|high>',
  mode = '<warn|enforce>',
  precedence = <integer>
);
```

## End-to-end example

### Session A (admin/superuser): setup

```sql
DROP POLICY IF EXISTS ai_usage_enforce_policy;
DROP CONTRACT IF EXISTS ai_users_enforce_contract;
DROP TABLE IF EXISTS doc.ai_users;

CREATE TABLE doc.ai_users (
  id INT PRIMARY KEY,
  email STRING,
  risk_score DOUBLE
) WITH (number_of_replicas = 0);

INSERT INTO doc.ai_users (id, email, risk_score) VALUES
  (1, 'alpha@x.com', 0.82),
  (2, 'beta@x.com',  0.41);

REFRESH TABLE doc.ai_users;

CREATE CONTRACT ai_users_enforce_contract
FOR TABLE doc.ai_users COLUMN email
WITH (
  version = 1,
  severity = 'high',
  expression = 'email like ''%@%''',
  mode = 'warn'
);

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

GRANT DQL ON TABLE doc.ai_users TO testuser;
```

### Session B (`testuser`): deny and allow checks

```sql
SET SESSION governance.enabled = true;

-- denied: purpose/model do not match policy allow-list
SET SESSION purpose = 'batch_reporting';
SET SESSION model_id = 'risk-model-v2';
SELECT id, risk_score FROM doc.ai_users;

-- allowed: purpose/model match policy allow-list
SET SESSION purpose = 'fraud_scoring';
SET SESSION model_id = 'risk-model-v1';
SELECT id, risk_score FROM doc.ai_users ORDER BY id;
```

## Decision matrix

| Purpose | Model | Expected Outcome |
| --- | --- | --- |
| `batch_reporting` | `risk-model-v2` | Denied in `enforce` mode |
| `fraud_scoring` | `risk-model-v2` | Denied (model mismatch) |
| `batch_reporting` | `risk-model-v1` | Denied (purpose mismatch) |
| `fraud_scoring` | `risk-model-v1` | Allowed |

## Contract severity interaction

`max_contract_severity` acts as a policy envelope:

- If policy allows up to `medium`, high-severity contract posture can trigger deny behavior in enforced contexts.
- Align contract severities and AI policy envelopes before production enablement.

## Observability and metrics

```sql
SELECT policy_decisions_total,
       policy_warned_count,
       policy_denied_count,
       policy_warn_rate,
       policy_deny_rate
FROM sys.governance_contract_metrics
LIMIT 1;
```

Audit verification (if audit sink is enabled):

```sql
REFRESH TABLE doc.policy_audit_events_e2e;

SELECT policy_id, scope, outcome, subject, resource, reason
FROM doc.policy_audit_events_e2e
WHERE policy_id = 'ai_usage_enforce_policy'
ORDER BY timestamp DESC
LIMIT 20;
```

## Troubleshooting

- Policy not applied:
  - confirm `SET SESSION governance.enabled = true`.
  - confirm user/role matches policy `principal`.
- Unexpected deny:
  - verify exact `purpose` and `model_id` session values.
  - validate contract severity envelope against `max_contract_severity`.
- No metrics movement:
  - ensure governed queries are actually executed on policy-bound tables.

## Rollout guidance

1. Start policy in `warn` mode to measure real traffic impact.
2. Observe deny/warn rates in `sys.governance_contract_metrics`.
3. Fix client context propagation (`purpose`, `model_id`) and model allow-lists.
4. Promote to `enforce` mode after stable baseline.
