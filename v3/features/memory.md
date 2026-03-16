# Memory

<div class="feature-tags"><span class="gh-label gh-label-release">26.3.1</span><span class="gh-label">Memory</span><span class="gh-label">Agentic</span><span class="gh-label">RAG</span></div>

MonkDB memory provides short-lived key/value state with SQL control plane and visibility tables.

## Memory objects

Create a memory namespace:

```sql
CREATE MEMORY session_store
WITH (strict = true, entry_ttl_ms = 3600000, max_entries = 1000);
```

Supported options:

- `strict` (boolean)
- `entry_ttl_ms` (long)
- `max_entries` (integer)

## Data path

Write/read through `memory.memory_entries`.

```sql
INSERT INTO memory.memory_entries (memory_name, entry_key, entry_value)
VALUES
  ('session_store', 'sess-42:intent', 'payment_failure'),
  ('session_store', 'sess-42:priority', 'urgent');

SELECT memory_name, entry_key, entry_value
FROM memory.memory_entries
WHERE memory_name = 'session_store'
ORDER BY entry_key;
```

Upsert pattern:

```sql
INSERT INTO memory.memory_entries (memory_name, entry_key, entry_value)
VALUES ('session_store', 'sess-42:intent', 'payment_failure_v2')
ON CONFLICT (memory_name, entry_key) DO UPDATE
SET entry_value = excluded.entry_value;
```

## Compaction

Manual compaction:

```sql
ALTER MEMORY session_store COMPACT;
```

Periodic compaction settings:

- `memory.compaction.enabled`
- `memory.compaction.interval`

## Status views

- `memory.memories`
- `memory.memory_entries`
- `memory.memory_status`

Example:

```sql
SELECT strict, entry_ttl_ms, max_entries, active_entries, expired_entries, capacity_used_percent
FROM memory.memory_status
WHERE memory_name = 'session_store';
```
