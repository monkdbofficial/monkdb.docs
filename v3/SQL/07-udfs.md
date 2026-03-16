# User-Defined Functions (UDFs)

MonkDB supports SQL-callable UDFs via `CREATE FUNCTION`.

## Lifecycle

### Create

```sql
CREATE FUNCTION doc.my_add(a INTEGER, b INTEGER)
RETURNS INTEGER
LANGUAGE JAVASCRIPT
AS 'function(a, b) { return a + b; }';
```

### Execute

```sql
SELECT doc.my_add(2, 3);
```

### Replace

```sql
CREATE OR REPLACE FUNCTION doc.my_add(a INTEGER, b INTEGER)
RETURNS INTEGER
LANGUAGE JAVASCRIPT
AS 'function(a, b) { return a + b + 1; }';
```

### Drop

```sql
DROP FUNCTION IF EXISTS doc.my_add(INTEGER, INTEGER);
```

## Operational guidance

- Keep logic deterministic and side-effect free for predictable planning.
- Avoid heavyweight CPU loops in hot query paths.
- Version UDF names/signatures deliberately for safer rollout.
- Track execution patterns through `sys.jobs`/`sys.jobs_log` statements.
