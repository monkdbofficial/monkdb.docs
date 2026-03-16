# UUID Data Type

<div class="feature-tags"><span class="gh-label gh-label-release">25.12.1</span><span class="gh-label">UUID</span><span class="gh-label">Data Type</span></div>

## Overview

MonkDB provides a first-class `UUID` type for table columns and expressions.

- Can be used as primary key or regular column.
- Stored/indexed as exact-match keyword-like field.
- Type preserved in mappings using metadata (`monkdb_type`).
- PostgreSQL OIDs supported (`2950` for uuid, `2951` for uuid[]).

## Basic usage

```sql
CREATE TABLE doc.users (
  id UUID PRIMARY KEY,
  name TEXT,
  created_at TIMESTAMPTZ
);

CREATE TABLE doc.orders (
  id UUID PRIMARY KEY DEFAULT gen_random_text_uuid(),
  amount DOUBLE PRECISION
);

SELECT *
FROM doc.orders
WHERE id = '550e8400-e29b-41d4-a716-446655440000';
```

## UUID generation functions

- `gen_random_uuid()`
- `uuid_generate_v4()` (alias)
- `gen_random_text_uuid()`

## Casting and validation behavior

Accepted inputs include:

- Canonical UUID string (`xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)
- `UUID` values
- `BytesRef`/string-like values that can be interpreted as UUID text
- URL-safe/base64 UUID bytes and text-UUID compatibility paths

Invalid UUID values are rejected by type casting/validation.

## Indexing guidance

Do:

- Use UUID as PK for entity identity.
- Index additional columns used in filters.

Don't:

- Add redundant index on UUID PK column.
- Over-index composite keys that always begin with UUID unless query patterns require it.
