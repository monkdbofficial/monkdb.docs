# FLOAT_VECTOR Similarity

<div class="feature-tags"><span class="gh-label gh-label-release">25.12.1</span><span class="gh-label">Vector</span><span class="gh-label">Similarity</span></div>

## What changed

MonkDB now supports explicit similarity selection per `FLOAT_VECTOR` column:

- Column DDL option: `WITH (similarity = '...')`
- Similarity stored in mappings and used by indexing/query planning
- `VECTOR_SIMILARITY` and `KNN_MATCH` accept optional similarity override
- Default remains `euclidean` for backward compatibility

## Supported similarity values

- `euclidean` (default)
- `cosine`
- `dot_product`
- `maximum_inner_product`

Accepted aliases include:

- `l2` for euclidean
- `dotproduct`, `dot-product` for dot product
- `cosine_similarity`, `cosine-similarity` for cosine
- `mips`, `max_inner_product` for maximum inner product

## DDL examples

```sql
CREATE TABLE euclid_default (
  id STRING PRIMARY KEY,
  embedding FLOAT_VECTOR(128)
);

CREATE TABLE word_embeddings (
  text STRING PRIMARY KEY,
  embedding FLOAT_VECTOR(4) WITH (similarity = 'cosine')
);

CREATE TABLE docs_dp (
  id STRING PRIMARY KEY,
  embedding FLOAT_VECTOR(768) WITH (similarity = 'dot_product')
);

CREATE TABLE recsys_mips (
  id STRING PRIMARY KEY,
  embedding FLOAT_VECTOR(256) WITH (similarity = 'maximum_inner_product')
);
```

## Query examples

Default column similarity:

```sql
WITH param AS (SELECT [0.3, 0.6, 0.0, 0.9] AS sv)
SELECT text,
       VECTOR_SIMILARITY(embedding, (SELECT sv FROM param)) AS score
FROM word_embeddings
WHERE KNN_MATCH(embedding, (SELECT sv FROM param), 2)
ORDER BY score DESC;
```

Override similarity (must be literal, non-null):

```sql
WITH param AS (SELECT [0.3, 0.6, 0.0, 0.9] AS sv)
SELECT text,
       VECTOR_SIMILARITY(embedding, (SELECT sv FROM param), 'dot_product') AS score
FROM word_embeddings
WHERE KNN_MATCH(embedding, (SELECT sv FROM param), 2, 'dot_product')
ORDER BY score DESC;
```

## Validation rules

- Similarity override must be a non-null literal string.
- Non-literal expressions are rejected at planning time.
- For `KNN_MATCH`, mismatch between override and column similarity fails early.
- Unsupported `WITH` options for `FLOAT_VECTOR` are rejected during analysis.

## Do / Don't

Do:

- Prefer column-declared similarity and omit override unless needed.
- Keep override values as literal strings.

Don't:

- Pass `NULL` or expressions as similarity overrides.
- Use unsupported options in `FLOAT_VECTOR ... WITH (...)`.
