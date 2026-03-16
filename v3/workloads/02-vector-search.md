# Vector Workloads

Use `FLOAT_VECTOR` columns for semantic retrieval and nearest-neighbor search.

## Create table

```sql
CREATE TABLE IF NOT EXISTS doc.documents (
  id TEXT PRIMARY KEY,
  content TEXT,
  embedding FLOAT_VECTOR(4) WITH (similarity = 'cosine')
);
```

## Upsert sample vectors

```sql
INSERT INTO doc.documents (id, content, embedding)
VALUES
  ('doc_1', 'MonkDB is great for time-series and vector workloads.', [0.91,0.07,0.01,0.22]),
  ('doc_2', 'Vector search in databases is important for AI applications.', [0.11,0.80,0.05,0.33]),
  ('doc_3', 'MonkDB provides scalable distributed storage.', [0.84,0.10,0.02,0.18])
ON CONFLICT (id) DO UPDATE
SET content = excluded.content,
    embedding = excluded.embedding;

REFRESH TABLE doc.documents;
```

## KNN query

```sql
WITH q AS (SELECT [0.10,0.79,0.06,0.30]::float_vector(4) AS v)
SELECT id, content, _score
FROM doc.documents
WHERE KNN_MATCH(embedding, (SELECT v FROM q), 2)
ORDER BY _score DESC;
```

## Similarity scoring query

```sql
WITH q AS (SELECT [0.10,0.79,0.06,0.30]::float_vector(4) AS v)
SELECT id,
       VECTOR_SIMILARITY(embedding, (SELECT v FROM q)) AS score
FROM doc.documents
ORDER BY score DESC
LIMIT 3;
```

## Similarity override (must match column similarity)

```sql
WITH q AS (SELECT [0.10,0.79,0.06,0.30]::float_vector(4) AS v)
SELECT id,
       VECTOR_SIMILARITY(embedding, (SELECT v FROM q), 'cosine') AS score
FROM doc.documents
WHERE KNN_MATCH(embedding, (SELECT v FROM q), 2, 'cosine')
ORDER BY score DESC;
```

