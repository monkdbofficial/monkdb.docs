# Row Filter Policies

Row filter policies constrain row visibility at query time. They are the primary control for multi-tenant isolation, data-domain segmentation, and scoped analyst access.

## How row filtering works

At planning/execution time, MonkDB evaluates active `row_filter` policies for the table and principal, then enforces the effective predicate.

Key points:

- `scope = 'row_filter'` applies predicate-based row visibility controls.
- `principal` can target a user, role, or `*`.
- `precedence` resolves conflicts; higher precedence wins when policies overlap.
- Policy enforcement depends on governance controls being enabled for the session/cluster.

## Core SQL pattern

```sql
CREATE POLICY <policy_name>
FOR TABLE <schema.table>
WITH (
  scope = 'row_filter',
  principal = '<user|role|*>',
  predicate = '<boolean expression>',
  precedence = <integer>
);
```

## End-to-end example

### Session A (admin/superuser): setup

```sql
DROP POLICY IF EXISTS users_rf_policy;
DROP TABLE IF EXISTS doc.users_rf;

CREATE TABLE doc.users_rf (
  id INT PRIMARY KEY,
  tenant_id INT,
  region STRING,
  email STRING
) WITH (number_of_replicas = 0);

INSERT INTO doc.users_rf (id, tenant_id, region, email) VALUES
  (1, 42, 'apac', 'a@acme.com'),
  (2, 42, 'emea', 'b@acme.com'),
  (3, 7,  'apac', 'c@other.com');

CREATE POLICY users_rf_policy
FOR TABLE doc.users_rf
WITH (
  scope = 'row_filter',
  principal = '*',
  predicate = 'tenant_id = 42',
  precedence = 100
);

GRANT DQL ON TABLE doc.users_rf TO testuser;
```

### Session B (`testuser`): enforce + query

```sql
SET SESSION governance.enabled = true;
SET SESSION audit.enabled = true;

SELECT id, tenant_id, region, email
FROM doc.users_rf
ORDER BY id;
```

Expected result: only rows with `tenant_id = 42` are visible.

## Precedence example

Use precedence for stricter scoped policies:

```sql
CREATE POLICY users_rf_apac
FOR TABLE doc.users_rf
WITH (
  scope = 'row_filter',
  principal = 'testuser',
  predicate = 'tenant_id = 42 AND region = ''apac''',
  precedence = 200
);
```

With this policy, `testuser` only sees APAC rows for tenant 42.

## Verification and observability

```sql
SELECT mode, queue_depth, index_enabled
FROM sys.policy_audit_sink_metrics
LIMIT 1;

REFRESH TABLE doc.policy_audit_events_e2e;

SELECT policy_id, scope, outcome, subject, resource, reason
FROM doc.policy_audit_events_e2e
WHERE policy_id IN ('users_rf_policy', 'users_rf_apac')
ORDER BY timestamp DESC
LIMIT 20;
```

## Troubleshooting

- All rows returned:
  - Confirm `SET SESSION governance.enabled = true`.
  - Confirm policy principal matches the executing user/role.
- Zero rows returned:
  - Check predicate correctness against actual data.
  - Check whether a higher-precedence restrictive policy is active.
- Query fails with policy errors:
  - Validate policy expression syntax and referenced columns.

## Operational guidance

- Start with broad allow predicates in staging and tighten iteratively.
- Keep predicates deterministic and index-friendly where possible.
- Use explicit precedence conventions (for example: 100 baseline, 200 strict overrides).
