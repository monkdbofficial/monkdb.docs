# Graph Workloads

This guide demonstrates graph modeling and traversal using SQL graph objects.

## 1) Create graph and base tables

```sql
CREATE GRAPH social;

CREATE TABLE doc.users (
  id TEXT NOT NULL,
  name TEXT,
  segment TEXT,
  embedding FLOAT_VECTOR(4),
  event_ts TIMESTAMPTZ,
  metric DOUBLE PRECISION,
  PRIMARY KEY (id)
);

CREATE TABLE doc.follows (
  src_id INT NOT NULL,
  dst_id INT NOT NULL,
  event_ts TIMESTAMPTZ,
  weight DOUBLE PRECISION,
  PRIMARY KEY (src_id, dst_id)
);

CREATE TABLE doc.likes (
  src_id INT NOT NULL,
  dst_id INT NOT NULL,
  event_ts TIMESTAMPTZ,
  weight DOUBLE PRECISION,
  PRIMARY KEY (src_id, dst_id)
);
```

## 2) Register vertex and edge tables

```sql
CREATE VERTEX TABLE doc.users FOR GRAPH social KEY id;
CREATE EDGE TABLE doc.follows FOR GRAPH social SOURCE KEY src_id TARGET KEY dst_id;
CREATE EDGE TABLE doc.likes   FOR GRAPH social SOURCE KEY src_id TARGET KEY dst_id;
```

## 3) Insert sample data

```sql
INSERT INTO doc.users (id, name, segment, embedding, event_ts, metric) VALUES
  (1, 'Alice', 'creator', CAST([0.91,0.07,0.01,0.22] AS FLOAT_VECTOR(4)), '2026-02-23T10:00:00Z', 12.4),
  (2, 'Bob',   'viewer',  CAST([0.11,0.80,0.05,0.33] AS FLOAT_VECTOR(4)), '2026-02-23T10:05:00Z',  8.1),
  (3, 'Cara',  'creator', CAST([0.84,0.10,0.02,0.18] AS FLOAT_VECTOR(4)), '2026-02-23T10:10:00Z', 15.9),
  (4, 'Dinesh','viewer',  CAST([0.20,0.71,0.04,0.40] AS FLOAT_VECTOR(4)), '2026-02-23T10:15:00Z',  7.7);

INSERT INTO doc.follows (src_id, dst_id, event_ts, weight) VALUES
  (1,2,'2026-02-23T11:00:00Z',0.9),
  (2,3,'2026-02-23T11:01:00Z',0.8);

INSERT INTO doc.likes (src_id, dst_id, event_ts, weight) VALUES
  (1,3,'2026-02-23T12:00:00Z',0.5),
  (3,1,'2026-02-23T12:01:00Z',0.4);

REFRESH TABLE doc.users, doc.follows, doc.likes;
```

## 4) Discover graph metadata

```sql
SELECT * FROM graph.graphs;
SELECT * FROM graph.vertices;
SELECT * FROM graph.edges;
```

## 5) Graph queries

```sql
SELECT *
FROM graph_edges('social')
ORDER BY table_name, source_vertex, target_vertex;

SELECT *
FROM graph_neighbors('social', '1')
ORDER BY neighbor_vertex;

SELECT vertex, depth, path
FROM traverse('social','1',2)
ORDER BY depth, vertex;
```

## 6) Hybrid graph + analytics query

```sql
SELECT date_trunc('hour', event_ts) AS hr, count(*)
FROM doc.follows
GROUP BY 1
ORDER BY 1;
```

## 7) Hybrid graph + vector query

```sql
SELECT id, name
FROM doc.users
ORDER BY vector_similarity(
  embedding,
  [0.90, 0.10, 0.00, 0.20]::float_vector(4)
) DESC
LIMIT 3;
```
