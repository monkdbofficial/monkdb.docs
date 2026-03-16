# Full-Text Search Workloads

Use full-text indexes and `MATCH()` for relevance-ranked text retrieval.

## Create table with FULLTEXT index

```sql
CREATE TABLE IF NOT EXISTS doc.articles (
  id INTEGER PRIMARY KEY,
  title TEXT,
  content TEXT,
  INDEX content_ft USING FULLTEXT (content) WITH (analyzer = 'english')
);
```

## Insert sample rows

```sql
INSERT INTO doc.articles (id, title, content) VALUES
  (1, 'Machine Learning', 'Machine learning algorithms power modern AI applications.'),
  (2, 'AI Ethics', 'Ethical considerations in AI are crucial for fairness and bias mitigation.'),
  (3, 'Databases', 'Distributed SQL systems support operational and analytical workloads.');

REFRESH TABLE doc.articles;
```

## MATCH query with relevance

```sql
SELECT id, title, content, _score
FROM doc.articles
WHERE MATCH(content, 'AI')
ORDER BY _score DESC;
```

## Multi-column weighted search

```sql
SELECT id, title, content, _score
FROM doc.articles
WHERE MATCH((title 2.0, content), 'machine learning')
ORDER BY _score DESC;
```

## Notes

- `LIKE` is not a substitute for full-text ranking semantics.
- Keep analyzers aligned to language and tokenization needs.

