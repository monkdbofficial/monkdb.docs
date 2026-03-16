# Endpoints

MonkDB exposes SQL over two primary interfaces plus graph gateway endpoints.

## PGWire endpoint

- PostgreSQL protocol compatible.
- Default port: `5432`.
- Works with common Postgres drivers and tools.

## HTTP endpoint

- SQL over HTTP for REST-style integration.
- Default port: `4200`.

## Gremlin HTTP gateway

- `/_gremlin` and `/gremlin`
- Additional paths: `/capabilities`, `/conformance`, `/stats`

## Endpoint strategy

- Use PGWire for traditional SQL applications/BI.
- Use HTTP for service-to-service SQL calls.
- Use Gremlin endpoint for graph traversal workloads with policy guardrails.
