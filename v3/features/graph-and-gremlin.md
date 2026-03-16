# Graph and Gremlin Gateway

<div class="feature-tags"><span class="gh-label gh-label-release">26.3.1</span><span class="gh-label">Graph</span><span class="gh-label">Gremlin</span></div>

MonkDB includes graph metadata, graph SQL helpers, and a Gremlin HTTP gateway.

## SQL graph model

- `CREATE GRAPH <name>`
- `CREATE VERTEX TABLE ... FOR GRAPH ... KEY ...`
- `CREATE EDGE TABLE ... FOR GRAPH ... SOURCE KEY ... TARGET KEY ...`

## End-to-end example

```sql
CREATE GRAPH social;

CREATE TABLE doc.users (
  id TEXT PRIMARY KEY,
  name TEXT,
  segment TEXT,
  embedding FLOAT_VECTOR(4),
  event_ts TIMESTAMPTZ,
  metric DOUBLE PRECISION
);

CREATE TABLE doc.follows (
  src_id TEXT,
  dst_id TEXT,
  event_ts TIMESTAMPTZ,
  weight DOUBLE PRECISION,
  PRIMARY KEY (src_id, dst_id)
);

CREATE VERTEX TABLE doc.users FOR GRAPH social KEY id;
CREATE EDGE TABLE doc.follows FOR GRAPH social SOURCE KEY src_id TARGET KEY dst_id;

INSERT INTO doc.users (id, name, segment, embedding, event_ts, metric) VALUES
  ('1','Alice','creator',[0.91,0.07,0.01,0.22],'2026-02-23T10:00:00Z',12.4),
  ('2','Bob','viewer',[0.11,0.80,0.05,0.33],'2026-02-23T10:05:00Z',8.1);

INSERT INTO doc.follows (src_id, dst_id, event_ts, weight) VALUES
  ('1','2','2026-02-23T11:00:00Z',0.9);

REFRESH TABLE doc.users, doc.follows;

SELECT * FROM graph_edges('social') ORDER BY table_name, source_vertex, target_vertex;
SELECT * FROM graph_neighbors('social', '1') ORDER BY neighbor_vertex;
SELECT vertex, depth, path FROM traverse('social', '1', 2) ORDER BY depth, vertex;
```

## Gremlin HTTP gateway

Endpoints:

- `/_gremlin` and `/gremlin`
- `/_gremlin/capabilities`
- `/_gremlin/conformance`
- `/_gremlin/stats`

Request JSON fields:

- Required: `graph`, `gremlin`
- Optional: `max_depth`, `max_rows`, `timeout_ms`, `request_id`
- Compatibility payloads: `op=eval`, `args`, `bindings`, `aliases`

## Policy and guardrail defaults

- `max_depth=8`
- `max_rows=10000`
- `timeout_ms=30000`
- `deny_unbounded_repeat=true`

Admission defaults:

- `assumed_fanout=16`
- `max_estimated_rows=500000`
- `max_estimated_work=2000000`
