# Geospatial WKB and 3D Retention

<div class="feature-tags"><span class="gh-label gh-label-release">25.12.1</span><span class="gh-label">Geospatial</span><span class="gh-label">WKB</span><span class="gh-label">3D</span></div>

MonkDB geospatial supports WKT and GeoJSON, and now also supports WKB input forms.

## WKB support

`geo_shape` and `geo_point` casting paths support WKB inputs in addition to WKT/GeoJSON.

Accepted WKB text forms include:

- `0x...` hex
- `x'...'` hex literal style
- `WKB(...)` wrapper form
- raw WKB bytes where applicable

## GeoJSON string ingest

`geo_shape` casting accepts GeoJSON provided as JSON text (`String`-style payloads), useful for JDBC/PG pipelines.

## 3D storage retention (Z ordinates)

MonkDB preserves Z ordinates for `geo_shape` round-trip storage paths:

- WKT -> storage -> retrieval
- GeoJSON -> storage -> retrieval
- WKB -> storage -> retrieval

## Current limitation

Spatial indexing/query evaluation remains 2D today.

- Z is ignored for spatial predicates (`within`, `intersects`, etc.)
- `geo_point` remains 2D for query semantics

This feature is about fidelity of stored geometry, not 3D query execution.
