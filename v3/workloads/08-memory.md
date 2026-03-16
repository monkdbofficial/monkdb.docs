# Memory Workloads

This guide demonstrates operational usage of MonkDB memory objects for session/context storage patterns.

## 1) Create base incident table

```sql
CREATE TABLE incidents (
  incident_id TEXT,
  summary TEXT,
  created_at TIMESTAMP
);

INSERT INTO incidents (incident_id, summary, created_at) VALUES
  ('inc-1', 'payment failure in eu', CURRENT_TIMESTAMP),
  ('inc-2', 'card auth timeout', CURRENT_TIMESTAMP);
```

## 2) Create memory object

```sql
CREATE MEMORY session_store
WITH (strict = true, entry_ttl_ms = 3600000, max_entries = 1000);
```

## 3) Inspect memory metadata

```sql
SELECT memory_name, options['strict'], options['entry_ttl_ms'], options['max_entries']
FROM memory.memories
WHERE memory_name = 'session_store';
```

## 4) Insert key-value entries

```sql
INSERT INTO memory.memory_entries (memory_name, entry_key, entry_value)
VALUES
  ('session_store', 'sess-42:intent', 'payment_failure'),
  ('session_store', 'sess-42:priority', 'urgent');
```

## 5) Read entries

```sql
SELECT memory_name, entry_key, entry_value
FROM memory.memory_entries
WHERE memory_name = 'session_store'
ORDER BY entry_key;
```

## 6) Upsert with conflict handling

```sql
INSERT INTO memory.memory_entries (memory_name, entry_key, entry_value)
VALUES ('session_store', 'sess-42:intent', 'payment_failure_v2')
ON CONFLICT (memory_name, entry_key) DO UPDATE
SET entry_value = excluded.entry_value;
```

## 7) Compact and monitor

```sql
ALTER MEMORY session_store COMPACT;

SELECT last_compacted_at IS NOT NULL,
       last_compaction_pruned_entries,
       total_compaction_pruned_entries
FROM memory.memories
WHERE memory_name = 'session_store';

SELECT strict, entry_ttl_ms, max_entries, active_entries, expired_entries, capacity_used_percent
FROM memory.memory_status
WHERE memory_name = 'session_store';
```

## 8) Cleanup

```sql
DROP MEMORY session_store;
```
