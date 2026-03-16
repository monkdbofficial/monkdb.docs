# SQL Constraints

This page defines table and column constraints referenced by command pages.

## Constraint Types

- `PRIMARY KEY`: Enforces row uniqueness for one or more columns.
- `NOT NULL`: Prevents null values in a column.
- `CHECK`: Enforces a boolean condition at write time.
- `INDEX` clauses in DDL: Control indexing behavior for query performance.

## CHECK

`CHECK` constraints enforce boolean predicates at write time. Rows that do not
satisfy the predicate are rejected for `INSERT`, `UPDATE`, and `COPY FROM`.

```sql
CREATE TABLE doc.payments (
  payment_id TEXT PRIMARY KEY,
  amount DOUBLE CHECK (amount >= 0),
  status TEXT CHECK (status IN ('pending', 'paid', 'failed'))
);
```

## Column Constraints

Applied inline with a column definition.

```sql
CREATE TABLE doc.accounts (
  id UUID PRIMARY KEY,
  email TEXT NOT NULL,
  age INT CHECK (age >= 18)
);
```

## Table Constraints

Applied at table level, often for multi-column rules.

```sql
CREATE TABLE doc.orders (
  order_id TEXT,
  customer_id TEXT,
  amount DOUBLE,
  PRIMARY KEY (order_id),
  CHECK (amount >= 0)
);
```

## Notes

- Prefer deterministic `CHECK` expressions.
- `PRIMARY KEY` columns are a natural fit for routing and point lookups.
- Validate index and constraint choices against workload patterns.

## Related

- [CREATE TABLE](./commands/35_CREATE_TABLE.md)
- [ALTER TABLE](./commands/17_ALTER_TABLE.md)
- [SQL Reference Overview](./01-sql-reference.md)
