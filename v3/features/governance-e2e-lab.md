# Governance E2E Lab Script

<div class="feature-tags"><span class="gh-label gh-label-release">26.3.1</span><span class="gh-label">Governance</span><span class="gh-label">E2E Lab</span></div>

This page provides an end-to-end governance/audit/lineage validation script for local test clusters.

## 0) Preflight (superuser)

```sql
SELECT current_user;
SELECT name, superuser FROM sys.users WHERE name IN ('monkdb', 'testuser');

REVOKE ALL FROM testuser;

DROP POLICY IF EXISTS users_rf_policy;
DROP POLICY IF EXISTS users_email_mask_policy;
DROP POLICY IF EXISTS ai_usage_enforce_policy;

DROP CONTRACT IF EXISTS users_email_format;
DROP CONTRACT IF EXISTS ai_users_enforce_contract;

DROP TABLE IF EXISTS doc.users_rf;
DROP TABLE IF EXISTS doc.users_mask;
DROP TABLE IF EXISTS doc.users_contract;
DROP TABLE IF EXISTS doc.ai_users;
DROP TABLE IF EXISTS doc.l_src;
DROP TABLE IF EXISTS doc.l_dst;
DROP TABLE IF EXISTS doc.governance_visible;
DROP TABLE IF EXISTS doc.governance_hidden;
DROP TABLE IF EXISTS doc.lineage_jobs_store_e2e;
DROP TABLE IF EXISTS doc.lineage_edges_store_e2e;
DROP TABLE IF EXISTS doc.policy_audit_events_e2e;
```

Enable sinks/settings:

```sql
SET GLOBAL TRANSIENT
  audit.enabled = true,
  "audit.sink.mode" = 'sync',
  "audit.sink.index.enabled" = true,
  "audit.sink.index.name" = 'policy_audit_events_e2e',
  "audit.sink.index.shards" = 1,
  "audit.sink.index.replicas" = '0',
  lineage.enabled = true,
  lineage.sink.mode = 'async',
  "lineage.sink.index.enabled" = true,
  "lineage.sink.index.jobs_table" = 'doc.lineage_jobs_store_e2e',
  "lineage.sink.index.edges_table" = 'doc.lineage_edges_store_e2e',
  "lineage.sink.index.shards" = 1,
  "lineage.sink.index.replicas" = '0',
  "lineage.sink.index.partition_by" = 'day';
```

## A) Row filter policy

```sql
CREATE TABLE doc.users_rf (id INT PRIMARY KEY, tenant_id INT, email STRING) WITH (number_of_replicas = 0);
INSERT INTO doc.users_rf VALUES (1, 42, 'a@acme.com'), (2, 7, 'b@other.com');

CREATE POLICY users_rf_policy
FOR TABLE doc.users_rf
WITH (scope = 'row_filter', principal = '*', predicate = 'tenant_id = 42', precedence = 100);

GRANT DQL ON TABLE doc.users_rf TO testuser;
```

## B) Column masking policy

```sql
CREATE TABLE doc.users_mask (id INT PRIMARY KEY, email STRING) WITH (number_of_replicas = 0);
INSERT INTO doc.users_mask VALUES (1, 'alpha@company.com'), (2, 'beta@company.com');

CREATE POLICY users_email_mask_policy
FOR TABLE doc.users_mask COLUMN email
WITH (scope = 'column_mask', principal = '*', masking_expression = '''***''', precedence = 100);

GRANT DQL ON TABLE doc.users_mask TO testuser;
```

## C) Contract validation

```sql
CREATE TABLE doc.users_contract (id INT PRIMARY KEY, email STRING) WITH (number_of_replicas = 0);
INSERT INTO doc.users_contract VALUES (1, 'ok@x.com'), (2, 'invalid_email');

CREATE CONTRACT users_email_format
FOR TABLE doc.users_contract COLUMN email
WITH (version = 1, severity = 'high', expression = 'email like ''%@%''', mode = 'warn');

VALIDATE TABLE doc.users_contract;

SELECT run_id, table_name, status, checked_contracts, violation_count
FROM governance.validation_runs
WHERE table_name = 'doc.users_contract'
ORDER BY started_at DESC LIMIT 5;
```

## D) AI usage policy

```sql
CREATE TABLE doc.ai_users (id INT PRIMARY KEY, email STRING) WITH (number_of_replicas = 0);
INSERT INTO doc.ai_users VALUES (1, 'a@x');
REFRESH TABLE doc.ai_users;

CREATE CONTRACT ai_users_enforce_contract
FOR TABLE doc.ai_users COLUMN email
WITH (version = 1, severity = 'high', expression = 'email like ''%@%''', mode = 'warn');

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

## E) Lineage end-to-end

```sql
CREATE TABLE doc.l_src (id INT PRIMARY KEY) WITH (number_of_replicas = 0);
CREATE TABLE doc.l_dst (id INT PRIMARY KEY) WITH (number_of_replicas = 0);

GRANT DQL, DML ON TABLE doc.l_src TO testuser;
GRANT DQL, DML ON TABLE doc.l_dst TO testuser;
```

As `testuser`:

```sql
SET SESSION lineage.enabled = true;
SET SESSION pipeline_id = 'pipeline-ctx';
SET SESSION model_id = 'model-ctx';
SET SESSION dataset_version = 'v-ctx';
SET SESSION purpose = 'fraud_scoring';
SET SESSION trace_id = 'trace-ctx';

INSERT INTO doc.l_src (id) VALUES (1), (2);
INSERT INTO doc.l_dst (id) SELECT id FROM doc.l_src;
```

## F) Governance tag visibility

```sql
CREATE TABLE doc.governance_visible (
  id INT PRIMARY KEY,
  email STRING
) WITH (
  number_of_replicas = 0,
  "tags.domain" = 'customer',
  "column_tags.email.sensitivity" = 'pii'
);

CREATE TABLE doc.governance_hidden (
  id INT PRIMARY KEY,
  email STRING
) WITH (
  number_of_replicas = 0,
  "tags.domain" = 'internal',
  "column_tags.email.sensitivity" = 'secret'
);

GRANT DQL ON TABLE doc.governance_visible TO testuser;
```

As `testuser`, inspect:

```sql
SELECT table_name, tag_name, tag_value
FROM information_schema.table_tags
WHERE table_schema = 'doc' AND table_name LIKE 'governance_%'
ORDER BY table_name, tag_name;

SELECT table_name, column_name, tag_name, tag_value
FROM information_schema.column_tags
WHERE table_schema = 'doc' AND table_name LIKE 'governance_%'
ORDER BY table_name, column_name, tag_name;
```
