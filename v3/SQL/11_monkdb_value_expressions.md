# SQL Value Expressions

Value expressions are used in projections, filters, ordering, grouping, and DDL properties.

## Common Expression Classes

- Literals: strings, numbers, booleans, nulls, arrays, objects.
- Column references and dereference paths.
- Arithmetic and comparison operators.
- Boolean logic: `AND`, `OR`, `NOT`.
- Function calls (scalar, aggregate, window).
- Casts: `CAST(expr AS type)` and `expr::type`.
- Subqueries and existence checks.

## Example

```sql
SELECT
  id,
  amount * 1.18 AS amount_with_tax,
  CASE WHEN amount > 1000 THEN 'high' ELSE 'standard' END AS bucket
FROM doc.orders
WHERE customer_id IS NOT NULL
ORDER BY amount DESC;
```

## Notes

- Keep expressions sargable in `WHERE` clauses when possible.
- Prefer explicit casts in production SQL for stable behavior.
- Use `TRY_CAST` when ingest quality is uncertain.

## Related

- [SELECT](./commands/68_SELECT.md)
- [WITH (CTE)](./commands/79_WITH.md)
- [Scalar Functions Catalog](./06-scalar-functions.md)
