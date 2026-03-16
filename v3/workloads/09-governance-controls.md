# Governance, Audit, Lineage, Contracts, and Policies Workloads

This workload guide focuses on policy enforcement and governance controls with end-to-end examples.

## 1) Row filter policy workload

```sql
CREATE TABLE doc.users_rf (id INT PRIMARY KEY, tenant_id INT, email STRING) WITH (number_of_replicas = 0);
INSERT INTO doc.users_rf VALUES (1, 42, 'a@acme.com'), (2, 7, 'b@other.com');

CREATE POLICY users_rf_policy
FOR TABLE doc.users_rf
WITH (scope = 'row_filter', principal = '*', predicate = 'tenant_id = 42', precedence = 100);

GRANT DQL ON TABLE doc.users_rf TO testuser;
```

As `testuser`:

```sql
SET SESSION governance.enabled = true;
SET SESSION audit.enabled = true;
SELECT id, tenant_id, email FROM doc.users_rf ORDER BY id;
```

## 2) Column masking workload

```sql
CREATE TABLE doc.users_mask (id INT PRIMARY KEY, email STRING) WITH (number_of_replicas = 0);
INSERT INTO doc.users_mask VALUES (1, 'alpha@company.com'), (2, 'beta@company.com');

CREATE POLICY users_email_mask_policy
FOR TABLE doc.users_mask COLUMN email
WITH (scope = 'column_mask', principal = '*', masking_expression = '''***''', precedence = 100);

GRANT DQL ON TABLE doc.users_mask TO testuser;
```

As `testuser`:

```sql
SET SESSION governance.enabled = true;
SET SESSION audit.enabled = true;
SELECT id, email FROM doc.users_mask ORDER BY id;
```

## 3) Contract validation workload

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
ORDER BY started_at DESC
LIMIT 5;
```

## 4) AI usage policy workload

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

As `testuser`:

```sql
SET SESSION governance.enabled = true;

SET SESSION purpose = 'batch_reporting';
SET SESSION model_id = 'risk-model-v2';
SELECT id FROM doc.ai_users;

SET SESSION purpose = 'fraud_scoring';
SET SESSION model_id = 'risk-model-v1';
SELECT id FROM doc.ai_users;
```

## 5) Lineage workload

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

As superuser:

```sql
SELECT source_table, target_table, transform_metadata['operation']
FROM sys.lineage_edges
WHERE source_table = 'doc.l_src' AND target_table = 'doc.l_dst'
ORDER BY timestamp DESC
LIMIT 5;
```
