# DML

## INSERT / UPDATE / DELETE

```sql
INSERT INTO doc.orders (id, amount) VALUES ('o1', 42.5);
UPDATE doc.orders SET amount = 45.0 WHERE id = 'o1';
DELETE FROM doc.orders WHERE id = 'o1';
```

## COPY FROM (including protocol ingest)

```sql
COPY doc.raw_events
FROM 'file:///data/events.ndjson'
WITH (format = 'json')
RETURN SUMMARY;
```

## Memory entries DML constraints

`memory.memory_entries` has intentionally strict supported forms.

Supported insert pattern:

```sql
INSERT INTO memory.memory_entries (memory_name, entry_key, entry_value)
VALUES ('session_store', 'sess-1:state', 'open')
ON CONFLICT (memory_name, entry_key) DO UPDATE
SET entry_value = excluded.entry_value;
```

Key constraints:

- `RETURNING` is not supported on this insert path.
- Only `VALUES` source is supported.
- `ON CONFLICT` must target `(memory_name, entry_key)`.
- Only `SET entry_value = excluded.entry_value` is supported in conflict update.

Delete is restricted to key predicates on `memory_name` and `entry_key`.
