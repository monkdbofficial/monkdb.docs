# Document / JSON Workloads

MonkDB supports JSON-like storage via `OBJECT` and collection handling via `ARRAY`.

## Create tables

```sql
CREATE TABLE IF NOT EXISTS doc.users (
  id INT PRIMARY KEY,
  name TEXT,
  address OBJECT(DYNAMIC),
  roles ARRAY(TEXT)
);

CREATE TABLE IF NOT EXISTS doc.articles (
  id INT PRIMARY KEY,
  title TEXT,
  tags ARRAY(TEXT)
);
```

## Insert samples

```sql
INSERT INTO doc.users (id, name, address, roles) VALUES
  (1, 'Alice', {city='New York', zipcode='10001'}, ['admin','editor']),
  (2, 'Bob',   {city='London', zipcode='SW1A'},   ['viewer']);

INSERT INTO doc.articles (id, title, tags) VALUES
  (1, 'Intro to MonkDB', ['database','sql','scalability']);

REFRESH TABLE doc.users, doc.articles;
```

## Query nested fields and arrays

```sql
SELECT id, name, address['city'] AS city
FROM doc.users
WHERE address['zipcode'] = '10001';

SELECT *
FROM doc.users
WHERE 'admin' = ANY(roles);

SELECT id, array_length(tags) AS tag_count
FROM doc.articles
WHERE array_length(tags) >= 3;
```

## Useful scalar helpers

```sql
SELECT object_keys(address), object_values(address) FROM doc.users;
SELECT array_length(tags) FROM doc.articles;
```

## Related function references

- [Scalar Functions Catalog](../SQL/06-scalar-functions.md)
- [SQL Value Expressions](../SQL/11_monkdb_value_expressions.md)

