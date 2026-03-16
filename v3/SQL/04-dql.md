# DQL

## Standard select

```sql
SELECT id, total
FROM doc.orders
WHERE total > 100
ORDER BY total DESC
LIMIT 10;
```

## Joins and aggregations

```sql
SELECT c.customer_id, SUM(o.total) AS spend
FROM doc.customers c
JOIN doc.orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id
ORDER BY spend DESC;
```

## Vector search

```sql
WITH q AS (SELECT [0.3, 0.6, 0.0, 0.9] AS v)
SELECT text,
       VECTOR_SIMILARITY(embedding, (SELECT v FROM q)) AS score
FROM doc.word_embeddings
WHERE KNN_MATCH(embedding, (SELECT v FROM q), 5)
ORDER BY score DESC;
```

## Geospatial

```sql
SELECT id
FROM doc.places
WHERE within(location, 'POLYGON ((...))');
```

## Graph helper queries

```sql
SELECT * FROM graph_edges('social') ORDER BY table_name, source_vertex, target_vertex;
SELECT * FROM graph_neighbors('social', '1') ORDER BY neighbor_vertex;
SELECT vertex, depth, path FROM traverse('social', '1', 2) ORDER BY depth, vertex;
```
