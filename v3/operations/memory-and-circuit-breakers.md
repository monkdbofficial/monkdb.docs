# Memory Configuration and Circuit Breakers

## JVM heap sizing

MonkDB runs on JVM. Heap is set through `MONKDB_HEAP_SIZE`.

Practical baseline:

- Start at ~25% of node RAM.
- Keep heap not below `1GB`.
- Prefer staying at or below ~`30.5GB` for Compressed Oops efficiency.

## Compressed Oops check

```bash
jcmd <pid> VM.info | grep "Compressed Oops"
```

If Compressed Oops is disabled, object pointer overhead increases.

## Swap and memory locking

Swapping degrades latency and stability.

Set in config if your host limits permit:

```yaml
bootstrap.memory_lock: true
```

Also configure OS memlock limits accordingly.

## Circuit breaker model

Circuit breakers are preventive memory guards. They estimate memory before/while operations run and abort work before heap exhaustion.

Common breaker categories:

- `query`
- `request`
- `jobs_log`
- `operations_log`
- `total` (parent)

## Typical exception

`CircuitBreakingException[Allocating ... failed, breaker would use ... Limit is ...]`

## Breaker incident response

1. Identify heavy active jobs:

```sql
SELECT j.id, stmt, username, SUM(used_bytes) AS sum_bytes
FROM sys.operations op
JOIN sys.jobs j ON op.job_id = j.id
GROUP BY j.id, stmt, username
ORDER BY sum_bytes DESC;
```

2. Check completed history in `sys.jobs_log` / `sys.operations_log`.
3. Optimize queries (filters, partitions, joins, cardinality).
4. Reduce concurrency for heavy workloads.
5. Scale cluster resources if pressure is persistent.

## Memory tuning checklist

- Validate heap setting against host RAM.
- Keep OS cache headroom for Lucene mmap access.
- Watch GC pauses after heap changes.
- Tune breaker limits only after query/profile analysis.
