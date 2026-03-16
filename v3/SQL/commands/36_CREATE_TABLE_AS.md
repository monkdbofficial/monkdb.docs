# CREATE TABLE AS

> Enterprise command reference.

## Command Snapshot

| Field | Value |
| --- | --- |
| Category | DDL and Administration |
| Mutates Data | Yes/Depends |
| Scope | Cluster / Object |
| Privilege Model | Requires DDL/administrative privilege according to target object scope. |

## Purpose

Defines, changes, or removes schema and metadata objects.

## Syntax

```sql
CREATE TABLE [ IF NOT EXISTS ] table_ident AS { ( query ) | query }
```

## Operational Notes

- Use schema-qualified identifiers in automation and automation pipelines.
- Validate behavior in staging for cluster-impacting or governance-impacting changes.
- Confirm runtime effects through system tables and metrics before and after execution.

## When to Use

- Use during planned schema and runtime administration changes.
- Use in automation pipelines with environment-specific validation and rollback strategy.

## When Not to Use

- Avoid during incident windows unless the command is part of approved mitigation.
- Avoid schema changes in peak traffic windows without staged rollout.

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
# CREATE TABLE AS

The `CREATE TABLE AS` statement is used to create a new table based on the results of a query. This allows you to define a table structure and populate it with data derived from existing tables.

---

## SQL Statement

```sql
CREATE TABLE [ IF NOT EXISTS ] table_ident AS { ( query ) | query }
```

---

## Description

The `CREATE TABLE AS` statement creates a new table and inserts rows based on the results of a specified query.

### Key Features:
- **Dynamic Table Creation:** The table's structure (column names and types) is derived from the query results.
- **Data Population:** Rows returned by the query are inserted into the newly created table.
- **Default Table Parameters:** Optional parameters for table creation (e.g., sharding, replication) are assigned default values unless explicitly specified.

### Limitations:
- If the `IF NOT EXISTS` clause is used and the table already exists, the statement does nothing, and no rows are inserted.
- System tables and foreign tables cannot be used as part of the query.

---

## Clauses

### **IF NOT EXISTS**
Prevents errors if the table already exists. If the table exists, no action is taken, and 0 rows are returned.

---

## Parameters

| Parameter        | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| **table_ident**   | The name (optionally schema-qualified) of the new table to be created.     |
| **query**         | A `SELECT` statement that defines the rows to insert into the new table.   |

---

## Examples

### Example 1: Create a Table from a Query
Create a new table named `active_users` based on data from an existing `users` table:

```sql
CREATE TABLE active_users AS
SELECT id, name, last_login
FROM users
WHERE last_login > CURRENT_DATE - INTERVAL '30 days';
```

This creates an `active_users` table with columns `id`, `name`, and `last_login`, populated with rows from the `users` table where users logged in within the last 30 days.

---

### Example 2: Create a Table if It Does Not Exist
Create a new table named `recent_orders` only if it does not already exist:

```sql
CREATE TABLE IF NOT EXISTS recent_orders AS
SELECT order_id, customer_id, order_date
FROM orders
WHERE order_date > CURRENT_DATE - INTERVAL '7 days';
```

If the `recent_orders` table already exists, no action is taken.

---

### Example 3: Create a Table Using Aggregated Data
Create a new table named `sales_summary` that holds aggregated sales data:

```sql
CREATE TABLE sales_summary AS
SELECT product_id, SUM(quantity) AS total_quantity, AVG(price) AS average_price
FROM sales
GROUP BY product_id;
```

This creates a `sales_summary` table with columns `product_id`, `total_quantity`, and `average_price`.

---

### Example 4: Create a Table with Schema Qualification
Create a new table in a specific schema:

```sql
CREATE TABLE analytics.top_customers AS
SELECT customer_id, SUM(total_spent) AS total_spent
FROM transactions
GROUP BY customer_id
ORDER BY total_spent DESC LIMIT 10;
```

This creates the `top_customers` table within the `analytics` schema.

---

## Notes

1. **Default Parameters:** The newly created table will use default settings for optional parameters like sharding and replication unless explicitly configured using additional clauses.
2. **Data Consistency:** The snapshot of data captured by the query reflects its state at the time of execution. Subsequent changes to source tables will not affect the new table.
3. **Performance Considerations:** Large queries may impact cluster performance during execution. Use filters or limits to reduce query size when necessary.
4. **Schema Qualification:** If creating tables within specific schemas, ensure proper schema permissions are granted.

---

##  Permissions

- **Creating the Target Table**:
  - Requires `CREATE` privilege on the target schema where the new table will be created.

- **Query Source Access**:
  - Requires `DQL` (Data Query Language) privileges on all source tables used in the query.

- **Schema Qualification**:
  - If a specific schema is referenced, the user must have appropriate access to that schema.

>  Note: While the `CREATE TABLE AS` operation uses results from a query, it does not automatically grant any additional privileges on the new table to others—explicit `GRANT` statements must follow if shared access is needed.

---

##  Summary

| Feature                        | Supported / Required                                               |
|--------------------------------|--------------------------------------------------------------------|
| Creates New Table              | Yes Yes                                                             |
| Populates Data from Query      | Yes Yes                                                             |
| Schema Inference from Query    | Yes Yes (column names and types from `SELECT`)                     |
| IF NOT EXISTS Support          | Yes Yes                                                             |
| Supports Aggregations/Subqueries | Yes Yes                                                          |
| Data Snapshot at Execution     | Yes One-time snapshot, no sync with source                          |
| Requires CREATE Privilege      | Yes On target schema                                                |
| Requires DQL Privilege         | Yes On all source tables in the query                               |
| Additional Clauses (e.g., WITH, CLUSTERED) | No Not currently supported — defaults are applied            |

---

## See Also

- [Create Table](./35_CREATE_TABLE.md)
- [Alter Table](./17_ALTER_TABLE.md)

