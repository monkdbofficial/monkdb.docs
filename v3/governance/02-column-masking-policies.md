# Column Masking Policies

Column masking policies hide or transform sensitive fields while preserving row-level access to non-sensitive data.

Typical use cases:

- PII redaction in analytics queries.
- Tiered access to customer/contact data.
- Safe default access for broad analyst roles.

## How masking works

Masking policies are evaluated per selected column. The masking expression is returned instead of the original value when policy conditions match.

Key options:

- `scope = 'column_mask'`
- `principal = '<user|role|*>'`
- `masking_expression = '<sql expression>'`
- `precedence = <integer>`

## Core SQL pattern

```sql
CREATE POLICY <policy_name>
FOR TABLE <schema.table> COLUMN <column_name>
WITH (
  scope = 'column_mask',
  principal = '<user|role|*>',
  masking_expression = '<expression>',
  precedence = <integer>
);
```

## End-to-end example

### Session A (admin/superuser): setup

```sql
DROP POLICY IF EXISTS users_email_mask_policy;
DROP POLICY IF EXISTS users_phone_mask_policy;
DROP TABLE IF EXISTS doc.users_mask;

CREATE TABLE doc.users_mask (
  id INT PRIMARY KEY,
  tenant_id INT,
  email STRING,
  phone STRING
) WITH (number_of_replicas = 0);

INSERT INTO doc.users_mask (id, tenant_id, email, phone) VALUES
  (1, 42, 'alpha@company.com', '+1-555-1010'),
  (2, 42, 'beta@company.com',  '+1-555-2020');

CREATE POLICY users_email_mask_policy
FOR TABLE doc.users_mask COLUMN email
WITH (
  scope = 'column_mask',
  principal = '*',
  masking_expression = '''***''',
  precedence = 100
);

CREATE POLICY users_phone_mask_policy
FOR TABLE doc.users_mask COLUMN phone
WITH (
  scope = 'column_mask',
  principal = '*',
  masking_expression = '''REDACTED''',
  precedence = 100
);

GRANT DQL ON TABLE doc.users_mask TO testuser;
```

### Session B (`testuser`): enforce + query

```sql
SET SESSION governance.enabled = true;
SET SESSION audit.enabled = true;

SELECT id, tenant_id, email, phone
FROM doc.users_mask
ORDER BY id;
```

Expected result:

- `email` returns `***`
- `phone` returns `REDACTED`
- non-protected columns (for example `id`, `tenant_id`) are unchanged

## Conditional masking pattern

You can create stricter masks for broader principals and narrower masks for privileged principals with precedence control.

```sql
CREATE POLICY users_email_mask_strict
FOR TABLE doc.users_mask COLUMN email
WITH (
  scope = 'column_mask',
  principal = '*',
  masking_expression = '''MASKED''',
  precedence = 50
);
```

Use a higher-precedence policy for privileged principals when needed.

## Verification and observability

```sql
REFRESH TABLE doc.policy_audit_events_e2e;

SELECT policy_id, scope, outcome, resource, reason
FROM doc.policy_audit_events_e2e
WHERE policy_id LIKE 'users_%_mask_%'
ORDER BY timestamp DESC
LIMIT 20;
```

## Common mistakes

- Masking appears not applied:
  - governance not enabled in session.
  - policy principal does not match user/role.
- Unexpected masked output type:
  - masking expression type does not align with selected column usage.
- Conflicting behavior:
  - overlapping policies with unclear precedence.

## Operational guidance

- Prefer deterministic masking expressions.
- Standardize mask strings by data class (`PII`, `SECRET`, `TOKEN`).
- Test BI/report compatibility when masked columns participate in downstream transformations.
